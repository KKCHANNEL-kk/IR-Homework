import jieba

def show_index(term_index,word):
    print("Word:"+word)
    if word in term_index:
        result = term_index[word]
        print("Length:"+str(result[0]))
        print("Search Result:"+str(result[1:]))
    else:
        print("Not Found")
    print('\n')


with open(r'text\HW3.txt', encoding='utf-8-sig') as f:
    doc_list = f.readlines()

jieba.load_userdict(r'text\dict.txt')
term_index = {}
token_cnt = 0
for doc_id, doc in enumerate(doc_list):
    tokens = jieba.lcut_for_search(doc)
    # print(terms)
    for token in tokens:
        token_cnt += 1
        if(token not in term_index):
            term_index[token] = [0]
        term_index[token][0] += 1
        term_index[token].append(doc_id)

print("Token Counts:",token_cnt)
print('Term Counts:',len(term_index),'\n')

search_items = ['迁移','迁移学习','推荐','深度学习','隐私','跨领域','跨域']
for item in search_items:
    show_index(term_index,item)

with open(r'text\inverted_index.txt','w',encoding='utf-8-sig') as f:
    for term,posting_list in term_index.items():
        f.write(term+' ')
        for doc_id in posting_list:
            f.write(str(doc_id)+' ')
        f.write('\n')