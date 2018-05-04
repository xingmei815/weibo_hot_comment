#!/usr/bing/python
# -*- coding: utf-8 -*-
import requests,time,os,sys,re
import json
import MySQLdb as mdb


reload(sys)
sys.setdefaultencoding('utf8')
host='127.0.0.1'

port_mysql=3306
user_mysql='root'
passwd_mysql='spider2018'
db_mysql='weib'

#获取卷与套餐的列表
def get_deallist():
    insert_data = []
    for row in range(1,600):
        http_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
        url = 'https://m.weibo.cn/api/comments/show?id=4233145060912663&page='+str(row)
        res = requests.get(url, headers=http_headers)
        html = json.loads(res.text)
        for voucherArr in html['data']["data"]:
            user_id=str(voucherArr["id"])
            comment=voucherArr["text"]
            creat_time = voucherArr["created_at"]
            insert_data.append([user_id,comment,creat_time])
        # 连接数据库同时进行批量插入
        con = None
        try:
            con = mdb.connect(host=host, port=port_mysql, user=user_mysql, passwd=passwd_mysql, db=db_mysql,
                              charset='utf8')
            cur = con.cursor()
            try:
                # 插入相关数据
                sql = "insert into weibo_comment(user_id, comment, creat_time) values(%s, %s, %s)"
                cur.executemany(sql, insert_data)
                con.commit()
            except:
                print insert_data
                print '-------',row
                pass
        finally:
            if con:
                # 无论如何，连接记得关闭
                con.close()


get_deallist()