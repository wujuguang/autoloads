#!/usr/bin/env python

from tornado.log import app_log
from tornado.options import define, options

define("output_encoding",
       default="utf-8",
       type=str,
       help="输出字符串的编码!")

define("scan_handlers_path",
       type=str,
       help="扫描handler的目录！")

define("directories",
       type=list,
       help="mako模板文件存储位置！")

define("module_directory",
       type=str,
       help="mako模板系统编译后py文件位置!")

define("port",
       type=int,
       help="系统监听端口！")


def parse_options_config():
    options.parse_command_line()
    app_log.info("初始化配置文件：%s" % 'config.conf')
    options.parse_config_file('config.conf')
