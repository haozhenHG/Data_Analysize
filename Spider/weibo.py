import requests
import csv
import pandas as pd
import jieba
import wordcloud
# 保存文件
f = open('weibodata.csv','w',encoding='utf-8-sig',newline='')
csvwb = csv.DictWriter(f,fieldnames=['昵称','地区','性别','评论'])
csvwb.writeheader()


def getcontents(Maxid):
    # 发送请求
    headers ={
        # cookie  常用于检测是否有登录账号
        'cookie':'XSRF-TOKEN=wZ8bECpJlgJyRbWSyefxAaDp; SCF=AlZTrvx4aEpcEtUeDb6sIc9mpN0rLfEhGfC97di_e2wRzIMhcDuaF6bGoW2H7ieTyz_scbvU_tjjE-Imn60dbBg.; SUB=_2A25KJp01DeRhGeBG7VEU9S7MyDiIHXVpXZD9rDV8PUNbmtAGLVH7kW9NRhJk6IB8WfV1VqQziyFdnAS3bxt6KRuI; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Av0xCkDDaiHBZ_nrFgJkx5JpX5KzhUgL.FoqRSoefSK57e0B2dJLoIEDzxEH8Sb-4BEHWBCH8SCHWxC-RBEH8SCHFxC-RSCH8SEHFBbHWxh54ehet; ALF=02_1732934246; WBPSESS=ajNkZa2PhdxrC0PPuU_zQFWFnZvPXbkCDhnBhExo1_W2n6PXRguOlwl2-22iNACZpnAxXZJu9DWzw6KBwWt5mpNMiJUxB0G4cYXXMBg3P6mB78-DWEEcUVbIUx0rCGZexw0aMiAQLntpouyF18cekg==',
        # 用户代理 表示浏览器/设备的基本身份信息
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }
    # 请求网址
    url ='https://weibo.com/ajax/statuses/buildComments'

    data={
        'is_reload': '1',
        'id': '5094848836666976',
        'is_show_bulletin': '2',
        'is_mix': '0',
        'max_id':Maxid,
        'count': '20',  # 固定不变
        'uid': '3261134763',
        'fetch_level': '0',
        'locale': 'zh-CN'

    }

    # 发送请求
    response = requests.get(url=url,params=data,headers=headers)

    # 获取响应json数据
    json_data = response.json()

    # print(json_data)

    # 字典取值
    data_list = json_data['data']

    for index in data_list:
        # print(index)
        # 提取性别信息
        sex = index['user']['gender']
        if sex == 'f':
            gender = '女'
        elif sex =='m':
            gender = '男'
        else:
            gender = '保密'
        # 提取具体内容
        dit ={
            '昵称':index['user']['screen_name'],
            '地区':index['source'].replace('来自',''),
            '评论':index['text_raw'],
            '性别':gender,
        }
        print(dit)
        csvwb.writerow(dit)
    # 获取下一页maxid
    maxid = json_data['max_id']
    return maxid

max_id = ''
for page in range(1,21):
    print(f'正在采集第%d页的数据'%page)
    max_id = getcontents(Maxid=max_id)



