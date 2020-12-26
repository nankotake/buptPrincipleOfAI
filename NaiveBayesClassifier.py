import os

if __name__ == '__main__':
    tfidf = []
    tfidfPath = r'C:\Users\wangj\Downloads\tf_idf'
    dirList = os.listdir(tfidfPath)
    #  读入TF-IDF词频
    for i in dirList:
        tempDict = {}
        filename = tfidfPath + '\\' + i
        file = open(filename,mode='r',encoding='utf-8')
        while 1:
            line = file.readline()

