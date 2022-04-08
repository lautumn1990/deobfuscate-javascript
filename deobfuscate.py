#! /usr/bin/env python3
# -*- coding:utf-8 _*-

"""
@author: lautumn
@license: Apache Licence
@file: deobfuscate.py
@time: 2022/4/8 10:49
"""
import os
import re
import execjs
from pathlib import Path

origin_file = 'origin/test.js'
target_file = 'target/test.js'
js_func_name = '_0xea12'  # 混淆js中函数定义的名称

replace_fun_set = set([])

# 一些函数可能进行了替换
replace_fun_pattern = ['var\s([\d\w]+)\s+=\s+', 'const\s([\d\w]+)\s+=\s+']

be_replaced_func_set = set([])

func_js = r"""
// 直接用重组后的数组替换原来的数组
var _0xa12e = ['pad', 'clamp', 'sigBytes', 'YEawH', 'yUSXm', 'PwMPi', 'pLCFG', 'ErKUI', 'OtZki', 'prototype', 'endWith', 'test', '8RHz0u9wbbrXYJjUcstWoRU1SmEIvQZQJtdHeU9/KpK/nBtFWIzLveG63e81APFLLiBBbevCCbRPdingQfzOAFPNPBw4UJCsqrDmVXFe6+LK2CSp26aUL4S+AgWjtrByjZqnYm9H3XEWW+gLx763OGfifuNUB8AgXB7/pnNTwoLjeKDrLKzomC+pXHMGYgQJegLVezvshTGgyVrDXfw4eGSVDa3c/FpDtban34QpS3I=', 'enc', 'Latin1', 'parse', 'window', 'location', 'href', '146385F634C9CB00', 'decrypt', 'ZeroPadding', 'toString', 'split', 'length', 'style', 'type', 'setAttribute', 'async', 'getElementsByTagName', 'NOyra', 'fgQCW', 'nCjZv', 'parentNode', 'insertBefore', 'head', 'appendChild', 'fromCharCode', 'ifLSL', 'undefined', 'mPDrG', 'DWwdv', 'styleSheets', 'addRule', '::before', '.context_kw', '::before{content: "', 'cssRules']

// 解混淆用到的函数
function _0xea12(_0x56430f, _0x7f6841) {
	_0x56430f = _0x56430f - 0x0;
	var _0x4f7a0f = _0xa12e[_0x56430f];
	return _0x4f7a0f;
};
"""


def do_decode():
    # 1.编译解混淆函数到node.js环境中
    ctx = execjs.compile(func_js)

    # 2.正则匹配出所有需要替换的函数
    with open(origin_file, encoding='utf-8') as f1:
        js = f1.read()
    replaceFunSet = {js_func_name}

    # print(replaceFunSet)
    # print(len(replaceFunSet))

    size = -1
    while len(replaceFunSet) != size:
        size = len(replaceFunSet)
        for pattern in replace_fun_pattern:
            for fun in replaceFunSet.copy():
                funSet = set(re.findall(pattern + fun, js))
                replaceFunSet.update(funSet)
    # print(replaceFunSet)
    # print(len(replaceFunSet))
    # return

    for replaceFun in replaceFunSet:
        be_replaced_func = set(re.findall(replaceFun + "\([\s\S]+?\)", js))
        be_replaced_func_set.update(be_replaced_func)

    # 3.循环遍历进行替换
    for be_replaced_func in be_replaced_func_set:
        try:
            args_tuple = re.findall("\(([\s\S]+?)\)", be_replaced_func)[0]
            args0 = eval(args_tuple.split(',')[0])

            res = ctx.call(js_func_name, args0)

            res = res.replace("\n","\\n")
            js = js.replace(be_replaced_func, "'" + res + "'")
            print('{} 替换完成'.format(res))
        except:
            pass


    Path(os.path.dirname(target_file)).mkdir(parents=True, exist_ok=True)
    with open(target_file, 'w', encoding='utf-8') as f2:
        js = f2.write(js)
    pass


if __name__ == '__main__':
    do_decode()
