#!/usr/bin/env python

from autoloads.utils.dbpipe import sql_query, query_filter, offset, limit, first, \
    get_all, scalar, order_by, group_by, update, add, add_all, delete, query_delete, \
    flush, refresh, commit, rollback, close


class DBEntityHelper(object):
    def __init__(self, entity_cls, entity_cols=None, wheres=None, order_by_cols=None):
        """
            :param entity_cls:      实体类
            :param entity_cols:     实体列
            :param wheres:          过滤条件
            :param order_by_cols:   排序条件
        """

        self._entity_cls = entity_cls
        self._entity_cols = entity_cols or [entity_cls]
        self._db_session = self._entity_cls.db_session_pool()
        self._where = wheres or []
        self._order_by_cols = order_by_cols or []

    def commit(self):
        return self._db_session | commit

    def rollback(self):
        return self._db_session | rollback

    def close(self):
        return self._db_session | close

    def get_query(self, *cols):
        return self._db_session | sql_query(*cols) | query_filter(*self._where)

    def get_first(self):
        return self.get_query(*self._entity_cols) | first

    def get_first_order_by(self):
        return self.get_query(*self._entity_cols) | order_by(*self._order_by_cols) | first

    def get_all(self, record_index, record_size):
        return self.get_query(*self._entity_cols) | offset(record_index) | limit(record_size) | get_all

    def get_all_order_by(self, record_index, record_size):
        return self.get_query(*self._entity_cols) | order_by(*self._order_by_cols) | offset(record_index) | limit(
            record_size) | get_all

    def get_scalar(self, query_expr):
        return self.get_query(query_expr) | scalar

    def get_statistics_by_group(self, group_by_list, record_index, record_size):
        return self.get_query(*self._entity_cols) | group_by(*group_by_list) | order_by(*self._order_by_cols) | offset(
            record_index) | limit(record_size) | get_all

    def add(self, entity):
        return self._db_session | add(entity)

    def add_all(self, entities):
        return self._db_session | add_all(entities)

    def delete(self, entity):
        return self._db_session | delete(entity)

    def delete_all(self):
        return self.get_query(*self._entity_cols) | query_delete

    def update_all(self, **_attributes):
        return self.get_query(*self._entity_cols) | update(_attributes)

    def refresh(self, entity):
        return self._db_session | refresh(entity)

    def flush(self):
        return self._db_session | flush
