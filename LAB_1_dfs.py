# Initial and goal states
initial_state = "EEE.WWW"
goal_state = "WWW.EEE"

# Possible moves relative to the empty space
moves = [-2, -1, 1, 2]

# Check if a move is valid
def is_valid_move(state, empty_idx, move):
    new_idx = empty_idx + move
    if new_idx < 0 or new_idx >= len(state):
        return False
    
    rabbit = state[new_idx]
    
    # East-bound rabbits move right
    if move > 0 and rabbit == 'W':
        return False
    # West-bound rabbits move left
    if move < 0 and rabbit == 'E':
        return False
    # Jumping over empty or same type is invalid
    if abs(move) == 2 and state[empty_idx + move // 2] not in ('E', 'W'):
        return False
    
    return True

# Generate new state after moving a rabbit
def generate_new_state(state, empty_idx, move):
    new_idx = empty_idx + move
    state_list = list(state)
    state_list[empty_idx], state_list[new_idx] = state_list[new_idx], state_list[empty_idx]
    return ''.join(state_list)

# DFS Implementation
def dfs(initial, goal):
    stack = [(initial, [initial])]
    visited = set([initial])
    
    while stack:
        state, path = stack.pop()
        if state == goal:
            return path
        
        empty_idx = state.index('.')
        for move in moves:
            if is_valid_move(state, empty_idx, move):
                new_state = generate_new_state(state, empty_idx, move)
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append((new_state, path + [new_state]))
    return None

# Run DFS
if __name__ == "__main__":
    solution_path = dfs(initial_state, goal_state)
    if solution_path:
        print("DFS Solution Path:")
        print(" → ".join(solution_path))
    else:
        print("No solution found.")
