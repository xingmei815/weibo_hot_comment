
#coding=utf-8
from selenium import webdriver
import time,os,re
import requests,time,os,sys,re
import json
import MySQLdb as mdb

browser = webdriver.Firefox()
host='127.0.0.1'
port_mysql=3306
user_mysql='root'
passwd_mysql='spider2018'
db_mysql='weib'

#-----提交表单的方式回车-----
browser.get('https://weibo.com/2551034310/GdUfM3Pqn?filter=hot&root_comment_id=0&type=comment#_rnd1525593056728')

#browser.find_element_by_id('kw').send_keys('selenium')
time.sleep(15)

temp_txt=0
#pageSource = browser.page_source
con = None
try:
    con = mdb.connect(host=host, port=port_mysql, user=user_mysql, passwd=passwd_mysql, db=db_mysql,
                      charset='utf8')
    cur = con.cursor()
    while 1:
        try:
            #browser.find_element_by_link_text(u'查看更多').click()
            browser.find_element_by_class_name('more_txt').click()
        except:
            pass
        js = "var q=document.documentElement.scrollTop=100000"
        browser.execute_script(js)
        time.sleep(3)
        #pageSource = browser.page_source
        #txt=re.findall(ur'：(.*?)<',pageSource)
        #for bro in txt:
        #    print len(txt),bro

        #if temp_txt!=txt[0] and len(temp_txt)>0:
        txt=''
        insert_data=''
        if  len(txt)-temp_txt > 80000:
            temp_txt = len(txt)
            try:
                sql = "insert into weibo_comment( comment) values(%s)"
                cur.executemany(sql, insert_data)
                con.commit()
            except:
                try:
                    txtName = "codingWord.txt"
                    f = file(txtName, "a+")
                    for bro in txt:
                        new_context = bro + '\n'
                        f.write(new_context)
                    f.close()
                except:
                    for bro in txt:
                        print len(txt), bro
        elif len(txt)>80220:
            for bro in txt:
                print len(txt), bro

finally:
    if con:
        # 无论如何，连接记得关闭
        con.close()
time.sleep(3000000)
#browser.quit()

