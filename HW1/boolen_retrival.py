def intersect(list1: list, list2: list) -> list:
    """
    取两个列表的交集
    """
    answer = []
    i = 1
    j = 1
    len_i = list1[0]
    len_j = list2[0]
    answer.append(0)
    while i <= len_i and j <= len_j:
        if list1[i] == list2[j]:
            answer.append(list1[i])
            answer[0] = answer[0]+1
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return answer


def union(list1: list, list2: list) -> list:
    """
    取两个列表的并集
    """
    answer = []
    i = 1
    j = 1
    len_i = list1[0]
    len_j = list2[0]
    answer.append(0)
    while i <= len_i and j <= len_j:
        if list1[i] == list2[j]:
            answer.append(list1[i])
            answer[0] = answer[0]+1
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            answer.append(list1[i])
            answer[0] = answer[0]+1
            i += 1
        else:
            answer.append(list2[j])
            answer[0] = answer[0]+1
            j += 1
    for doc_id in list1[i:]:
        answer.append(doc_id)
    for doc_id in list2[j:]:
        answer.append(doc_id)
    answer[0] = answer[0]+len(list1[i:])+len(list2[j:])
    return answer


def negate(list1: list, doc_len: int) -> list:
    """
    取反
    """
    answer = []
    i = 1
    len_i = list1[0]
    answer.append(doc_len-len_i)
    left_limit = 0
    while i <= len_i:
        for doc_id in range(left_limit, list1[i]):
            answer.append(doc_id)
        left_limit = list1[i]+1
        i += 1
    return answer


def multiIntersect(lists: list) -> list:
    """
    取多个列表的交集
    """
    lists.sort(key=lambda x: x[0])
    cmp_count = len(lists)
    if cmp_count == 1:
        return lists[0]
    else:
        answer = intersect(lists[0], lists[1])
    index = 2
    while index != cmp_count:
        answer = intersect(answer, lists[index])
        index += 1
    return answer


with open(r'text\inverted_index.txt', encoding='utf-8') as f:
    inverted_index = f.readlines()

term_index = {}
for term_row in inverted_index:
    term_row = term_row.split()
    term_name = term_row[0]
    term_freq = int(term_row[1])
    term_doc_list = term_row[1:]
    term_doc_list = [int(i) for i in term_doc_list]
    term_index[term_name] = term_doc_list

print('transfer AND learning:', intersect(
    term_index['transfer'], term_index['learning']))
print('transfer:', term_index['transfer'])
print('learning:', term_index['learning'], '\n')


print('transfer AND learning AND filtering:', multiIntersect(
    [term_index['transfer'], term_index['learning'], term_index['filtering']]))
print('transfer:', term_index['transfer'])
print('learning:', term_index['learning'])
print('filtering:', term_index['filtering'], '\n')

print('recommendation AND filtering:', intersect(
    term_index['recommendation'], term_index['filtering']))
print('recommendation:', term_index['recommendation'])
print('filtering:', term_index['filtering'], '\n')

print('recommendation OR filtering:', union(
    term_index['recommendation'], term_index['filtering']))
print('recommendation:', term_index['recommendation'])
print('filtering:', term_index['filtering'], '\n')


print('transfer AND NOT (recommendation OR filtering):', intersect(
    term_index['transfer'], negate(union(term_index['recommendation'], term_index['filtering']), 60)))
print('transfer:', term_index['transfer'])
print('NOT (recommendation OR filtering) :', negate(
    union(term_index['recommendation'], term_index['filtering']), 60))
