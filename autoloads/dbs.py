import logging

from sqlalchemy import Table, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)


class ModelHelper:

    @staticmethod
    def get_models(db_engine, tables=None, column_prefix='_', schema=None):
        return Models(db_engine, tables, column_prefix, schema)


class Models:
    def __call__(self, table_name=None):
        if table_name is None:
            return self.models
        return self.models[table_name]

    def get(self, table_name=None):
        return self.__call__(table_name)

    def get_base(self):
        if not hasattr(self, '_base'):
            self._base = declarative_base()
        return self._base

    def get_db_session_pool(self):
        if not hasattr(self, 'db_session_pool'):
            self.db_session_pool = sessionmaker(expire_on_commit=self.expire_on_commit)
            self.db_session_pool.configure(bind=self.engine)

        return self.db_session_pool

    def __init__(self, db_engine, tables=None, column_prefix='_', schema=None, expire_on_commit=False):
        """根据某个session实例，从绑定的数据库里生成制定表的Model.

            注意:
                1.若tables为None, 从绑定数据库生成所有对应的model.
                2.若数据库表缺失主键, 生成Model会失败.

            :param tables: 表名
            :param column_prefix: Model的属性前缀
            :param db_engine: create_engine()实例
        """
        self.models = {}
        self.schema = schema
        self.column_prefix = column_prefix

        self.get_base()
        self.engine = db_engine
        self.expire_on_commit = expire_on_commit
        self.db_session_pool = self.get_db_session_pool()
        self.table_names = tables if tables else inspect(self.engine).get_table_names()

        errors = []
        for _table_ in self.table_names:
            _table_name = f'{_table_}'
            try:
                self.models[_table_name] = self._generate_model(_table_name)
            except Exception as ex:
                logger.warning('Model generate failed for table %s: %s', _table_name, ex)
                errors.append(f'Table Name: {_table_name}, Error: {ex}')

        self.errors = errors
        if errors:
            logger.error('%d table(s) failed to generate models.', len(errors))
            if not self.models:
                raise RuntimeError(
                    f'No models were generated; all {len(self.table_names)} table(s) failed. Errors: {errors}'
                )

    def _generate_model(self, table_name, model_name=None):

        if model_name is None:
            model_name = table_name

        kwarg = dict(autoload_with=self.engine, schema=self.schema)
        _table = Table(table_name, self._base.metadata, **kwarg)

        kwarg = {'__table__': _table,
                 '__mapper_args__': {'column_prefix': self.column_prefix},
                 'db_session_pool': self.db_session_pool}
        _model = type(model_name, (self._base,), kwarg)
        return _model
