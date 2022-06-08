# 全局变量统计
skip_times = 0
cmp_times = 0


def initCnt():
    global skip_times, cmp_times
    skip_times = 0
    cmp_times = 0


class Node:
    value = None    # 词频或文档doc_id
    skip_index = None

    def __init__(self, value: int, skip_index=None):
        self.value = value
        self.skip_index = skip_index

    def hasSkip(self):
        return self.skip_index != None

    def __repr__(self):
        return str(self.value)


def intersect(list1: list, list2: list) -> list:
    """
    取两个列表的交集
    """
    global skip_times, cmp_times
    answer = []
    i = 1
    j = 1
    len_i = list1[0].value
    len_j = list2[0].value
    answer.append(Node(0))
    while i <= len_i and j <= len_j:
        if list1[i].value == list2[j].value:
            answer.append(int(list1[i].value))
            answer[0].value = answer[0].value+1
            i += 1
            j += 1
        elif list1[i].value < list2[j].value:
            i += 1
        else:
            j += 1
        cmp_times += 1
    return answer


def intersect_with_skips(list1: list, list2: list) -> list:
    """
    取两个列表的交集，使用跳表指针
    """
    global skip_times, cmp_times
    answer = []
    i = 1
    j = 1
    len_i = list1[0].value
    len_j = list2[0].value
    answer.append(Node(0))
    while i <= len_i and j <= len_j:
        if list1[i].value == list2[j].value:
            answer.append(int(list1[i].value))
            answer[0].value = answer[0].value+1
            i += 1
            j += 1
            cmp_times += 1
        elif list1[i].value < list2[j].value:
            cmp_times += 1
            while list1[i].hasSkip():
                if(list1[list1[i].skip_index].value <= list2[j].value):
                    i = list1[i].skip_index
                    skip_times += 1
                    cmp_times += 1
                else:
                    cmp_times += 1
                    break
            i += 1
            # if list1[i].hasSkip() and list1[list1[i].skip_index].value <= list2[j].value:
            #     while(list1[i].hasSkip() and list1[list1[i].skip_index].value <= list2[j].value):
            #         i = list1[i].skip_index
            #         skip_times+=1
            #         cmp_times+=1

        else:
            cmp_times += 1
            # if list2[j].hasSkip() and list2[list2[j].skip_index].value <= list1[i].value:
            #     while (list2[j].hasSkip() and list2[list2[j].skip_index].value <= list1[i].value):
            #         j = list2[j].skip_index
            #         skip_times+=1
            #         cmp_times+=1
            while list2[j].hasSkip():
                if(list2[list2[j].skip_index].value <= list1[i].value):
                    j = list2[j].skip_index
                    skip_times += 1
                    cmp_times += 1
                else:
                    cmp_times += 1
                    break
            j += 1
    return answer


with open(r'text\inverted_index_Ex1.txt', encoding='utf-8') as f:
    inverted_index = f.readlines()

term_index = {}
for term_row in inverted_index:
    term_row = term_row.split()
    term_name = term_row[0]
    term_freq = Node(int(term_row[1]))
    term_doc_list = term_row[1:]
    term_doc_list = [Node(int(i)) for i in term_doc_list]
    term_index[term_name] = term_doc_list

term_index['a'][1].skip_index = 5
term_index['a'][5].skip_index = 9
term_index['a'][9].skip_index = 13
term_index['a'][13].skip_index = 17

a_b_normal = intersect(term_index['a'], term_index['b'])
print("a_b_normal: ", a_b_normal)
print("skip_times: ", skip_times)
print("cmp_times: ", cmp_times, '\n')
initCnt()

a_c_normal = intersect(term_index['a'], term_index['c'])
print("a_c_normal: ", a_c_normal)
print("skip_times: ", skip_times)
print("cmp_times: ", cmp_times, '\n')
initCnt()

a_b_skip = intersect_with_skips(term_index['a'], term_index['b'])
print("a_b_skip: ", a_b_skip)
print("skip_times: ", skip_times)
print("cmp_times: ", cmp_times, '\n')
initCnt()

a_c_skip = intersect_with_skips(term_index['a'], term_index['c'])
print("a_c_skip: ", a_c_skip)
print("skip_times: ", skip_times)
print("cmp_times: ", cmp_times, '\n')
initCnt()
