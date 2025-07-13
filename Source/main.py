import state_search as ss
import state_logic as sl
import read_map as rm

import time
import tracemalloc

maps = rm.load_all_maps()

def benchmark_all_alg(map, file):
    algs = [
        ("IDS", ss.bfs),
        ("BFS", ss.bfs),
        ("UCS", ss.ucs),
        ("A*_", ss.a_star),
    ]

    for name, func in algs:
        sl.expanded_node = 0

        tracemalloc.start()
        start_time = time.time()

        path, cost = func(map)

        duration = time.time() - start_time
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        file.write(f"| `{map}` | {name} | {duration:.4f}s | {peak} B | {sl.expanded_node} |\n")


# Write to result.md

#with open("result.md", "w") as f:
#    f.write("| Map | Name | Runtime | Peak Memory Usage | Expanded Node |\n")
#    f.write("|-----|------|---------|-------------------|----------------|\n")
#    for map in maps:
#        benchmark_all_alg(map, f)

def i_hate_ids(map):
    tracemalloc.start()
    start_time = time.time()
    path, cost = ss.ids(map)
    duration = time.time() - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"| {map} | {duration:.4f}secs | {peak}B | {sl.expanded_node} |")

i_hate_ids(maps[6])