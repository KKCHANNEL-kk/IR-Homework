import math
from tracemalloc import stop
import tool


doc_list = tool.getDocList(r'text\HW4_2.txt')
stopwords = tool.getStopwords(r'text\cn_stopwords.txt')
N = len(doc_list)
term_dict = {}  # 形如 {term1:id1,...}
term_df = []    # 形如 term_df[id1] = df1
term_tf = []    # 形如 term_tf[doc_id] = [{term_id:tf},...]
term_id = 0     # 建立term-id映射的全局id

for doc in doc_list:
    raw_terms = tool.clean_cn_str(doc,stopwords)
    tf = {}
    for term in raw_terms:
        if term not in term_dict:
            term_dict[term] = term_id
            term_id = term_id+1
            term_df.append(0)
        id = term_dict[term]
        if term not in tf:
            tf[id] = 0
        tf[id] = tf[id]+1
    term_tf.append(tf)
    for id in tf.keys():
        term_df[id] = term_df[id]+1
        
tf_idf = []
for doc_id,doc in enumerate(term_tf):
    doc_vec = []
    for item in doc.items():
        id = item[0]
        tf = item[1]
        idf = math.log(N/term_df[id],10)
        doc_vec.append((id,round((1+math.log(tf,10))*idf,2)))
    doc_vec.sort()
    tf_idf.append(doc_vec)

similarity = [[-1 for i in range(N)] for j in range(N)]

for i in range(N):
    for j in range(N):
        if similarity[i][j]!=-1:
            continue
        similarity[i][j] = tool.calSimilarity(tf_idf[i],tf_idf[j])
        similarity[j][i] = similarity[i][j]
        
for doc_id,doc_score in enumerate(similarity[:10]):
    print("=============================================")
    print('doc_%d: %s\n' %(doc_id,doc_list[doc_id][:-1]))
    top3 = tool.getTopK(doc_score,3)
    for i in range(3):
        print("Similar No.%d is doc_%d: %s" %(i+1,top3[i][0],doc_list[top3[i][0]][:-1]))
        print("Similarity: %s" %top3[i][1])
        list1= tool.clean_cn_str(doc_list[doc_id],stopwords)
        list2 = tool.clean_cn_str(doc_list[top3[i][0]],stopwords)
        print("Same in: ",[term for term in list1 if term in list2])
        print()

        
        