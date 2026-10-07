#!/usr/bin/env python

import os
from autoloads.utils import json_encode


class Tornado(object):
    """视图URL处理装饰器.
    """

    format_funcs = {
        'string': lambda s: s,
        'json': json_encode,
    }

    handlers = []  # 存储该应用程序的处理器.
    not_scan_file = ['__init__']  # 不扫描的文件名.

    def __new__(cls):
        if 'instance' not in cls.__dict__:
            cls.instance = object.__new__(cls)
        return cls.instance

    def __call__(self):
        return Tornado.handlers

    def _get_scan_file(self, dir_path):
        """获取处理器模块列表.

            :param dir_path: 处理器视图目录 注意: scan_dir 为相对路径.
        """

        file_list = []
        for s in os.listdir(dir_path):
            new_dir = os.path.join(dir_path, s)
            if os.path.isfile(new_dir):
                # 为文件时操作
                file_dir = os.path.splitext(new_dir)
                if file_dir[1] == '.py':
                    # 只取不带后缀的文件名.
                    _file_name = file_dir[0]
                    if _file_name.startswith('./'):
                        _file_name = _file_name[2:]
                    _file_name = _file_name.split('/')
                    if not set(Tornado.not_scan_file) & set(_file_name):
                        # 转换文件路径形式为python路径形式.
                        _file_name = '.'.join(_file_name)
                        file_list.append(_file_name)
            elif os.path.isdir(new_dir):
                # 为目录时递归
                file_list.extend(self._get_scan_file(new_dir))
        return file_list

    def scan(self, scan_dir):
        """从指定目录扫描python处理器文件, 并导入.

            :param scan_dir: 处理器视图目录 注意: scan_dir 为相对路径.
        """

        _scan_file_list = self._get_scan_file(scan_dir)
        for _scan_file in _scan_file_list:
            # print((' scan url => ', _scan_file))
            __import__(_scan_file)

    def route(self, path='/', **kw):
        """页面请求处理器的装饰器, 用于绑定url地址.

            :param path: url正则路径.

        在页面请求处理器中使用形式如下::

            @app.route('/test')
            class Test(BaseRequestHandler):
                pass
          """

        def _cls(cls):
            self.handlers.append((path, cls, kw))
            return cls

        return _cls


app = Tornado()
