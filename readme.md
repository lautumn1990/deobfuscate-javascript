# 使用python库还原字面量

参考[js混淆还原](https://blog.csdn.net/weixin_42156283/article/details/104576280)

针对数组类混淆, 可以找出变量函数然后进行代码替换

先使用[jsbeautifier](http://jsbeautifier.org/)进行一遍格式化

```sh
# 安装
pip install PyExecJS
```

手动找到混淆函数

如果碰到`UnicodeEncodeError: 'gbk' codec can't encode character '\U0001f55b' in position 7226: illegal multibyte sequence`错误,
则修改`subprocess.py`文件,
如`C:\Users\Lenovo\AppData\Local\Programs\Python\Python39\Lib\subprocess.py`, 
中的`class Popen`->`def __init__`->`encoding=None`改成`encoding="utf-8"`