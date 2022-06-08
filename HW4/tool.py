import math
import jieba


def getDocList(path):
    '''
    读取文档集文件，返回文档list
    '''
    with open(path, 'r',encoding='utf-8-sig') as f:
        docList = f.readlines()
        return docList

def vecDot(vec1,vec2): 
    '''
    计算两个向量的点积
    '''
    i=0
    j=0
    len_i = len(vec1)
    len_j = len(vec2)
    dot_value = 0
    while i<len_i and j<len_j:
        if(vec1[i][0]==vec2[j][0]):
            dot_value += vec1[i][1]*vec2[j][1]
            i+=1
            j+=1
        elif vec1[i][0]<vec2[j][0]:
            i += 1
        elif vec1[i][0]>vec2[j][0]:
            j += 1
    return dot_value

def vecLen(vec):
    '''
    计算向量的空间长度
    '''
    len_value = 0
    for item in vec:
        len_value += item[1]**2
    
    return math.sqrt(len_value)

def calSimilarity(doc1,doc2):
    '''
    计算两个tf-idf文档向量的余弦相似度
    '''
    dot = vecDot(doc1,doc2)
    len_doc1 = vecLen(doc1)
    len_doc2 = vecLen(doc2)
    # cosine similarity = a.b / |a|*|b|
    return round(dot/(len_doc1*len_doc2),2)

def getTopK(doc,k):
    '''
    从文档相似度的得分列表中获取前k位
    '''
    doc_score = doc.copy()
    topK = []
    for i in range(k):
        max_index = 0
        max_score = 0
        for j in range(len(doc_score)):
            if doc_score[j]>max_score:
                max_score = doc_score[j]
                max_index = j
        topK.append((max_index,max_score))
        doc_score[max_index] = -1
    return topK
    
def getStopwords(path):
    '''
    读取停用词列表
    '''
    with open(path, 'r', encoding='utf-8') as f:
        stopword_list = [word.strip('\n') for word in f.readlines()]
    return stopword_list

def clean_cn_str(str,stopword_list):
    '''
    为中文字符串分词后去停用词，返回中文分词列表
    '''
    result = []
    word_list = jieba.lcut(str.strip('\n'))
    for word in word_list:
        if word not in stopword_list:
            result.append(word)
    return result
