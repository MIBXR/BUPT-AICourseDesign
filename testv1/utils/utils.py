import jieba.posseg as pseg

stop_use = []
with open("stop_words.txt", 'r',encoding='utf-8') as file_stop:
    for line in file_stop:
        item = line.strip().split(' ')
        stop_use.append(item[0])

def load_dict(filename):
    dict = {}
    with open(filename, 'r', encoding='utf8') as f:
        for line in f:
            item = line.strip().split(' ')
            dict[item[0]] = int(item[1])
    print(dict)
    f.close()
    return dict

def save_dict(dict, filename):
    with open(filename, 'w', encoding='utf8') as f:
        for key in dict:
            f.write(key + ' ' + str(dict[key]) + '\n')
    f.close()

def save_sub_word_bank(list, threshold, filename):
    sum = 0
    with open(filename, 'w', encoding='utf8') as f:
        i = 0
        while i < len(list) and list[i][1] >= threshold:
            f.write(list[i][0] + ' ' + str(list[i][1]) + '\n')
            sum += list[i][1]
            i += 1
        del list[i:]
    f.close()

    return sum,list

def append_dict(key, value, filename):
    with open(filename, 'a', encoding='utf8') as f:
        f.write(key + ' ' + str(value) + '\n')
    f.close()

def update_dict(content, dict):

    words = pseg.cut(content)

    for word, flag in words:
        if flag=='n' and len(word)!=1 and word not in stop_use:
            if word in dict.keys():
                dict[word] += 1
            else:
                dict[word] = 1
    return dict

def update_word_bank(word_bank, sub_word_bank):  # sub_word_bank是list形式

    for each in sub_word_bank:
        if each[0] in word_bank.keys():
            word_bank[each[0]] += each[1]
        else:
            word_bank[each[0]] = each[1]
    return word_bank

def open_file(txt_path):
    """

    :param path: 文本文件路径
    :return: 文本文件内容，如果打不开则返回None
    """
    try:
        with open(txt_path, 'r', encoding='GBK') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(txt_path, 'r', encoding='UTF-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(txt_path, 'r', encoding='ANSI') as f:
                    content = f.read()
            except Exception:
                content = None
                print("pass")
    return content