import timeit

def loop_way(email_list):
    res = []
    for email in email_list:
        if email.endswith('@gmail.com'):
            res.append(email)
    return res

def compr_way(email_list):
    return [email for email in email_list if email.endswith('@gmail.com')]

if __name__ == '__main__':
    all_emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 
                  'anna@live.com', 'philipp@gmail.com'] * 5

    setup = f"from __main__ import loop_way, compr_way\nall_emails = {all_emails}"
    loops = 900_000
    loop_time = timeit.timeit('loop_way(all_emails)', setup=setup, number=loops)
    compr_time = timeit.timeit('compr_way(all_emails)', setup=setup, number=loops)

    if compr_time <= loop_time:
        print('it is better to use a list comprehension')
    else:
        print('it is better to use a loop')

    shortest, longest = sorted([loop_time, compr_time])
    print(f'{shortest} vs {longest}')