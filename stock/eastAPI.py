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
#设置下载数据的区间
tradedate_list = c.tradedates("2016-01-01", "2017-10-15").Dates
#tradedate_list = ["20071231", "20081231", "20091231", "20101231", "20111231", "20121231", "20131231", "20141231", "20151231","20161231"]
#这是得到当前的A股代码
secID_list = c.sector("2000032254", "20170630").Codes
#下载数据
table = pd.DataFrame(index=secID_list, columns=tradedate_list)
for dt in tradedate_list:
    data = c.css(secID_list, "YOYOP", "ReportDate="+dt)
    for stk in data.Codes:
        table.loc[stk,dt] = data.Data[stk][0]
table.index.names = ["secID"]
logoutResult = c.stop()

#保存为csv文件到桌面
table.to_csv('yoyop.csv')
#保存到mysql数据库
engine= create_engine("mysql+pymysql://root:123456@localhost/emdata",echo = False)
table.to_sql("yoyop", engine, if_exists="replace", index=True, dtype={'secID':types.CHAR(12)})