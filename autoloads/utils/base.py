#!/usr/bin/env python

from autoloads.utils import json_encode
from autoloads.utils.datatype import json_data_encode
from autoloads.utils.dbhelper import DBEntityHelper


class Entity(object):
    """包含实体对象的简单操作.
    """

    db_operate_cls = DBEntityHelper

    def __init__(self, **kwargs):
        for _key in kwargs:
            setattr(self, "%s" % _key, kwargs[_key])

    def save(self):
        self.__class__.add(self)

    def json_decode_attrs(self):
        """需要json化的对象属性.
        """
        pass

    def json_attr_parser_funcs(self):
        """需要进行数据处理的属性方法.
        """
        pass

    @classmethod
    def column_prefix(cls):
        return cls.__mapper_args__["column_prefix"]

    @classmethod
    def columns(cls):
        return cls.__mapper__.columns

    def json(self):
        column_prefix_len = len(self.__class__.column_prefix())
        _attribute = self.json_decode_attrs() or self.__class__.columns().keys()
        _parser_funcs = self.json_attr_parser_funcs() or {}
        attr_items = [
            (_attr,
             _parser_funcs[_attr](getattr(self, _attr)) if _attr in _parser_funcs else getattr(self, _attr))
            for _attr in _attribute]

        attr_items = map(lambda x: (x[0][column_prefix_len:], x[1]), attr_items)
        attr_dict = dict(attr_items)
        return attr_dict

    def __str__(self):
        attr_dict = self.json()

        try:
            result = json_encode(attr_dict)
        except TypeError:
            result = json_data_encode(attr_dict)
        return result

    def __repr__(self):
        return self.__str__()


class EntityHelper(object):
    """数据库操作封装.
    """

    @classmethod
    def add(cls, entity, refresh=True):
        db_operate = cls.db_operate_cls(entity_cls=cls)
        try:
            db_operate.add(entity)
            if refresh:
                db_operate.flush()
                db_operate.refresh(entity)
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()

    @classmethod
    def add_all(cls, entitys, refresh=True):
        db_operate = cls.db_operate_cls(entity_cls=cls)
        try:
            db_operate.add_all(entitys)
            if refresh:
                db_operate.flush()
                for _entity in entitys:
                    db_operate.refresh(_entity)
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()

    @classmethod
    def delete(cls, entity):
        db_operate = cls.db_operate_cls(entity_cls=cls)
        try:
            db_operate.delete(entity)
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()

    @classmethod
    def delete_by_where(cls, wheres=None):
        db_operate = cls.db_operate_cls(entity_cls=cls, wheres=wheres)
        try:
            db_operate.delete_all()
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()

    @classmethod
    def update_by_where(cls, wheres=None, **attrs):
        db_operate = cls.db_operate_cls(entity_cls=cls, wheres=wheres)
        try:
            db_operate.update_all(**attrs)
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()

    @classmethod
    def get_scalar_by_where(cls, query_expr, wheres=None):
        db_operate = cls.db_operate_cls(entity_cls=cls, wheres=wheres)
        try:
            _count = db_operate.get_scalar(query_expr)
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()
        return _count

    @classmethod
    def get_statistics_by_group(cls, recordindex, pagesize, group_by_list, order_by_cols=None, wheres=None, cols=None):
        db_operate = cls.db_operate_cls(entity_cls=cls,
                                        entity_cols=cols,
                                        wheres=wheres,
                                        order_by_cols=order_by_cols)
        try:
            _statistics = db_operate.get_statistics_by_group(group_by_list, recordindex, pagesize)
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()
        return _statistics

    @classmethod
    def get_first_by_where(cls, wheres=None, cols=None):
        db_operate = cls.db_operate_cls(entity_cls=cls,
                                        entity_cols=cols,
                                        wheres=wheres)
        try:
            _entity = db_operate.get_first()
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()
        return _entity

    @classmethod
    def get_first_order_by_where(cls, order_by_cols, wheres=None, cols=None):
        db_operate = cls.db_operate_cls(entity_cls=cls,
                                        entity_cols=cols,
                                        wheres=wheres,
                                        order_by_cols=order_by_cols)
        try:
            _entity = db_operate.get_first_order_by()
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()
        return _entity

    @classmethod
    def get_all_by_where(cls, recordindex, pagesize, wheres=None, cols=None):
        db_operate = cls.db_operate_cls(entity_cls=cls,
                                        entity_cols=cols,
                                        wheres=wheres)
        try:
            entities = db_operate.get_all(recordindex, pagesize)
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()
        return entities

    @classmethod
    def get_all_order_by_where(cls, recordindex, pagesize, order_by_cols, wheres=None, cols=None):
        db_operate = cls.db_operate_cls(entity_cls=cls,
                                        entity_cols=cols,
                                        wheres=wheres,
                                        order_by_cols=order_by_cols)
        try:
            entities = db_operate.get_all_order_by(recordindex, pagesize)
            db_operate.commit()
        except Exception as ex:
            db_operate.rollback()
            raise
        finally:
            db_operate.close()
        return entities


# 为兼容之前使用此组件的老项目
EntityOper = EntityHelper
