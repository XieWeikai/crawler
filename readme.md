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

---

# 给知识图谱添加图片属性

## 脚本依赖

- py2neo: 用于连接neo4j数据库
- tqdm: 用于展示进度
- fake_useragent: 生成加的User-Agent
- requests: 发送http请求

## 使用docker配置proxy-pool

本项目使用了 https://github.com/jhao104/proxy_pool 实现的代理池，该项目从网上爬取免费的代理并以API的形式提供服务。本节将如何通过docker来配置使用proxy-pool.

创建一个供容器使用的网络

```bash
docker network create proxy_pool
```

创建`redis`容器

```bash
docker run --name redis-proxy-pool --network proxy_pool -d -p 6379:6379 redis
```

可以通过在本地运行`redis-cli`查看`redis`是否正常。

创建`proxy_pool`容器

```bash
docker run --name proxy_pool --env DB_CONN=redis://redis-proxy-pool:6379/0 \
-p 5010:5010 -d jhao104/proxy_pool:latest
```

启动后，用如下命令测试`proxy_pool`运行是否正常

```bash
curl localhost:5010/count/
```

若返回结果类似下面这样，则正常

```json
{"count":52,"http_type":{"http":41,"https":11},"source":{"freeProxy02":2,"freeProxy03":12,"freeProxy05":2,"freeProxy06":17,"freeProxy07":1,"freeProxy08":13,"freeProxy10":6}}
```

## 使用说明

项目目录下的`config.py`用于控制脚本行为，对各个配置解释如下

```python
# neo4j数据库连接
uri = "bolt://localhost:7687"
auth = ("neo4j", "123456")

# 使用py2neo match某个标签时最大返回节点数
# 如果设成100, 则在查找某个节点时最多查到100个节点
limit = 8807

# 要添加图片属性的节点标签 也可以设为'症状'等别的
node_label = '疾病'

# 搜索关键字时按照node的某个属性值来搜
# 例如此处设为'name', node_label设为'疾病'
# 则脚本会先找到标签为'疾病'的node
# 再以找到的node的name属性作为关键字查找图片
node_key = 'name'

# 搜索时额外添加的关键字
add_keyword = '症状'
```

`imgspider`目录下的`config.py`控制爬虫行为，解释如下

```python
# 获取代理间隔时间
get_proxy_interval = 1.0

# 若该值为True ,则每次计算时间间隔时会
# 将间隔乘上一个0~1之间的随机数
random_interval = True

# 查百度API时失败重试次数
retry_num = 10

# 爬取间隔
crawl_interval = 0.5
```

配置好后直接在项目目录下运行`add_image_to_kg.py`即可。若脚本卡住或出现其他问题，等待一段时间直接重新启动即可，之前已经处理过的`node`不会再次处理。