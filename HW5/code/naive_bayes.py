import pkuseg
import pandas as pd
import math
import jieba
import tool

def trainNB(label,terms,docs,_class):
    '''
    传入docs（pandas的DataFrame格式），对应label列的列名，terms列的列名，分类列表。
    返回每个分类的先验概率prior，每个分类的条件概率condprob。
    '''
    # 用于计算prior
    doccnt_class = {}
    doccnt_all = 0
    prior = {}
         
    # 用于计算condprob
    wordcnt_unique = 0 # 文档集中不重复的词的数量
    wordcnt_class = {} # 文档集中每一类的词频数
    vocabulary_class_cnt = {} # 文档集中每个词在每一类的出现频率
    condprob = {} # 文档集中每个词在每一类的条件概率
    
    for c in _class:
        doccnt_class[c] = 0
        wordcnt_class[c] = 0

    for index,row in docs.iterrows():
        doccnt_class[row[label]] = doccnt_class[row[label]]+1
        doccnt_all += 1 # iterrows遍历的每一行是一个文档
        
        words = row[terms]

        for word in words:
            if word not in vocabulary_class_cnt:
                wordcnt_unique = wordcnt_unique + 1
                vocabulary_class_cnt[word] = {}
                condprob[word] = {}
                for c in _class:
                    vocabulary_class_cnt[word][c] = 0 # word 在 c 类文档中出现的词频
                    # condprob[word][c] = 0 # word 在 c 类文档中出现的条件概率
                    
            vocabulary_class_cnt[word][row[label]] = vocabulary_class_cnt[word][row[label]]+1
            wordcnt_class[row[label]] = wordcnt_class[row[label]]+1
    
    for c in _class:
        prior[c] = doccnt_class[c]/doccnt_all
        for word,word_class_cnt in vocabulary_class_cnt.items():
            condprob[word][c] = (word_class_cnt[c]+1)/(wordcnt_class[c]+wordcnt_unique)
            
    return prior,condprob
    

def predictNB(words,prior,condprob,_class):
    '''
    输入预测用的分词列表words，训练集的先验分布prior和条件概率conddprob,分类列表_class。
    返回预测结果。
    '''
    words = set(words)
    score = {}
    for c in _class:
        score[c] = math.log(prior[c])
        for word in words:
            if word in condprob:
                score[c] += math.log(condprob[word][c])
    
    maxNB = score[_class[0]]
    maxC = _class[0]
    for c in _class:
        if score[c]>maxNB:
            maxNB = score[c]
            maxC = c
    
    return (maxC,maxNB)

def filterFeature(fea_dict,label,terms):
    return [term for term in terms if term in fea_dict[label]]

if __name__ == '__main__':
    data = pd.read_csv('data/gwt_info.csv')
    stopwords = tool.getStopwords('data/cn_stopwords.txt')
    data['words'] = data.apply(lambda x: tool.clean_cn_str_jieba_search(str(x['title'])+' '+str(x['content']),stopwords),axis=1)

    _class = data['department'].unique()
    
    # 划分数据集，严谨一些可以进行随机划分
    train_docs = data[data['no']<20][['department','words']]
    test_docs = data[(data['no']<30) & (data['no']>=20)][['department','words']]
    
    prior,condprob = trainNB('department','words',train_docs,_class)
    test_docs['predict_nofea'] = test_docs.apply(lambda x: predictNB((x['words']),prior,condprob,_class),axis=1)
    test_docs['is_correct_nofea'] = test_docs.apply(lambda x: x['department']==x['predict_nofea'][0],axis=1)
    
    # 读取特征词集合
    mi = pd.read_csv('data/MI_result_jieba_search.csv')
    chi = pd.read_csv('data/CHI_result_jieba_search.csv')
    
    mi_fea = {}
    chi_fea = {}
    for c in _class:
        mi_fea[c] = list(mi[c].apply(lambda x:eval(x)[0]))
        chi_fea[c] = list(chi[c].apply(lambda x:eval(x)[0]))
    
    # 训练模型，预测分类
    train_docs['words_mi'] = train_docs.apply(lambda x: filterFeature(mi_fea,x['department'],x['words']),axis=1)
    train_docs['words_chi'] = train_docs.apply(lambda x: filterFeature(chi_fea,x['department'],x['words']),axis=1)
    
    prior_mi,condprob_mi = trainNB('department','words_mi',train_docs,_class)
    test_docs['predict_mi'] = test_docs.apply(lambda x: predictNB((x['words']),prior_mi,condprob_mi,_class),axis=1)
    test_docs['is_correct_mi'] = test_docs.apply(lambda x: x['department']==x['predict_mi'][0],axis=1)

    prior_chi,condprob_chi = trainNB('department','words_chi',train_docs,_class)
    test_docs['predict_chi'] = test_docs.apply(lambda x: predictNB((x['words']),prior_chi,condprob_chi,_class),axis=1)
    test_docs['is_correct_chi'] = test_docs.apply(lambda x: x['department']==x['predict_chi'][0],axis=1)
    
    # 计算准确率
    print('No Feature accuracy : %f' % test_docs['is_correct_nofea'].mean())
    print('MI Feature accuracy : %f' % test_docs['is_correct_mi'].mean())
    print('CHI Feature accuracy : %f' % test_docs['is_correct_chi'].mean())
    print('=================================================================')
    
    for c in _class:
        print('No Feature accuracy in class %s: %f' % (c,test_docs[test_docs['department']==c]['is_correct_nofea'].mean()))
        print('MI Feature accuracy in class %s: %f' % (c,test_docs[test_docs['department']==c]['is_correct_mi'].mean()))
        print('CHI Feature accuracy in class %s: %f' % (c,test_docs[test_docs['department']==c]['is_correct_chi'].mean()))
        print('=================================================================')
    
    # test_docs[['department','predict_nofea','predict_mi','predict_chi']].to_csv('data/test_docs_nofea_mi_chi.csv',encoding='utf-8-sig')