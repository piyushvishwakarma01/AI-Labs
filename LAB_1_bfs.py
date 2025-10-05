from collections import deque

def successors(state):
    i = state.index('.')
    res = []
    n = len(state)
    # check left side rabbits moving right into dot
    if i-1 >= 0 and state[i-1] == 'E':
        s = list(state); s[i], s[i-1] = s[i-1], s[i]; res.append(''.join(s))
    if i-2 >= 0 and state[i-2] == 'E':
        s = list(state); s[i], s[i-2] = s[i-2], s[i]; res.append(''.join(s))
    # W from i+1 or i+2 moving left into dot
    if i+1 < n and state[i+1] == 'W':
        s = list(state); s[i], s[i+1] = s[i+1], s[i]; res.append(''.join(s))
    if i+2 < n and state[i+2] == 'W':
        s = list(state); s[i], s[i+2] = s[i+2], s[i]; res.append(''.join(s))
    return res

def bfs(start="EEE.WWW", goal="WWW.EEE"):
    q = deque([(start, [start])])
    visited = {start}
    while q:
        state, path = q.popleft()
        if state == goal:
            return path
        for s in successors(state):
            if s not in visited:
                visited.add(s)
                q.append((s, path + [s]))
    return None

if __name__ == "__main__":
    path = bfs()
    print("BFS steps:", len(path)-1)
    for step in path:
        print(step)
