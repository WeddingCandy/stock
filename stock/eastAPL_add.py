#coding:utf8
import pandas as pd
import numpy as np
from EmQuantAPI import *
import datetime
import csv
from sqlalchemy import create_engine,types
import pymysql

#OPEN
#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start()
#设置新增下载数据的区间
attrlist_add=[ "MV","EV"]#"DIVIDENDYIELD",
list = ['first']#初始化table的第一列，后drop除去
tradedate_list = [ "20141231", "20151231","20161231"]#获取数据的时间区间
year = [] #获取时间区间的年份，此处暂时不涉及年份去重
for yr in range(len(tradedate_list)):
    year.append( tradedate_list[yr][0:4])
#total num = 100
secID_list = c.sector("2000033013","20170101").Codes #,"20170630"
#构建tables
tables =pd.DataFrame(index=secID_list, columns=list)
#获取数据1
"""for dt in range(len(tradedate_list)):
    data = c.css(secID_list, "DIVIDENDYIELD", "ReportDate="+tradedate_list[dt],"Year="+year[dt]) #
    for stk in data.Codes:
        tables.loc[stk,tradedate_list[dt]] = data.Data[stk][0]"""
#获取数据2
for i in range(len(attrlist_add)):
    table = pd.DataFrame(index=secID_list, columns=tradedate_list)
    for dt in tradedate_list:
        data2 = c.css(secID_list, "MV,EV","TradeDate="+dt )
        for stk in data2.Codes:
            table.loc[stk, dt] = data2.Data[stk][i]
    tables = pd.concat([tables,table],axis=1,join="inner")
tables.index.names = ["secID"]  # para name
#剔除第一列初始列
tables.drop('first',axis=1, inplace=True)#  去掉第一列
#tables.rename(columns={'A':'a', 'B':'b', 'C':'c'}, inplace = True)
#获取变量“时间+名称”
namelist=[]
for atrr in attrlist_add:
    for year in tradedate_list:
        namelist.append(year+atrr)
tables.columns = namelist
date =  datetime.datetime.now().strftime('%Y-%m-%d')

#保存为csv文件到工作环境
tables.to_csv('%s.csv' % (date) )
tables.to_csv('clustertest.csv')
#参数为append下是新增记录
"""
#新数据插入到mysql数据库
engine= create_engine("mysql+pymysql://root:112233@localhost/east",echo = False)
tables.to_sql('%s.csv' % (date), engine, if_exists="replace", index=True, dtype={'secID':types.CHAR(12)})
logoutResult = c.stop()
"""
#SQL= 'alter table clustertest add (20141231MV double,	20151231MV double,	20161231MV double,	20141231EV double,	20151231EV  double,20161231EV double);'