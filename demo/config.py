#!/usr/bin/env python

import functools

from sqlalchemy.engine import create_engine

from autoloads import ModelHelper

# 修改你自己的数据库连接参数
data_dsn = "mysql+pymysql://root:12345678@localhost/test_db"
db_engine = create_engine(data_dsn)

# 定义你数据库里及对应的表
MYSQL_DATABASES_TABLES = dict(
    test_db=["table_one", "table_two", "table_user"],
)


def generate_models(engine, databases_config, database_name, column_prefix='_'):
    """"从数据库表生成模型

        :param engine:              连接engine
        :param databases_config:    数据库配置
        :param database_name:　     数据库名称
        :param column_prefix:       属性(列)前缀
    """
    _database = database_name
    _tables = databases_config[_database]
    _models = ModelHelper.get_models(engine,
                                     tables=_tables,
                                     column_prefix=column_prefix,
                                     schema=_database)
    return _models


# 构建基本配置
generate_models = functools.partial(generate_models, db_engine, MYSQL_DATABASES_TABLES)

# 按数据库名称(如:"test_db")生成该数据库对应配置的表
# Number_1: 属于Init()过程
my_db_models = generate_models("test_db")

# 绑定数据表, 构建model, 如:(table_one,table_two)
# Number_2: 属于call()过程
# table_one = my_db_models("table_one")
# table_two = my_db_models("table_two")

if __name__ == '__main__':

    # 获得表table_one对应的Model
    table_one = my_db_models("table_one")

    # 使用Model的db_session_pool方法获取连接
    db_session = table_one.db_session_pool()

    table_one_info = db_session.query(table_one).filter().first()
    print(table_one_info, "=" * 5)
    if table_one_info:
        table_one_info._name = "test"
        table_one_info._text = "test_text"
    else:
        table_one_info = table_one()
        table_one_info._name = "test"
        # pass

    db_session.add(table_one_info)
    db_session.commit()
    db_session.close()
