#!/usr/local/bin/python3
# -*- coding: utf-8 -*- 
import os,re,sys,time
import subprocess,shlex
import math,random
import json
from pathlib import Path
import pandas as pd

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
#sys.stdin=open('in.txt','r')

current_path = os.getcwd()
target_path_head = os.path.expanduser('~/Workspace/Instagram/')
path_list = ['thecaratclub', '_mountainbikezone', 'ridecake', 'airpods_case_1']


new_order = ['id', 'created_at', 'post_host',  'text', 'likes_count', 'answers', 'owner.id', 'owner.is_verified', 'owner.profile_pic_url', 'owner.username']
new_order2 = ['id', 'created_at', 'post_host', 'label', 'logits', 'text', 'likes_count', 'answers', 'owner.id', 'owner.is_verified', 'owner.profile_pic_url', 'owner.username']

def get_comments(target_path='.'):
    ret = []
    comment_files = sorted(Path(target_path).glob('*comments.json'))
    for file in comment_files:
        with open(file, 'r') as f:
            j = json.load(f)
        for i in j:
            ret.append(i['text'])
    print(f'Totally {len(ret)} comments.')
    return ret


def save_to_file(sl, fname='text_only.txt'):
    with open(fname, 'w') as fout:
        for i in sl:
            fout.write(i.strip()+'\n')
    return

def timestamp_to_time(timestamp):
    from datetime import datetime
    dt_object = datetime.fromtimestamp(timestamp)
    print("dt_object =", dt_object)
    print("type(dt_object) =", type(dt_object))
    return dt_object

def get_100(f):
    with open(f, 'r') as fin:
        s = fin.readlines()
    s = sorted(s, key=lambda x: len(x), reverse=True)
    print(s[0])
    save_to_file(s[:100], fname='airpods_case_1_100.txt')
    pass



def get_json(target_path='.'):
    ret = []
    comment_files = sorted(Path(target_path).glob('*comments.json'))
    for file in comment_files:
        with open(file, 'r') as f:
            j = json.load(f)
        ret += j
    print(f'Totally {len(ret)} comments.')
    return ret


def main():
    # r = get_comments(target_path)
    # for i in range(5):
    #     print(r[i])
    # save_to_file(r, fname = Path(target_path).name+'.txt')
    data = []
    for i in path_list:
        j = get_json(os.path.join(target_path_head, i))
        for k in j:
            k['post_host'] = i
            k['text'] = k['text'].replace('\n', ' ')
        df = pd.json_normalize(j)
        data.append(df)

    merged = pd.concat(data)
    merged = merged[new_order]
    merged.to_csv('Instagram.csv', index=False, encoding='utf-8')
    save_to_file(merged['text'])

    df = pd.read_csv('Instagram.csv', header=0)
    df2 = pd.read_csv('Instagram4_output.txt', names=['label','logits','text'])
    merged2 = pd.concat([df, df2[['label','logits']]], axis=1)
    print(merged2)
    merged2 = merged2[new_order2]
    merged2.to_csv('Instagram2.csv', index=False, encoding='utf-8')
    # for i in range(len(merged)):
    #     merged[i]['label'] = df2.iloc[i]['label']
    #     merged[i]['logits'] = df2.iloc[i]['logits']
    pass

if __name__ == '__main__':
    main()
    