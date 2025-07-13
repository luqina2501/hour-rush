import state_search as ss
import read_map as rm

maps = rm.load_all_maps()
succs, cost = ss.ucs(maps[3])

print(cost)
for succ in succs:
    print(succ)