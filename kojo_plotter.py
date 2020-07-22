from matplotlib import pyplot as plt
import sqlite3

conn = sqlite3.connect('Kojo_simulations.db')
minutes = 5
c = conn.cursor()

c.execute('''
SELECT * FROM two_workers_waits ORDER BY cnt_simulations
''')
dict_graph = {}

all_ = c.fetchall()

for t,cnt_sim,_,_,_ in all_:
    if cnt_sim not in dict_graph:
        dict_graph[cnt_sim] = []
    dict_graph[cnt_sim].append(t)
x = dict_graph.keys()
y = [len([True for wait_time in dict_graph[k] if wait_time >= minutes])/len(dict_graph[k])for k in dict_graph]
plt.plot(x,y,'b',label='2 workers')

c.execute('''
SELECT * FROM three_workers_waits ORDER BY cnt_simulations
''')
dict_graph = {}

all_ = c.fetchall()

for t,cnt_sim,rush_l,normal_l,p in all_:
    if cnt_sim not in dict_graph:
        dict_graph[cnt_sim] = []
    dict_graph[cnt_sim].append(t)
    r_l = rush_l
    n_l = normal_l
    prop=p
x = dict_graph.keys()
y = [len([True for wait_time in dict_graph[k] if wait_time >= minutes])/len(dict_graph[k])for k in dict_graph]
plt.plot(x,y,'r',label='3 workers')
plt.legend()
plt.title("Cantidad de simulaciones y por ciento de clientes q esperaron \nmás de 5 minutos con rush_EX: {} min y normal_EX: {} min\n con p: {}".format(r_l/60,n_l/60,prop))
plt.show()

