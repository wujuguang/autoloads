#!/usr/bin/env python

from sqlalchemy import Table, inspect
from sqlalchemy.orm import declarative_base, sessionmaker


class ModelHelper(object):

    @staticmethod
    def get_models(db_engine, tables=None, column_prefix='_', schema=None):
        return Models(db_engine, tables, column_prefix, schema)


class Models(object):
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
            _table_name = '{0}'.format(_table_)
            try:
                self.models[_table_name] = self._generate_model(_table_name)
            except Exception as ex:
                errors.append('Table Name: %s, Error: %s' % (_table_name, ex))

        if errors:
            print('\n', '=' * 40, 'Error In Generate Mode', '=' * 40)
            print(errors)

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
