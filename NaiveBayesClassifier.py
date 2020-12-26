import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics


def getDataSet(filePath):
    dirList = os.listdir(filePath)
    trainClass = []
    trainList = []
    testClass = []
    testList = []
    # 获取训练集、测试集
    for i in dirList:
        secondPath = filePath + '\\' + i
        secondList = os.listdir(secondPath)
        tempInt = 0
        maxInt = len(secondList) / 2
        for j in secondList:
            # file = open(secondPath + '\\' + j, mode='r', encoding='utf-8')
            # tempStr = file.read()
            # tempStr = tempStr.replace('\n', '')
            # tempList = tempStr.split(' ')
            # tempInt += 1
            # if tempInt >= maxInt:
            #     testList.append(tempList)
            #     testClass.append(i)
            # else:
            #     trainList.append(tempList)
            #     trainClass.append(i)
            file = open(secondPath + '\\' + j, mode='r', encoding='utf-8')
            tempStr = file.read()
            tempStr = tempStr.replace('\n', '')
            tempInt += 1
            if tempInt >= maxInt:
                testList.append(tempStr)
                testClass.append(i)
            else:
                trainList.append(tempStr)
                trainClass.append(i)
        print('add', i, 'to list')
    return trainList, trainClass, testList, testClass



if __name__ == '__main__':
    # 获取所有字符集、类型向量
    listTrain, trainClasses, listTest, TestClasses = getDataSet(filePath=r'C:\Users\wangj\Downloads\after')
    # 获取TF-IDF值
    tf = TfidfVectorizer(max_df=0.5)
    trainFeatures = tf.fit_transform(listTrain)
    testFeatures = tf.transform(listTest)
    # 分类器
    clfMNB = MultinomialNB().fit(trainFeatures, trainClasses)
    # 预测
    predictedMNB = clfMNB.predict(testFeatures)
    # 准确度
    accuracy = metrics.accuracy_score(TestClasses,predictedMNB)
    print('accuracy:',accuracy)
    recall = metrics.recall_score(TestClasses,predictedMNB,average=None)
    print('recall:',recall)
