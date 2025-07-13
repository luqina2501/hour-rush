def is_legit(state = "////////////////////////////////////"):
    length = len(state)
    if length != 36:
        print(f"Invalid size: {length}")
        return False
    
    str = list(state) # muttable

    for i in range(36):
        ch = state [i]
        if ch == 'a' or ch == 'b':
            if i - 1 < 0 or str[i - 1] != '/':
                return False
            str[i - 1] = ch
        
        elif ch == 'c':
            if i - 6 < 0 or str[i - 6] != '/':
                return False
            str[i - 6] = '2'
        
        elif ch == 'm':
            if i - 2 < 0:
                return False
            for k in range (i - 2, i):
                if i - 2 < 0 or any(str[k] != '/' for k in range(i - 2, i)):
                    return False
            str[i - 1] = '3'
            str[i - 2] = '3'

        elif ch == 'n':
            if i -  12 < 0:
                return False
            for k in range (i - 12, i, 6):
                if i - 12 < 0 or any(str[k] != '/' for k in range(i - 12, i, 6)):
                    return False
            str[i - 6] = '3'
            str[i - 12] = '3'
    return True

def is_goal(state = "////////////////////////////////////"):
    return (state[17] == 'a')

expanded_node = 0
def expand(state = "////////////////////////////////////"):
    ++expanded_node
    succs = []
    coss = []

    if not is_legit(state):
        return succs, coss
    
    types = {
        'a': {'cost': 2, 'dir': 'h'},
        'b': {'cost': 2, 'dir': 'h'},
        'c': {'cost': 2, 'dir': 'v'},
        'm': {'cost': 3, 'dir': 'h'},
        'n': {'cost': 3, 'dir': 'v'}
    }

    for i in range(36):
        char = state[i]
        if char not in types:
            continue
        
        cost = types[char]['cost']
        dir = types[char]['dir']

        if dir == 'h':
            head = i + 1
            tail = i - cost
            # forward
            if head < 36 and state[head] == '/' and head // 6 == i // 6:
                tmp = list(state)
                tmp[head] = char
                tmp[i] = '/'
                new_state = "".join(tmp)
                if is_legit(new_state):
                    succs.append(new_state)
                    coss.append(cost)
            # backward
            if tail >= 0 and state[tail] == '/' and tail // 6 == i // 6:
                tmp = list(state)
                tmp[i - 1] = char
                tmp[i] = '/'
                new_state = "".join(tmp)
                if is_legit(new_state):
                    succs.append(new_state)
                    coss.append(cost)
        if dir == 'v':
            head = i + 6
            tail = i - cost * 6
            # down
            if head < 36 and state[head] == '/' and head % 6 == i % 6:
                tmp = list(state)
                tmp[head] = char
                tmp[i] = '/'
                new_state = "".join(tmp)
                if is_legit(new_state):
                    succs.append(new_state)
                    coss.append(cost)
            # up
            if tail >= 0 and state[tail] == '/' and tail % 6 == i % 6:
                tmp = list(state)
                tmp[i - 6] = char
                tmp[i] = '/'
                new_state = "".join(tmp)
                if is_legit(new_state):
                    succs.append(new_state)
                    coss.append(cost)

    return succs, coss