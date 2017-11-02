# -*- coding: utf-8 -*-
from scipy import spatial
from scipy.cluster.hierarchy import linkage ,fcluster,fclusterdata,dendrogram
from sklearn.cluster import KMeans,estimate_bandwidth
from sklearn.decomposition import PCA
from sklearn.decomposition import FactorAnalysis
from sklearn.externals import joblib
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import time
#从mysql导入数据
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='112233', db='east')
cursor = conn.cursor() #创建游标
#dataset_tmp = cursor.fetchall() #元祖
sql = "select * from clustertest"
df = pd.read_sql(sql,conn,index_col="secID") #df.drop('secID',axis=0,inplace=True)
cursor.close()
conn.close()

normalized_df = preprocessing.normalize(df)
normalized_df_pd = pd.DataFrame(normalized_df)




"""
num_cluster = 3

#nuwMat =FactorAnalysis(n_components=2).fit_transform(df) #FA降维
nuwMat = PCA(n_components=2).fit_transform(df) #PCA降维
kmeans = KMeans(n_clusters=num_cluster,random_state=0).fit(nuwMat) #聚类计算

center = kmeans.cluster_centers_ #获取聚类中心点坐标
df_center = pd.DataFrame(center, columns=['x', 'y'])
labels = kmeans.labels_
#绘图
axes=plt.subplot()
axes.plot(df_center['x'],df_center['y'],'ro')
axes.plot(nuwMat[:, 0], nuwMat[:, 1],'bo')
plt.show()

"""
"""
num_cluster = 5

#nuwMat =FactorAnalysis(n_components=2).fit_transform(df) #FA降维
#nuwMat = PCA(n_components=2).fit_transform(df) #PCA降维
kmeans = KMeans(n_clusters=num_cluster,random_state=0).fit(df) #聚类计算
labels = kmeans.labels_.tolist()
center = kmeans.cluster_centers_ #获取聚类中心点坐标

labels = kmeans.labels_
km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()
df_center = pd.DataFrame(center, columns=['x', 'y'])
#绘图
axes=plt.subplot()
axes.plot(df_center['x'],df_center['y'],'ro')
axes.plot(nuwMat[:, 0], nuwMat[:, 1],'bo')
plt.show()
"""

#层次聚类
matData = df.as_matrix()
distance = spatial.distance.pdist(matData)
linkresult = linkage(distance,method='average',metric='euclidean')
fcluster(linkresult,t=0.99,criterion='inconsistent',depth=2,R=None,monocrit=None)#这个需要先计算linkage，再出结果
dendrogram(linkresult,get_leaves=False,show_leaf_counts=False)#这个可以绘制出树形图




if __name__ == '__main__':
    print("step 1: load data...")
    dataSet = PCA(n_components=2).fit_transform(normalized_df)  # PCA降维
    #dataSet = np.array(df)
    for k in range(2, 10):
        clf = KMeans(n_clusters=k)  # 设定k  ！！！！！！！！！！这里就是调用KMeans算法
        s = clf.fit(dataSet)  # 加载数据集合
        numSamples = len(dataSet)
        centroids = clf.labels_
        print(centroids, type(centroids))  # 显示中心点
        print(clf.inertia_)# 显示聚类效果
        mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']# 画出所有样例点 属于同一分类的绘制同样的颜色
        for i in range(numSamples): # markIndex = int(clusterAssment[i, 0])
            plt.plot(dataSet[i][0], dataSet[i][1], mark[clf.labels_[i]])  # mark[markIndex])
            mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']# 画出质点，用特殊图型
        centroids =clf.cluster_centers_
        for i in range(k):
            plt.plot(centroids[i][0], centroids[i][1], mark[i], markersize=12)# print centroids[i, 0], centroids[i, 1]
        plt.show()

        """
        # 简单打印结果
        r1 = pd.Series(centroids).value_counts()  # 统计各个类别的数目
        r2 = pd.DataFrame(centroids)  # 找出聚类中心
        r = pd.concat([r2, r1], axis=1)  # 横向连接(0是纵向), 得到聚类中心对应的类别下的数目
        r.columns = list(normalized_df_pd.columns) + [u'类别数目']  # 重命名表头
        print(r)
        # 详细输出原始数据及其类别
        r = pd.concat([normalized_df_pd, pd.Series(clf.labels_, index=normalized_df_pd.index)], axis=1)
        # 详细输出每个样本对应的类别
        r.columns = list(normalized_df_pd.columns) + [u'聚类类别']  # 重命名表头
        outputfile = r'C:\Users\Chans\PycharmProjects\stock\data_type.xls'
        r.to_excel(outputfile)  # 保存结果  """

