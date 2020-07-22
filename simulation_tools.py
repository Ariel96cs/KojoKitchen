import numpy as np
exponential_gen = lambda l: -(1/l)*np.log(1-np.random.random())#np.random.exponential
uniform_gen = lambda a,b: a+(b-a)*np.random.random()
binomial_gen = np.random.binomial


def find_i(value, arr):
    for i, val in enumerate(arr):
        if val == value:
            return i
    return -1


def is_rush_hour(current_time, interval1, interval2):
    return (current_time < interval1[1] and current_time >= interval1[0]) or \
           (current_time < interval2[1] and current_time >= interval2[0])

