import os
from collections import defaultdict
import math
import operator


def loadDataSet(dir, dirNum):
    tempI = 0
    baseLocation = r'C:\Users\wangj\Downloads\after'  # 文件输出位置
    resultList = []
    secondLocation = baseLocation + '\\' + dir
    secondContent = os.listdir(secondLocation)  # 读取子目录
    for filename in secondContent:
        name = secondLocation + '\\' + filename  # 文件名
        tempFile = open(name, encoding='utf-8', mode='r')
        tempLine = tempFile.read()  # 获取内容
        resultList.append(tempLine.split(' '))  # 把拆分过的列表放入resultList
        print('get content ', tempI, ': ', name)
        tempI += 1
        if tempI >= dirNum / 2:
            break
    return resultList


def select(listWords):
    # 获取词频
    doc_feq = defaultdict(int)
    for l in listWords:
        for i in l:
            doc_feq[i] += 1
    # 缩小范围，控制在前400个关键词
    doc_feq = dict(sorted(doc_feq.items(), key=operator.itemgetter(1), reverse=True)[0:400])
    # 获取TF值————tf = ni,j / sum for k(nk,j)
    word_tf = {}
    for i in doc_feq:
        word_tf[i] = doc_feq[i] / sum(doc_feq.values())
    # 获取IDF————idfi = ln(D/j:ti∈dj)
    doc_num = len(listWords)
    word_idf = {}  # 存储每个词的idf
    word_doc = defaultdict(int)  # 存储包含该词的文档数
    for i in doc_feq:  # 获取出现该词的文档数
        for j in listWords:
            if i in j:
                word_doc[i] += 1
    for i in doc_feq:  # 获取IDF
        word_idf[i] = math.log(doc_num / (word_doc[i] + 1))  # 默认底数为e
    # 计算TF*IDF
    word_tf_idf = {}
    for i in doc_feq:
        word_tf_idf[i] = word_tf[i] * word_idf[i]
    # 排序
    dict_select = sorted(word_tf_idf.items(), key=operator.itemgetter(1), reverse=True)
    return dict_select


if __name__ == '__main__':
    dirList = []
    dirContent = []
    outPath = r'C:\Users\wangj\Downloads\tf_idf'
    # 获取子文件夹名称、文件数量
    for filename in os.listdir(r'C:\Users\wangj\Downloads\after'):
        dirList.append(filename)
    for dirName in dirList:
        dirContent.append(len(os.listdir('C:\\Users\\wangj\\Downloads\\after\\' + dirName)))
    # 建立词袋模型
    for i in range(len(dirList)):
        thisList = loadDataSet(dirList[i], dirContent[i])
        tf_idf = select(thisList)
        print(len(tf_idf))
        path = outPath+'\\'+dirList[i]+'.txt'
        tempFile = open(path,mode='w',encoding='utf-8')
        for i in tf_idf:
            tempStr = i[0] + ' ' + str(i[1])+'\n'
            tempFile.write(tempStr)
        tempFile.close()
