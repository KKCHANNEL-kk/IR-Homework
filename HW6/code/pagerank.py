from numpy import *
import random
web_graph = array([[0,1,1],[0,0,1],[0,1,0]])
teleportation_rate = 0.05

def calP(graph,rate):
    n = len(graph)
    result = []
    for vector in graph:
        p_vec = []
        cnt = 0
        for i in vector:
            cnt += i
        prob = 1/cnt
        for i in vector:
            if i !=0:
                p_vec.append((1-rate)*prob+rate/n)
            else:
                p_vec.append(rate/n)
        result.append(p_vec)
    return array(result)

P = calP(web_graph,teleportation_rate)
x = P[0]
err = 1
while err>0.0000001:
    x_new = dot(x,P)
    err = abs((x_new-x)).sum()
    x=x_new

print(x)