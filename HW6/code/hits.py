from numpy import *
set_printoptions(suppress=True)

edges = [(0,1),(0,3),(1,4),(1,5),(3,6),(6,0),(6,2),(7,2),(7,5),(8,2)]
n = 9
web_graph = [[0 for i in range(n)] for i in range(n)]

for edge in edges:
    u=edge[0]
    v=edge[1]
    web_graph[u][v]=1

web_graph = array(web_graph)
ggT = dot(web_graph,web_graph.T)
gTg = dot(web_graph.T,web_graph)

h = array([1 for i in range(n)]).reshape(n,1)
a = array([1 for i in range(n)]).reshape(n,1)

h = h/h.sum()
a = a/a.sum()

err = 1
while err>0.0001:
    h_new = dot(ggT,h)
    a_new = dot(gTg,a)
    h_new = h_new/h_new.sum()
    a_new = a_new/a_new.sum()
    err = max(abs((h_new-h)).sum(),abs((a_new-a)).sum())
    h = h_new
    a = a_new

print('h:\n',h)
print('a:\n',a)

