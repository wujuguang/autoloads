#!/usr/bin/env python

from collections.abc import Iterable
from datetime import date, datetime
from decimal import Decimal
from json import dumps


def json_data_encode(json_data):
    """可以序列化 datetime等多类型数据.

        :param json_data
    """

    def _any(data):
        if isinstance(data, dict):
            return_data = _dict(data)
        elif isinstance(data, Iterable) and not isinstance(data, (str, bytes)):
            return_data = _list(data)
        elif isinstance(data, Decimal):
            return_data = str(data)
        elif isinstance(data, float):
            return_data = float(data)
        elif isinstance(data, datetime):
            return_data = data.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(data, date):
            return_data = data.strftime('%Y-%m-%d')
        else:
            return_data = data
        return return_data

    def _list(data):
        list_data = []
        for v in data:
            list_data.append(_any(v))
        return list_data

    def _dict(data):
        dict_data = {}
        for k, v in data.items():
            dict_data[k] = _any(v)
        return dict_data

    ret = _any(json_data)
    return dumps(ret, cls=None, ensure_ascii=False, indent=4)
