#!/usr/bin/env python

from pipe import Pipe


# ======================query=========================


@Pipe
def sql_query(_db_session, *cols):
    return _db_session.query(*cols)


@Pipe
def query_filter(query, *where):
    return query.filter(*where)


@Pipe
def offset(query, record_index):
    return query.offset(record_index)


@Pipe
def limit(query, record_size):
    return query.limit(record_size)


@Pipe
def first(query):
    return query.first()


# all was previously named get_all, avoid conflicts with the built-in all() function/type.

@Pipe
def get_all(query):
    return query.all()


@Pipe
def scalar(query):
    return query.scalar()


@Pipe
def order_by(query, *order_by_cols):
    return query.order_by(*order_by_cols)


@Pipe
def group_by(query, *group_by_cols):
    return query.group_by(*group_by_cols)


# =====================update=========================

@Pipe
def update(query, **attribute):
    return query.update(attribute, synchronize_session="fetch")


@Pipe
def add(_db_session, entity):
    return _db_session.add(entity)


@Pipe
def add_all(_db_session, entities):
    return _db_session.add_all(entities)


@Pipe
def delete(_db_session, entity):
    return _db_session.delete(entity)


@Pipe
def query_delete(query):
    return query.delete(synchronize_session="fetch")


@Pipe
def refresh(_db_session, entity):
    return _db_session.refresh(entity)


@Pipe
def flush(_db_session):
    return _db_session.flush()


# ===================transaction======================

@Pipe
def commit(_db_session):
    return _db_session.commit()


@Pipe
def rollback(_db_session):
    return _db_session.rollback()


@Pipe
def close(_db_session):
    return _db_session.close()
