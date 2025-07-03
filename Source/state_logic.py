def is_legit(state = "////////////////////////////////////"):
    if len(state) != 36:
        return False
    
    str = list(state) # muttable

    for i in range(36):
        if state[i] == 'a':
            if i - 1 < 0 or str[i - 1] != '/':
                return False
            str[i - 1] = 'A'
        
        if state[i] == 'b':
            if i - 1 < 0 or str[i - 1] != '/':
                return False
            str[i - 1] = 'B'
        
        if state[i] == 'c':
            if i - 6 < 0 or str[i - 6] != '/':
                return False
            str[i - 6] = 'C'
        
        if state[i] == 'm':
            if i - 2 < 0:
                return False
            for k in range (i - 2, i):
                if str[k] != '/':
                    return False

        if state[i] == 'N':
            if i - 12 < 0:
                return False
            for k in range (i - 12, i, 6):
                if str[k] != '/':
                    return False
    return True

def is_goal(state = "////////////////////////////////////"):
    return (state[17] == 'a')

def expand(state = "////////////////////////////////////"):
    succs = []
    coss = []

    if not is_legit(state):
        return succs, coss
    
    types = {
        'a': {'cost': 2, 'dir': 'h'},
        'b': {'cost': 2, 'dir': 'h'},
        'c': {'cost': 2, 'dir': 'v'},
        'm': {'cost': 2, 'dir': 'h'},
        'n': {'cost': 2, 'dir': 'v'}
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