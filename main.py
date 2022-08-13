import os
import json
import hashlib
from time import sleep

import requests
from imgspider.baidu import baidu_img

import config

# 关键词迭代器
# 通过config生成关键词
def items():
    count = 0
    for file in config.files :
        file_path = os.path.join(config.data_src_dir,file)
        key_words = None
        with open(file_path,'r') as f:
            key_words = json.load(f)
            for key_word in key_words:
                if count >= config.num_of_item:
                    return
                additional_word = config.additional_keywords.get(file)
                if additional_word is not None:
                    key_word = key_word + ' ' + additional_word
                yield key_word
                count += 1

def download(key_words):
    try :
        os.makedirs(os.path.join(config.data_dst_dir,'img'))
        print('make %s directory'%config.data_dst_dir)
    except OSError:
        print('%s directory already exists'%config.data_dst_dir)

    count = 0
    with open(os.path.join(config.data_dst_dir,'info.txt'),'w') as output:
        for key_word in key_words:
            img = baidu_img(key_word)
            for data,content in img.get_imgs(config.num_per_item,img=config.img_from):
                md5 = hashlib.md5()
                md5.update(data['title'].encode('utf-8'))
                name = md5.hexdigest() + '.' + data['type']
                with open(os.path.join(config.data_dst_dir,'img',name),'wb') as f:
                    f.write(content)
                data['imgName'] = name
                output.write(json.dumps(data,ensure_ascii=False)+'\n')
            print('keyword:%s/%s'%(count,config.num_of_item))
            count += 1
            if count > 0 and count % 20 == 0:
                print('sleep for 1s')
                sleep(1)





if __name__== '__main__':
    download(items())
