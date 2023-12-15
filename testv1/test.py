import jieba
import jieba.analyse
import jieba.posseg as pseg

import os
import time
from utils import utils
import math


train_set_path = "D:\\A temp\\RGZN-1\\ML文本分类\\测试集"

#  得到训练集文件的路径组织
A = []
for _, __, ___ in os.walk(train_set_path):
    #print(_)
    #print(__)
    #print(___)
    A.append([_, __, ___])

#  获取文章类型列表
article_types = A[0][1]
print("Involved types:")
print(article_types)

#  读入训练好的模型（即统计数据）
word_numbers = utils.load_dict("word_numbers.txt")  # 读入训练集词库中词汇数目的统计信息
article_numbers = utils.load_dict("article_numbers.txt")  # 读入训练集文章数目统计信息
word_bank = utils.load_dict("word_bank.txt")  # 读入词库,每一项包括词汇和频数
sub_word_bank = [utils.load_dict(article_types[i]+".txt") for i in range(len(article_types))]  # 读入子词库,每一项包括词汇和在特定类别出现的频数
jieba.load_userdict("word_bank.txt")  # 将词库载入jieba

#  计算先验
priors = dict()
for type in article_numbers.keys():
    if type != "total":
        priors[type] = int(article_numbers[type])/int(article_numbers["total"])

#  初始化统计指标
features = [[0, 0, 0, 0] for i in range(len(article_types))]  # 每行的四个数据分别代表TP、FP、FN、TN


#  定义分类器
def judge(dict, article_types, word_numbers, priors, word_bank, sub_word_bank):
    scores = [0 for i in range(len(article_types))]

    V = len(word_bank)
    # print("V",V)

    #  先验得分
    for i in range(len(article_types)):
        scores[i] += math.log(priors[article_types[i]])

    for word in dict.keys():
        # print(word)
        #  先检查这个单词是否在词库里，不在则不纳入考虑
        if word not in word_bank.keys():
            continue

        times = dict[word]
        for i in range(len(article_types)):
            #  获取子词库的总词数
            total_times = word_numbers[article_types[i]]
            #  获取这个单词在特定子词库出现的频数
            if word in sub_word_bank[i]:
                sub_times = sub_word_bank[i][word]
            else:
                sub_times = 0
            #  add-one smoothing方式计算得分
            scores[i] += times * math.log((sub_times + 1)/(total_times+V))

    max_score = scores[0]
    max_i = 0
    for i in range(1, len(article_types)):
        if scores[i] > max_score:
            max_score = scores[i]
            max_i = i

    # print(article_types[max_i])
    return max_i

#  定义更新统计数据的函数
#  每行的四个数据分别代表TP、FP、FN、TN
def update_features(prediction, real, features):
    if prediction == real:
        for i in range(len(article_types)):
            if i == prediction:
                features[i][0] += 1
            else:
                features[i][3] += 1
    else:
        for i in range(len(article_types)):
            if i == prediction:
                features[i][1] += 1
            elif i == real:
                features[i][2] += 1
            else:
                features[i][3] += 1

result = [[0 for j in range(len(article_types))] for i in range(len(article_types))]

#  测试
for i in range(0,len(article_types)):

    article_type = article_types[i]
    for txt in A[i+1][2]:

        D = dict()  # 用来记录单篇文章的提取词信息
        txt_path = train_set_path + "\\" + article_type + "\\" + txt
        print(txt_path)

        content = utils.open_file(txt_path)
        if content == None:
            continue
        D = utils.update_dict(content, D)

        prediction = judge(D, article_types, word_numbers, priors, word_bank, sub_word_bank)

        result[i][prediction] += 1

        print("prediction: "+article_types[prediction]+", answer: "+article_types[i])
        update_features(prediction, i, features)


#  打印测试结果
    total_TP = 0
    total_FP = 0
    total_FN = 0
    total_TN = 0

    for i in range(len(article_types)):
        print("Type: "+article_types[i])


        TP = features[i][0]
        FP = features[i][1]
        FN = features[i][2]
        TN = features[i][3]

        # print(TP, FP, FN, TN)

        P = TP/(TP + FP) if (TP + FP) > 0 else 0
        R = TP/(TP + FN) if (TP + FN) > 0 else 0
        FM = 2*P*R/(P+R) if (P+R) > 0 else 0

        print("Precision: " + str(P))
        print("Recall: " + str(R))
        print("F1-Measure: " + str(FM))
        print()

        total_TP += TP
        total_FP += FP
        total_FN += FN
        total_TN += TN

    total_P = total_TP/(total_TP + total_FP) if (total_TP + total_FP) > 0 else 0
    total_R = total_TP/(total_TP + total_FN) if (total_TP + total_FN) > 0 else 0
    total_FM = 2*total_P*total_R/(total_P + total_R) if (total_P + total_R) > 0 else 0

    print("Totol:")
    print("Precision: " + str(total_P))
    print("Recall: " + str(total_R))
    print("F1-Measure: " + str(total_FM))

for i in result:
    print(i)

