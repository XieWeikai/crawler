# 百度图片爬虫

## 目标

为构造多模态知识图谱，初步尝试从百度图片爬取相关条目的图片。

## 说明

### imgspider包

该包内有目前只有一个`baidu.py`,该模块中有一个类`baidu_img`，该类实现了简单的按照关键词爬取百度图片的功能，详见代码注释。

### 使用

`main.py`为程序入口。`config.py`中配置爬取相关参数，其内容如下

```python
# 数据源目录
data_src_dir = 'graph_data'

# 爬取数据目录
data_dst_dir = 'data'

# 关键字文件
# 内容为json数组
files = [
    'diseases.json',
    'drugs.json'
]

# 若希望某些文件中的关键字搜索时额外添加一些关键字就在这里加
# 例: 'diseases.json':'disease'
# 则diseases.json中出现的关键字在搜索时都会加上 疾病 这个关键字
additional_keywords = {

}

# 每个关键字爬取图片数量
num_per_item = 1

# 爬取关键字个数
num_of_item = 100

# 爬取百度自己存的缩略图或从图片源网站爬取图片
# 可选取值为thumb(缩略图) origin(图片源)
img_from = 'thumb'
```

上面为示例，设置好各参数运行`main.py`即可。