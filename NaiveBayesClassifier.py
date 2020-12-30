import os
import time
import numpy as np
from collections import defaultdict


class Corpus(object):
    def __init__(self, data, path):
        self.tags = defaultdict(int)
        self.vocabs = set()
        self.docs = data
        self.tfidf_path = path

        self.build_vocab()
        self.v_l = len(self.vocabs)  # 字典大小
        self.d_l = len(self.docs)  # 文档数

        print('Corpus inited!')

    # 生成词典，使用之前生成的tf-idf
    def build_vocab(self):
        fileList = os.listdir(self.tfidf_path)
        for fileName in fileList:
            file = open(self.tfidf_path + '\\' + fileName, mode='r', encoding='utf-8')
            while True:
                tempLine = file.readline()
                tempLine = tempLine.rstrip('\n')
                if not tempLine:
                    break
                tempList = tempLine.split(' ')
                self.vocabs.add(tempList[0])
                self.tags[fileName.split('.')[0]] += 1
            file.close()
        self.vocabs = list(self.vocabs)
        print('vocabs done! length =', len(self.vocabs))

    # 生成词袋模型
    def generate_bow(self):
        self.bow = np.zeros([self.d_l, self.v_l])
        for i in range(self.d_l):
            for word in self.docs[i][1]:
                if word in self.vocabs:
                    self.bow[i, self.vocabs.index(word)] += 1
        print('bow generated!')

    # 生成tf-idf矩阵
    def generate_tfidf(self):
        self.generate_bow()
        self.tfidf = np.zeros([self.d_l, self.v_l])
        dictTFIDF = {}

        fileList = os.listdir(self.tfidf_path)
        for fileName in fileList:
            file = open(self.tfidf_path + '\\' + fileName, mode='r', encoding='utf-8')
            while True:
                tempLine = file.readline()
                tempLine = tempLine.rstrip('\n')
                if not tempLine:
                    break
                tempList = tempLine.split(' ')
                if dictTFIDF.get(tempList[0], -1) == -1:
                    dictTFIDF[tempList[0]] = float(tempList[1])
            file.close()

        for idx in range(self.d_l):
            for word in self.docs[idx][1]:
                if word in self.vocabs:
                    self.tfidf[idx, self.vocabs.index(word)] = dictTFIDF.get(word)
        print('tf-idf generated!')

    # 计算idx
    def get_idx(self, sentence):
        bow = np.zeros([1, self.v_l])
        for word in sentence:
            if word in self.vocabs:
                bow[0, self.vocabs.index(word)] += 1
        return bow


class NBayes(Corpus):
    def __init__(self, data, path):
        super(NBayes, self).__init__(data, path)
        self.y_prob = {}
        self.c_prob = None
        self.feature = None

    def train(self):
        print('start training')
        print('start generate tf-idf')
        self.generate_tfidf()
        self.feature = self.tfidf

        for tag in self.tags:
            self.y_prob[tag] = float(self.tags[tag]) / self.d_l
        self.c_prob = np.zeros([len(self.tags), self.v_l])
        z = np.zeros([len(self.tags), 1])

        for idx in range(self.d_l):
            tid = list(self.tags.keys()).index(self.docs[idx][0])
            self.c_prob[tid] += self.feature[idx]
            z[tid] = np.sum(self.c_prob[tid])

        self.c_prob /= z

    def predict(self, target):
        words = target
        idx = self.get_idx(words)

        tag, score = None, -1
        for (p_c, y) in zip(self.c_prob, self.y_prob):
            tmp = np.sum(idx * p_c * self.y_prob[y])

            if tmp > score:
                tag = y
                score = tmp
        return tag, 1 - score


def getDataSet(filePath):
    dirList = os.listdir(filePath)
    trainList = []
    testList = []
    # ---------
    # debug_count = 0
    # 获取训练集、测试集
    for i in dirList:
        # ---------
        # if debug_count == 3:
        #     break
        # debug_count = 1
        # secondDebug = 0
        # ---------
        secondPath = filePath + '\\' + i
        secondList = os.listdir(secondPath)
        tempInt = 0
        maxInt = len(secondList) / 2
        for j in secondList:
            # ---------
            # secondDebug += 1
            # if secondDebug >= 50:
            #     break
            # ---------
            file = open(secondPath + '\\' + j, mode='r', encoding='utf-8')
            tempStr = file.read()
            file.close()
            tempStr = tempStr.replace('\n', '')
            tempList = tempStr.split(' ')
            tempInt += 1
            if tempInt >= maxInt:
                testList.append((i, tempList))
            else:
                trainList.append((i, tempList))
        print('add', i, 'to list')
    # return trainList, testList, dirList
    return trainList, testList, dirList


if __name__ == '__main__':
    startime = time.time()
    print('start reading! time', startime)
    # 获取所有字符集、类型向量
    trainList, testList, typeList = getDataSet(filePath=r'C:\Users\wangj\Downloads\after')
    print('loading complete! time', time.time() - startime)
    # 获取TF-IDF值
    nb = NBayes(trainList, path=r'C:\Users\wangj\Downloads\tf_idf')
    nb.train()
    print('training complete! time', time.time() - startime)
    # 预测
    correct = {}
    incorrect = {}
    total = {}
    results = {}
    for i in typeList:
        correct[i] = 0
        incorrect[i] = []
        total[i] = 0
        results[i] = 0
    for idx in range(len(testList)):
        result, possible = nb.predict(target=testList[idx][1])
        if result == testList[idx][0]:
            correct[result] += 1
            # print('correct!', result, testList[idx][0])
        else:
            incorrect[testList[idx][0]].append(result)
            # print('incorrect!', result, testList[idx][0])
        results[result] += 1
        total[testList[idx][0]] += 1
    # 生成精确率、召回率
    allCorrect = 0
    totalNum = 0
    for i in typeList:
        allCorrect += correct[i]
        totalNum += total[i]
        print('Precision for', i, ':', correct[i] / results[i])
    print('total Precision :', correct[i] / results[i])
    allCorrect = 0
    totalNum = 0
    for i in typeList:
        allCorrect += correct[i]
        totalNum += total[i]
        print('Recall for', i, ':', correct[i] / total[i])
    print('total Recall :', correct[i] / total[i])
    # 结束
    endtime = time.time()
    print('finish! time', endtime - startime)
