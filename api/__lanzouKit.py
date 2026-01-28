#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hook document.cookie 直接拿值
pip install quickjs
By Kimi AI
"""

import re
import quickjs

class LanZou:
    # 1. 准备一段“前置”代码，用来 Hook document.cookie 的 setter
    HOOK_JS = """
    var fakeLocation = { reload: function() {} };
    var _cookieCache = '';
    var document = {
        cookie: '',
        get cookie() { return _cookieCache; },
        set cookie(val) {
            _cookieCache = val;
            if (val.includes('acw_sc__v2='))
                __acw_sc__v2_value = val.split(';')[0].split('=')[1];
        },
        location: fakeLocation
    };
    globalThis.document = document;
    globalThis.location = fakeLocation;
    """

    def __init__(self):
        pass

    def extract_cookie(self, script_html: str) -> str:
        # 抠 <script> 里的纯 JS（这部分不改）
        match = re.search(r'<script>(.*?)</script>', script_html, flags=re.S)
        if not match:
            raise ValueError('未找到 <script> 标签')
        inner_js = match[1]

        ctx = quickjs.Context()
        # 先下钩子
        ctx.eval(self.HOOK_JS)
        # 再跑服务器给的完整脚本（含 OB 混淆）
        ctx.eval(inner_js)
        # 把我们截到的值拿出来
        try:
            return ctx.eval('__acw_sc__v2_value')
        except quickjs.JSException:
            raise RuntimeError('没能截获 acw_sc__v2，可能脚本结构已变动')
