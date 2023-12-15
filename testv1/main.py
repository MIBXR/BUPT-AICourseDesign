import os
from utils import utils


threshold = 10

# D:\\Projects\\Pycharm\\JB\\复旦测试集
train_set_path = "D:\\A temp\\RGZN-1\\ML文本分类\\训练集"
times_record_name = "times.txt"

A = []

#  得到训练集文件的路径组织
for _, __, ___ in os.walk(train_set_path):
    #print(_)
    #print(__)
    #print(___)
    A.append([_, __, ___])

#  初始化记录训练结果的数据结构
word_bank = dict()  # 词库
word_total = 0  # 词库单词数目
article_total = 0  # 训练使用的文章数目

#  训练（即开始分词并统计）
for i in range(0, len(A[0][1])):    # 子文件夹组成的列表
    sub_word_bank = dict()
    sub_article_total = 0

    article_type = A[0][1][i]
    print("Type: "+A[0][1][i])
    for txt in A[i+1][2]:
        txt_path = train_set_path + "\\" + article_type + "\\" + txt
        print(txt_path)

        content = utils.open_file(txt_path)
        if content == None:
            continue
        else:
            # 统计有效文章数
            article_total += 1
            sub_article_total += 1

        sub_word_bank = utils.update_dict(content, sub_word_bank)

    sub_word_bank = sorted(sub_word_bank.items(), key=lambda d: d[1], reverse=True)
    print(sub_word_bank)

    dict_name = article_type + ".txt"
    sub_word_total, sub_word_bank= utils.save_sub_word_bank(sub_word_bank, threshold, dict_name)

    word_total += sub_word_total

    utils.append_dict(article_type, sub_word_total, "word_numbers.txt")
    utils.append_dict(article_type, sub_article_total, "article_numbers.txt")

    utils.update_word_bank(word_bank, sub_word_bank)
    print("*"*50)

utils.save_dict(word_bank, "word_bank.txt")  # 写入词库,每一项包括词汇和频数
utils.append_dict("total", word_total, "word_numbers.txt")
utils.append_dict("total", article_total, "article_numbers.txt")
