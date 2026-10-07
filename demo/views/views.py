#!/usr/bin/env python

from models.models import User

from autoloads import app, BaseRequestHandler, BuildFilter, RequestParser


class BaseHandler(BaseRequestHandler):
    def response_json(self, data="", curr_page_index=1, page_count=0, success=True, **kw):
        kwargs = dict(
            success=success,
            message=dict(
                curr_page_index=curr_page_index,
                page_count=page_count,
                data=data,
                **kw))

        result = self.build_response_json(**kwargs)
        self.write(result)
        self.finish()


@app.route('/test')
class Test(BaseHandler):
    def get(self):
        # 从request中获取参数, 并对应User实体类生成对应的dict.
        rp = RequestParser(User, self.request)

        # 将根据request生成的dict作为参数传入User实体中.
        cu = User(**rp())

        # 根据User实体类的实例cu生成过滤条件.
        bf = BuildFilter(cu)

        # 根据条件查询实例.
        cus = User.get_all_by_where(0, 10, bf())

        # 将实例全部转换成字典.
        cus = [cu.json() for cu in cus]

        # 创建固定格式的返回数据结构.
        self.response_json(data=cus, success=True)
