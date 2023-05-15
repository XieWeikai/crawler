#encoding:utf8
import os
from py2neo import Graph
import hashlib
from imgspider import baidu
import config
from tqdm import tqdm

data_path = config.data_dst_dir
limit_num = config.limit  # max diseases number
node_label = config.node_label
node_key = config.node_key
add_keyword = config.add_keyword

graph = Graph(config.uri, auth=config.auth)

# graph 为到neo4j的连接
# 以标签为label的节点中的key的值搜索出图片
# 下载到data目录下
# 限制最多limit条
# 将图片名称作为节点的attr_name
# additional_search_key为搜索图片时额外添加的关键字
def add_baidu_img(graph,label,key,limit,attr_name,additional_search_key):
    try :
        os.makedirs(data_path)
        print('make %s directory'%data_path)
    except OSError:
        print('%s directory already exists'%data_path)

    nodes = tqdm(graph.nodes.match(label).limit(limit), desc='downloading images')

    for node in nodes:
        if 'img' in node:  # already has img attribute
            continue
        nodes.set_postfix_str(f'handling :{node[key]}')
        img = baidu.baidu_img(f'{node[key]} {additional_search_key}')
        for meta, content in img.get_imgs(1, img=config.img_from):
            md5 = hashlib.md5()
            md5.update(content)
            file_name = md5.hexdigest() + '.' + meta['type']

            with open(f'{data_path}/{file_name}','wb') as f:
                f.write(content)

            node[attr_name] = file_name
            graph.push(node)

if __name__ == '__main__':
    add_baidu_img(graph,node_label,node_key,limit_num,'img',add_keyword)
