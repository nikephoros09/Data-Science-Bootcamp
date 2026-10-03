import sys
import timeit

def loop_way(email_list):
    res = []
    for email in email_list:
        if email.endswith('@gmail.com'):
            res.append(email)
    return res

def compr_way(email_list):
    return [email for email in email_list if email.endswith('@gmail.com')]


def map_way(email_list):
    return list(filter(None, map(lambda email: email if email.endswith('@gmail.com') else None, email_list)))

def filter_way(email_list):
    return list(filter(lambda x: x.endswith('@gmail.com'), email_list))

if __name__ == '__main__':
    res = None
    all_emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
                  'anna@live.com', 'philipp@gmail.com'] * 5
    the_way = sys.argv[1]
    loops = int(sys.argv[2])
    setup = f"from __main__ import loop_way, compr_way, map_way, filter_way\nall_emails = {all_emails}"
    if the_way == 'loop':
        res = timeit.timeit('loop_way(all_emails)', setup=setup, number=loops)
    elif the_way == 'comprehension':
        res = timeit.timeit('compr_way(all_emails)', setup=setup, number=loops)
    elif the_way == 'map':
        res = timeit.timeit('map_way(all_emails)', setup=setup, number=loops)
    elif the_way == 'filter':
        res = timeit.timeit('filter_way(all_emails)', setup=setup, number=loops)
    print(res)


