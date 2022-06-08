def position_cmp(p1,p2,k_distance,type):
    if type == -1:
        return p1-p2>=-k_distance and 0>=p1-p2
    elif type==1:
        return p1-p2<=k_distance and 0<=p1-p2
    elif type == 0:
        return (p1-p2>=-k_distance and 0>=p1-p2) or (p1-p2<=k_distance and 0<=p1-p2)
        


def positional_intersect(list1:list,list2:list,k_distance:str) -> list:
    """
    取两个列表的邻近交集
    """
    answer = []
    i = 1
    j = 1
    len_i = len(list1)-1
    len_j = len(list2)-1
    type = 0
    k_dis = 0
    if k_distance[0] == '+':
        type = 1
        k_dis = int(k_distance[1:])
    elif k_distance[0] == '-':
        type = -1
        k_dis = int(k_distance[1:])
    else:
        type = 0
        k_dis = int(k_distance)
            
    while i <= len_i and j <= len_j:
        if list1[i][0] == list2[j][0]:
            doc_id = list1[i][0]
            position1 = list1[i][1]
            position2 = list2[j][1]
            # pp1 = 1
            # pp2 = 1
            # len_pp1 = position1[0]
            # len_pp2 = position2[0]
            # l = []
            # while pp1<=len_pp1:
            #     while pp2<=len_pp2:
            #         if position_cmp(position1[pp1],position2[pp2],k_dis,type):
            #             l.append(position2[pp2])
            #         elif position2[pp2]>position1[pp1]:
            #             break
            #         pp2+=1
            #     for ps in l:
            #         answer.append([doc_id,position1[pp1],ps])
            #     pp1+=1
            for pp1 in position1[1:]:
                for pp2 in position2[1:]:
                    if(position_cmp(pp1,pp2,k_dis,type)):
                        answer.append([doc_id,pp1,pp2])
            
            i+=1
            j+=1

        elif list1[i][0] < list2[j][0]:
            i += 1
        else:
            j += 1
    return answer


# 建立文档列表
with open(r'text\HW2.txt', encoding='utf-8-sig') as f:
    doc_list = f.readlines()

term_index = {}
for doc_id, doc in enumerate(doc_list):
    # 进行文本预处理（去除冒号，转换为小写）
    doc = doc.lower().replace(':',' ')
    # 分词，准备录入词表
    terms = doc.split()
    doc_term_pos = {}
    for term_pos, term in enumerate(terms):
        if term not in doc_term_pos:
            doc_term_pos[term] = [0]
        doc_term_pos[term].append(term_pos)
        doc_term_pos[term][0]+=1
    
    for term in doc_term_pos:
        if term not in term_index:
            term_index[term] = [0]
        term_index[term].append([doc_id,doc_term_pos[term]])
        term_index[term][0]+=doc_term_pos[term][0]

def show(word1,word2,k_distance):
    print(word1,':',term_index[word1],'\n')
    print(word2,':',term_index[word2],'\n')
    print('{}和{}的临近{}交集：'.format(word1,word2,k_distance))
    print(positional_intersect(term_index[word1],term_index[word2],k_distance))
    print('\n')


show('ranking','filtering','-4')
show('ranking','filtering','-5')
show('ranking','filtering','-6')
show('ranking','filtering','-7')
show('heterogeneous','learning','+2')
show('recommendation','bias','2')