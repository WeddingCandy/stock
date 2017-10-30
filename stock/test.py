#coding:utf8
import pandas as pd
import numpy as np
from EmQuantAPI import *
import datetime
import csv
from sqlalchemy import create_engine,types
import pymysql



#data = c.manualactivate("mxq0001", "gm251515")

#OPEN
#调用登录函数（激活后使用，不需要用户名密码）
loginResult = c.start()
#设置下载数据的区间
tradedate_list = c.tradedates("2017-10-20", "2017-10-26").Dates
#tradedate_list = ["20071231", "20081231", "20091231", "20101231", "20111231", "20121231", "20131231", "20141231", "20151231","20161231"]
#这是得到当前的A股代码-----test B股,total num = 100
secID_list = c.sector("2000033013","2017-06-30").Codes #,"20170630"
#下载数据
table = pd.DataFrame(index=secID_list, columns=tradedate_list)#use pandas.DataFrame
for dt in tradedate_list:
    data1 = c.css(secID_list, "TOTALSHARE", "ReportDate="+dt)#merge?????
    data2 = c.css(secID_list, "PE,PEG,PB,EV", "ReportDate="+ dt,"PredictYear=2017")
    for stk in data2.Codes:  #for-cycle to write data into table
        table.loc[stk,dt] = data2.Data[stk][1]#The index of dataframe
table.index.names = ["secID"]# para name
logoutResult = c.stop()

#保存为csv文件到桌面
table.to_csv('test5.csv')
#保存到mysql数据库
engine= create_engine("mysql+pymysql://root:112233@localhost/east",echo = False)
table.to_sql("test5", engine, if_exists="replace", index=True, dtype={'secID':types.CHAR(12)})
