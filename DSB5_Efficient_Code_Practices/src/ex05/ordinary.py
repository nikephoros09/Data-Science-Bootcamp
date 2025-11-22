import sys
import resource

def dump_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines

if __name__ == '__main__':
    filename = sys.argv[1]

    usage_start = resource.getrusage(resource.RUSAGE_SELF)
    start_time = usage_start.ru_utime + usage_start.ru_stime

    lines = dump_lines(filename)
    for line in lines:
        pass

    usage_end = resource.getrusage(resource.RUSAGE_SELF)
    peak_memory_gb = usage_end.ru_maxrss / (1024 ** 2)
    end_time = usage_end.ru_utime + usage_end.ru_stime

    cpu_time = end_time - start_time
    print(f"Peak Memory Usage = {peak_memory_gb:.3f} GB")
    print(f"User Mode Time + System Mode Time = {cpu_time:.2f}s")