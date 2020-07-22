from simulation_tools import *
import sys


def Kojo_simulator(try_extra_worker=False,
                   easy_lambda=1/1000, rush_hour_lambda=1/100,p=0.5):
    '''
    El tiempo será medido en segundos a partir de la hora inicial definida.
    '''
    # calculamos los segundos de los tiempos más importantes
    close_time = 11 * 60 * 60
    min_rush1 = 90 * 60  # apartir de las 10:00 a 11:30
    max_rush1 = min_rush1 + 150 * 60
    rush_interval1 = (min_rush1, max_rush1)
    min_rush2 = 7 * 60 * 60
    max_rush2 = min_rush2 + 120 * 60
    rush_interval2 = (min_rush2, max_rush2)


    # Abrimos la tienda
    opened = True
    simulation_time = 0
    total_clients = 0

    # luego tengo que agregar en las rush hour al nuevo trabajador
    # y retirarlo cuando no lo sea
    worker_busy = [False, False]
    inf = sys.maxsize
    # ak guardamos la hora de salida del cliente del trabajador i
    worker_time_busy = [inf, inf, inf]
    # ak guardamos la cantidad de clientes q ha atendido el trabajador i
    worker_clients = [0, 0, 0]

    # ak guardamos los tiempos de llegada al restaurante
    street_queue = []

    # ak guardamos los tiempos de espera en la cola q será lo que estamos buscando
    left_client_queue = []

    # generamos el primer arribo
    arraive_time = exponential_gen(easy_lambda)

    # mientras que esté abierta la tienda o halla alguien trabajando
    while opened or any(worker_busy):

        # verificamos la próxima salida
        next_out_time = min(worker_time_busy)

        # si lo próximo q ocurre es q llega una persona y llega antes de que cerremos
        if arraive_time <= next_out_time and arraive_time < close_time:
            simulation_time = arraive_time
            total_clients += 1
            # lo ponemos momentáneamente en la cola
            street_queue.append(simulation_time)

            # preguntamos si hay al menos un cocinero vacío
            if not all(worker_busy):
                i = find_i(False, worker_busy)
                # el cocinero i pasa a estar ocupado
                worker_busy[i] = True
                worker_clients[i] += 1

                # se deja pasar al primer cliente de la cola
                # y generamos su tiempo de salida que depende de lo que pida
                generate_client_out(i, left_client_queue, simulation_time, street_queue, worker_time_busy,p)

            # si estamos en hora pico, generamos el proximo arribo con su lambda respectivo
            if is_rush_hour(simulation_time, rush_interval1, rush_interval2):
                arraive_time = simulation_time + exponential_gen(rush_hour_lambda)
                # print("Estamos en hora pico")

                # si queremos probar con un tercer trabajador y no lo hemos agregado
                if try_extra_worker and len(worker_busy) == 2:
                    worker_busy.append(False)
            else:
                # si esta no estamos en rush hour y
                # teniamos un tercer trabajador, y este no está haciendo nada

                if len(worker_busy) == 3 and not worker_busy[2]:
                    worker_busy.pop()

                arraive_time = simulation_time + exponential_gen(easy_lambda)

        # si lo próximo q ocurre es la salida de un cliente o
        # si ya cerró la tienda y todavia hay trabajadores ocupados
        # me muevo para la próxima salida
        elif (arraive_time > next_out_time) or (any(worker_busy) and not opened):
            i = find_i(next_out_time, worker_time_busy)
            simulation_time = next_out_time

            # si quedan personas en la cola
            if len(street_queue) > 0:
                # entramos al próximo cliente y generamos su tiempo de salida
                generate_client_out(i, left_client_queue, simulation_time, street_queue, worker_time_busy,p)
            else:
                # si no hay nadie en la cola
                worker_busy[i] = False
                worker_time_busy[i] = inf

        # si ya es hora de cerrar o no viene mas nadie antes de que cierre la tienda
        if simulation_time >= close_time or arraive_time >= close_time:
            # print('Estamos cerrando la tienda')
            opened = False

    return left_client_queue, worker_clients


def generate_client_out(i, left_client_queue, simulation_time, street_queue, worker_time_busy,p):
    left_client_queue.append(simulation_time - street_queue.pop(0))
    #                 simulamos que es lo que quiere el cliente si sandwish o sushi
    client_request_for_sushi = True if uniform_gen(0, 1) < p else False
    if client_request_for_sushi:
        worker_time_busy[i] = simulation_time + uniform_gen(5, 8) * 60
    else:
        worker_time_busy[i] = simulation_time + uniform_gen(3, 5) * 60