import pkuseg
import pandas as pd
import math
import jieba
import tool

def calculate_CHIsquare(label,terms,docs):
    vocabulary = {}
    _class = docs[label].unique()
    doccnt_class = {}
    for c in _class:
        doccnt_class[c] = 0
    doccnt_all = 0
    for index,row in docs.iterrows():
        words = list(set(row[terms]))
        for word in words:
            if word not in vocabulary:
                vocabulary[word] = {}
                for c in _class:
                    vocabulary[word][c] = 0 # word 在 c 类文档中出现的文档数
            vocabulary[word][row[label]] = vocabulary[word][row[label]]+1
        doccnt_class[row[label]] = doccnt_class[row[label]]+1
        doccnt_all += 1 # iterrows遍历的每一行是一个文档
        
    CHI = {}
    for c in _class:
        CHI[c] = []
        
    for word,word_class_doccnt in vocabulary.items():
        for c,doccnt in word_class_doccnt.items():
            n = doccnt_all
            n11 = doccnt    # word 在 c 类文档中出现的文档数，可能为0
            n01 = doccnt_class[c] - n11 # word 在 c 类文档中不出现的文档数, 即 c 类文档总数 - n11，可能为0
            n1_ = sum(word_class_doccnt.values()) # word 在所有文档中出现的文档数，不可能为0
            n10 = n1_ - n11 # word 在其他类文档中出现的文档数，即包含word但不属于 c 类的文档数，可能为0
            n00 = n - n1_ - n01 # 不包含word的其他类文档数，可能为0
            n0_ = n - n1_ # 所有文档（包含c类）中不包含word的文档数，可能为0
            n_1 = doccnt_class[c] # c 类文档总数，此例中不可能为0
            n_0 = doccnt_all - n_1 # 其他类文档总数，不可能为0
            chi = (n*(n11*n00-n01*n10)**2)/(n_1*n1_*n_0*n0_+1)
            # 分母+1做平滑处理
            CHI[c].append((word,round(chi,6)))

    for c in CHI.values():
        c.sort(key=lambda x:x[1],reverse=True)
    
    return CHI
    

def print_CHI_result(CHI):
    for cname,ccnt in CHI.items():
        print(cname,' Top 15: ',ccnt[:15])
        print('\n')

if __name__ == '__main__':
    data = pd.read_csv('data/gwt_info.csv')
    stopwords = tool.getStopwords('data/cn_stopwords.txt')
    data['words'] = data.apply(lambda x: tool.clean_cn_str_jieba_search(str(x['title'])+' '+str(x['content']),stopwords),axis=1)

    
    docs = data[data['no']<30][['department','words']] # 取出各类最近30条，作为特征选择的语料
    CHI = calculate_CHIsquare('department','words',docs)
    print_CHI_result(CHI)
    chidf = pd.DataFrame(CHI)
    # chidf.iloc[0:15].to_csv('data/CHI_result_jieba.csv',encoding='utf-8-sig')
    # chidf.iloc[0:15].to_csv('data/CHI_result_pkuseg.csv',encoding='utf-8-sig')
    chidf.iloc[0:15].to_csv('data/CHI_result_jieba_search.csv',encoding='utf-8-sig')