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

if __name__ == '__main__':
    all_emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
                  'anna@live.com', 'philipp@gmail.com'] * 5

    setup = f"from __main__ import loop_way, compr_way, map_way\nall_emails = {all_emails}"
    loops = 90_000
    loop_time = timeit.timeit('loop_way(all_emails)', setup=setup, number=loops)
    compr_time = timeit.timeit('compr_way(all_emails)', setup=setup, number=loops)
    map_time = timeit.timeit('map_way(all_emails)', setup=setup, number=loops)
    times = [loop_time, compr_time, map_time]
    shortest, middle, longest = sorted(times)

    if shortest == loop_time:
        print('it is better to use a loop')
    elif shortest == compr_time:
        print('it is better to use a list comprehension')
    elif shortest == map_time:
        print('It is better to use a map')
        
    print(f'{shortest} vs {middle} vs {longest}')
