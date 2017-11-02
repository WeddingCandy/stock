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
#tradedate_list = c.tradedates("2017-10-20", "2017-10-26").Dates


attrlist=["PE" ,"PB","PS"]
list = ['first']
tradedate_list = [ "20141231", "20151231","20161231"]
#这是得到当前的A股代码-----test B股,total num = 100
secID_list = c.sector("2000033013","20170101").Codes #,"20170630"
#下载数据
tables =pd.DataFrame(index=secID_list, columns=list)
for i in range(0,3):
    table = pd.DataFrame(index=secID_list, columns=tradedate_list)  # use pandas.DataFrame
    for dt in tradedate_list:
        data2 = c.css(secID_list, "PE ,PB,PS","TradeDate="+dt,type="6" )
        for stk in data2.Codes:#for-cycle to write data into table
            table.loc[stk, dt] = data2.Data[stk][i]  # The index of dataframe
    tables = pd.concat([tables,table],axis=1,join="inner")
tables.index.names = ["secID"]  # para name
tables.drop('first',axis=1, inplace=True)#  去掉第一列
#tables.rename(columns={'A':'a', 'B':'b', 'C':'c'}, inplace = True)
namelist=[]
for atrr in attrlist:
    for year in tradedate_list:
        namelist.append(year+atrr)
tables.columns = namelist






#保存为csv文件到桌面
tables.to_csv('clustertest.csv')
#保存到mysql数据库
engine= create_engine("mysql+pymysql://root:112233@localhost/east",echo = False)
tables.to_sql("clustertest", engine, if_exists="replace", index=True, dtype={'secID':types.CHAR(12)})
logoutResult = c.stop()
