# 建立文档列表
with open(r'text\HW1.txt', encoding='utf-8-sig') as f:
    doc_list = f.readlines()

term_index = {}
for doc_id, doc in enumerate(doc_list):
    # 进行文本预处理（去除冒号，转换为小写）
    doc = doc.lower().replace(':',' ')
    # 分词，准备录入词表
    terms = doc.split()
    for term in terms:
        if term not in term_index:
            term_index[term] = [0]
        term_index[term][0] = term_index[term][0] + 1
        term_index[term].append(doc_id)

term_index = sorted(term_index.items(), key=lambda x: (x[1][0],x[0]),reverse=True)

for term in term_index:
    print(term[0], term[1][0], term[1][1:])
    
with open(r'text\inverted_index.txt', 'w', encoding='utf-8') as f:
    for term in term_index:
        f.write(term[0] + ' ' + str(term[1][0]) + ' ')
        for doc_id in term[1][1:]:
            f.write(str(doc_id) + ' ')
        f.write('\n')
