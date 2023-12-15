stop_use = []
with open("stop_words.txt", 'r', encoding='utf-8') as file_stop:
    for line in file_stop:
        item = line.strip().split(' ')
        stop_use.append(item[0])

print(stop_use)