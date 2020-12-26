import os
import jieba

# 读取停止词
stopName = r'C:\Users\wangj\OneDrive\Code\AI\stop_words_ch.txt'
stopFile = open(stopName,mode='r',encoding='utf-8')
stopList = []
for i in stopFile.read():
    stopList.append(i)
stopFile.close()
# 保存数据所在的文件夹、文件名
dirList = []
dirContent = []
baseLocation = r'C:\Users\wangj\Downloads\thucnews'
afterLocation = r'C:\Users\wangj\Downloads\after'  # 文件输出位置
# 获取子文件夹名称
for filename in os.listdir(r'C:\Users\wangj\Downloads\thucnews'):
    dirList.append(filename)
# 获取子文件夹长度
for i in range(0, len(dirList)):
    dirContent.append(os.listdir(baseLocation + '\\' + dirList[i]))
# 保存分词
for i in dirList:
    secondLocation = baseLocation + '\\' + i  # 读取子目录
    sLAfter = afterLocation + '\\' + i  # 保存子目录
    for j in dirContent[dirList.index(i)]:
        # 读取文件
        print('open : ' + secondLocation + '\\' + j)
        file = open(secondLocation + '\\' + j, encoding='utf-8')
        tempStr = file.read().replace('\n', '')
        tempStr = tempStr.replace('　', '')
        # 去除回车、全角空格
        tempList = tempStr.split(' ')
        tempStr = ''.join(tempList)
        # 去除其他
        print(tempStr)
        jiebaList = jieba.cut(tempStr)
        result = []
        # 去除停止词
        print('jieba: ' + secondLocation + '\\' + j)
        for jie in jiebaList:
            if jie not in stopList:
                result.append(jie)
        # 输出
        if not os.path.exists(sLAfter):
            os.makedirs(sLAfter)
        toFile = open(sLAfter + '\\' + j, mode='w', encoding='utf-8')
        toFile.write(' '.join(result))
        toFile.close()
        print('saveTo: ' + sLAfter + '\\' + j)
        file.close()
