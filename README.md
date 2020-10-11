# ad_json - 对Python json模块的扩展版

ad_json模块功能：

* 支持普通json模块的load、loads、dump、dumps功能；

* 支持下标方式和**属性方式**，对值进行访问和修改。

json格式文件test.json中的内容如下：

```python
{
    "a": [{"a": 0}, 2], 
    "b": {}, 
    "c": 2
}
```

加载json文件和修改属性：

```python
with open("test.json", "r", encoding="utf-8") as fp:
    ad_json = AdJson()
    ad_json.load(fp)

    ad_json.a[0].a = 3
    ad_json.b.e.f = 10

    print(ad_json.dumps())
```

上述操作输出：

```python
{"a": [{"a": 3}, 2], "b": {"e": {"f": 10}}, "c": 2}
```

## 安装

将工程下载到本地，然后在命令行中执行：

```python
python setup.py install
```

## 使用

**1.非常简便的使用属性访问方式创建嵌套的字典**

```python
>>> from ad_json import AdJson
>>> some_json = AdJson()
>>> some_json.a.b.c = 10
>>> some_json
{'a': {'b': {'c': 10}}}
```

**2.使用新字典，更新当前对象属性**

```python
>>> from ad_json import AdJson
>>> some_json = AdJson()
>>> some_json.a.b.c = 10
>>> new_dict = {"c": [1, 2, 3]}
>>> some_json.update(new_dict)
>>> some_json
{'a': {'b': {'c': 10}}, 'c': [1, 2, 3]}
```

**3.将创建的json数据dump到文件**

```python
>>> from ad_json import AdJson
>>> some_json = AdJson()
>>> some_json.a.b.c = 10
>>> with open("test.json", "w", encoding="utf-8") as fp:
        some_json.dump(fp)
```

## 测试用例

测试用例文件位于工程的test目录的test_ad_json.py文件中，可采用下列方式运行：

```python
python test/test_ad_json.py
```


## 结语

欢迎大家斧正，谢谢大家的支持！！

作者：youngzhiyong
邮箱：youngzhiyong@yeah.net
