import pkuseg
import pandas as pd
import math
import jieba

def getStopwords(path):
    '''
    读取停用词列表
    '''
    with open(path, 'r', encoding='utf-8') as f:
        stopword_list = [word.strip('\n') for word in f.readlines()]
    return stopword_list

seg = pkuseg.pkuseg()

def clean_cn_str(str,stopword_list):
    '''
    为中文字符串分词后去停用词，返回中文分词列表
    '''
    result = []
    word_list = seg.cut(str.strip('\n'))
    for word in word_list:
        if word not in stopword_list:
            result.append(word)
    return result

def clean_cn_str_jieba(str,stopword_list):
    '''
    用jieba为中文字符串分词后去停用词，返回中文分词列表
    '''
    result = []
    word_list = jieba.lcut(str.strip('\n'))
    for word in word_list:
        if word not in stopword_list:
            result.append(word)
    return result

def clean_cn_str_jieba_search(str,stopword_list):
    '''
    用jieba_search模式为中文字符串分词后去停用词，返回中文分词列表
    '''
    result = []
    word_list = jieba.lcut_for_search(str.strip('\n'))
    for word in word_list:
        if word not in stopword_list:
            result.append(word)
    return result