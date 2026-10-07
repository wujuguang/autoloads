#!/usr/bin/env python

from models.base import BaseModel
from config import my_db_models

from autoloads import Entity

# 根据自动加载的数据库models获取对应的model
user = my_db_models('table_user')


class User(user, BaseModel):
    # 供BuildFilter使用, 过滤条件的生成字典, 根据该字典生成对应的过滤条件.
    filter_attr_dict = dict(
        _id=lambda x: User._id == int(x),
    )

    # 供RequestParser使用, 请求参数(self.request)的字典生成处理, 根据该项生成包含对应model的属性的字典.
    request_parser_attr_dict = dict(
        _id=lambda x: int(x),
    )

    # 返回需要生成json的字段, 返回None则包含所有字段.
    def json_decode_attrs(self):
        return ["_id"]

    # 生成json()时, 对应字段的处理方式.
    def json_attr_parser_funcs(self):
        return dict(
            _id=int,
        )

    def __init__(self, **kargs):
        Entity.__init__(self, **kargs)
