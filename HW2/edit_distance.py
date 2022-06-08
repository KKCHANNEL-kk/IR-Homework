def editDistance(s1,s2):
    m = [[0 for j in range(len(s2)+1)] for i in range(len(s1)+1)]
    for i in range(1,len(s1)+1):
        m[i][0] = i
    for j in range(1,len(s2)+1):
        m[0][j] = j
    
    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            if(s1[i-1] == s2[j-1]):
                m[i][j] = min(m[i-1][j]+1,m[i][j-1]+1,m[i-1][j-1])
                # 删除 插入 复制
            else:
                m[i][j] = min(m[i-1][j]+1,m[i][j-1]+1,m[i-1][j-1]+1)
                # 删除 插入 替换
    
    return m[len(s1)][len(s2)]
    
def show(s1,s2):
    print('{} and {} \'s edit disdance is {}'.format(s1,s2,editDistance(s1,s2)))


show('business','buisness')
show('committee','commitee')
show('conscious','concious')
show('definitely','definately')
show('fluorescent','florescent')
show('forty','fourty')
show('government','goverment')
show('idiosyncrasy','idiosyncracy')
show('immediately','immediatly')
show('millennium','millenium')
show('noticeable','noticable')
show('tendency','tendancy')
show('truly','truely')
show('weird','wierd')
show('privilege','privledge')