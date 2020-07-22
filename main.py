from Kojo_simulator import Kojo_simulator as ks
import sqlite3
from tqdm import tqdm
from time import sleep


conn = sqlite3.connect('Kojo_simulations.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS two_workers_waits
(waits real, cnt_simulations real,rush_EX real,normal_EX real,sushi_prop real)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS three_workers_waits
(waits real, cnt_simulations real,rush_EX real,normal_EX real,sushi_prop real)
''')
#
# c.execute('''
# CREATE TABLE IF NOT EXISTS cnt_simulations
# (cnt_workers real, cnt_simulations real)
# ''')

conn.commit()
print(">>>Inserte el valor esperado del tiempo en horario pico, en minutos...")
EX_rush = int(input())*60
print(">>>Inserte el valor esperado del resto del tiempo, en minutos...")
EX_normal = int(input())*60
print(">>>Inserte la razón de elección por los clientes entre sushi y sándwich ...")
p = float(input())
rush_lambda,normal_lambda = 1/EX_rush,1/EX_normal

print('>>>Espere mientras realizamos el cómputo...')
sleep(0.5)
for cnt_simulations in tqdm(range(1,100)):
    c.execute('DELETE FROM three_workers_waits WHERE cnt_simulations={}'.format(cnt_simulations))
    c.execute('DELETE FROM two_workers_waits WHERE cnt_simulations={}'.format(cnt_simulations))
    for _ in range(cnt_simulations):
        # (una lista de tiempos de espera en la cola, una lista de la cantidad de clientes que atendio cada trabajador)
        clients_waits_in_seconds,worker_clients3 = ks(try_extra_worker=True, easy_lambda=normal_lambda,
                                                      rush_hour_lambda=rush_lambda,p=p)
        for i in clients_waits_in_seconds:
            c.execute('INSERT INTO three_workers_waits VALUES ({},{},{},{},{})'.format(i,cnt_simulations,EX_rush,
                                                                                    EX_normal,p))
        # c.executemany('INSERT INTO three_workers_waits VALUES (?)',clients_waits_in_seconds)

    for _ in range(cnt_simulations):
        # (una lista de tiempos de espera en la cola, una lista de la cantidad de clientes que atendio cada trabajador)
        clients_waits_in_seconds,worker_clients2 = ks(easy_lambda=normal_lambda,rush_hour_lambda=rush_lambda,p=p)
        for i in clients_waits_in_seconds:
            c.execute('INSERT INTO two_workers_waits VALUES ({},{},{},{},{})'.format(i,cnt_simulations,EX_rush,
                                                                                  EX_normal,p))
        # c.executemany('INSERT INTO two_workers_waits VALUES (?)',clients_waits_in_seconds)

    # c.execute('SELECT * FROM cnt_simulations ORDER BY cnt_workers')
    # elements = c.fetchall()
    # w2 = (2,elements[0][1]+cnt_simulations)
    # w3 = (3,elements[1][1]+cnt_simulations)
    # c.execute('UPDATE cnt_simulations SET cnt_simulations={} WHERE cnt_workers={}}'.format(w2[1],w2[0]))
    # c.execute('UPDATE cnt_simulations SET cnt_simulations={} WHERE cnt_workers={}}'.format(w3[1],w3[0]))
    conn.commit()
sleep(0.5)
print(">>>Listo")


