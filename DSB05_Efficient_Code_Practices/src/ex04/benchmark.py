import timeit
import random
from collections import Counter

#keys - numbers, values - count
def my_dictionary(items):
    num_n_count = {}
    for current in items:
        num_n_count[current] = num_n_count.get(current, 0) + 1
    return num_n_count

def my_top_ten(items):
    result = my_dictionary(items)
    top_num = sorted(result.items(), key=lambda x: x[1], reverse=True)[:10]
    return dict(top_num)

def counter_counts(items):
    return Counter(items)

def counter_top_ten(items):
    return Counter(items).most_common(10)

if __name__ == '__main__':
    data = [random.randint(0, 100) for i in range(10_000)]
    # setup = (
    #     f'from __main__ import my_dictionary, counter_counts, my_top_ten, counter_top_ten\ndata = {data}'
    # )

    # print('My function:', timeit.timeit('my_dictionary(data)', setup=setup, number=1))
    # print('Counter:', timeit.timeit('counter_counts(data)', setup=setup, number=1 ))
    # print('My top:', timeit.timeit('my_top_ten(data)', setup=setup, number=1))
    # print('Counter\'s top:', timeit.timeit('counter_top_ten(data)', setup=setup, number=1))
    print(my_top_ten(data))
    print(counter_top_ten(data))
