import sys
import timeit
from functools import reduce

def loop_way(n):
    total = 0
    for i in range(1, n+1):
        total += i * i
    return total

def reduce_way(n):
    return reduce(lambda sum, x: sum + x*x, range(1, n+1))

if __name__ == '__main__':
    func_name = sys.argv[1]
    loops = int(sys.argv[2])
    num = int(sys.argv[3])

    if func_name == 'loop':
        func = loop_way
    elif func_name == 'reduce':
        func = reduce_way
    print(func(num))
    # setup = f"from __main__ import func\nnum = {num}"

    # res = timeit.timeit('func(num)', setup=setup, number=loops)
    # print(res)
