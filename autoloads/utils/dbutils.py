#!/usr/bin/env python

import copy
from decimal import Decimal


def get_page_count(record_count, page_size):
    """获取页数.

        :param record_count: 记录数
        :param page_size: 每页条数
    """
    return int((record_count + page_size - 1) / page_size)


def get_record_index(page_index, page_size):
    """获取当前页起始条数索引.

        :param page_index: 第几页
        :param page_size: 每页条数
    """
    return int((page_index - 1) * page_size)


class Parser(object):
    def parser(self):
        """在子类中定义实质的解析.
        """
        raise Exception("Parser's function(parser) is not implement")

    def __call__(self):
        """为子类的方法使用返回 'parser()' 结果.
        """
        return self.parser()


class BuildFilter(Parser):
    """从实体类的实例中构建过滤条件.
    """

    def __init__(self, entity):
        self._entity = entity

    def parser(self):
        # 如果为空返回空列表.
        if not self._entity:
            return []

        cls = self._entity.__class__
        if hasattr(cls, "filter_attr_dict") and cls.filter_attr_dict:
            # 如果实体类有该项, 并且该项的值为真.
            filter_attr_dict = cls.filter_attr_dict
            filter_list = [
                filter_attr_dict[x](getattr(self._entity, x))
                for x in filter_attr_dict
                if getattr(self._entity, x) is not None
            ]
        else:
            attributes = cls.columns().keys()
            filter_list = [
                getattr(cls, x) == getattr(self._entity, x)
                for x in attributes
                if getattr(self._entity, x)
            ]

        return filter_list


class RequestParser(Parser):
    """构建实体类的属性数据, 以请求处理器中数据为原料, 以字典的形式返回.
    """

    parser_types = [int, float, Decimal]

    def __init__(self, cls, request):
        """
            :param cls:     实体模型类
            :param request: 页面处理器请求(self.request)

        在页面请求处理器中使用形式如下::

            class Test(BaseRequestHandler):
                def get(self):
                    from models import User
                    rp = RequestParser(User, self.request)
        """

        self.cls = cls
        self.request_arguments = copy.deepcopy(request.arguments)  # 请求处理器传入的数据
        self.column_prefix = self.cls.column_prefix()  # 实体模型类的属性前缀

    def parser(self):
        """构建实体类的属性数据, 以请求处理器中数据为原料, 以字典的形式返回.
        """

        # 都为空时返回
        if not self.cls and not self.request_arguments:
            return None

        # 从请求参数(request.arguments)的key/value中, 构建新的字典(key增加前缀).
        args = {"%s%s" % (self.column_prefix, arg): self.request_arguments[arg] for arg in self.request_arguments}

        request_parser_dict = {}
        if hasattr(self.cls, "request_parser_attr_dict") and self.cls.request_parser_attr_dict:
            # 如果实体类有该项, 并且该项的值为真.
            request_parser_attributes = self.cls.request_parser_attr_dict.keys()

            # 遍历实体类的request_parser_attr_dict属性集.
            # 如果有属性存在于请求参数(request.arguments)则记录.
            for attr in request_parser_attributes:
                if attr in args:
                    request_parser_dict[attr] = self.cls.request_parser_attr_dict[attr](args[attr][-1])
        else:
            # 如果实体类无该项, 则以该实体类的全列.
            attributes = dict(self.cls.columns().items())
            for attr in args.keys():
                if attr in attributes:
                    # 获取数据库列的对应python类型.
                    py_type = attributes[attr].type.python_type
                    _value = args[attr][-1]
                    if py_type in self.__class__.parser_types:
                        request_parser_dict[attr] = py_type(_value)
                    elif isinstance(_value, bytes):
                        request_parser_dict[attr] = _value.decode('utf-8')
                    else:
                        request_parser_dict[attr] = _value

        return request_parser_dict


class EntityParser(Parser):
    """模型类实例更新. 将一个字典key/value集合, 设置到该实例对应的key属性上, 返回实例.
    """

    def __init__(self, entity, **_attributes):
        """
            :param entity 模型类实例
            :param _attributes 字典对象
        """
        self.entity = entity
        self._attributes = _attributes

    def parser(self):
        """如果类实例不为空, 遍历字典中每一项, 如果该项存在于类实例, 则传递该项值于类实例.
        """
        if self.entity:
            for attr in self._attributes:
                if hasattr(self.entity, attr):
                    setattr(self.entity, attr, self._attributes[attr])
        return self.entity
