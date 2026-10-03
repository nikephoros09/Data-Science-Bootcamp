import pstats

stats = pstats.Stats('profiling-cumulative.prof')

with open('pstats-cumulative.txt', 'w') as f:
    stats.sort_stats('cumulative').stream = f
    stats.print_stats(5)