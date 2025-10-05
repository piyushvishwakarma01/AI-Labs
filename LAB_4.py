import numpy as np
import random
import math



def cost_function(state, goal_state):
    """
    Compute cost based on number of misplaced pieces.
    Lower cost means the current configuration is closer to goal.
    """
    # Count number of pieces that are not in their correct position
    misplaced = np.sum(state != goal_state)
    return misplaced


def generate_neighbor(state):
    """
    Generate a neighboring state by swapping two adjacent pieces.
    """
    new_state = state.copy()
    n = len(state)

    # Randomly pick two distinct indices to swap
    i, j = random.sample(range(n), 2)
    new_state[i], new_state[j] = new_state[j], new_state[i]

    return new_state


def simulated_annealing(initial_state, goal_state, T_max=100.0, T_min=0.1, alpha=0.95, max_iter=1000):
    """
    Perform simulated annealing to minimize the cost function.
    """
    current_state = initial_state.copy()
    current_cost = cost_function(current_state, goal_state)
    best_state = current_state.copy()
    best_cost = current_cost

    T = T_max  # Initial temperature

    for iteration in range(max_iter):
        # Generate a new neighboring state
        neighbor_state = generate_neighbor(current_state)
        neighbor_cost = cost_function(neighbor_state, goal_state)

        delta_E = neighbor_cost - current_cost

        # If new state is better, accept it; else accept probabilistically
        if delta_E < 0 or random.random() < math.exp(-delta_E / T):
            current_state = neighbor_state
            current_cost = neighbor_cost

            # Track the best solution found so far
            if current_cost < best_cost:
                best_state = current_state.copy()
                best_cost = current_cost

        # Cool down the temperature
        T *= alpha

        # Stop if temperature is too low or puzzle solved
        if T < T_min or best_cost == 0:
            break

    return best_state, best_cost


if _name_ == "_main_":
    # Let's assume puzzle pieces are represented as a 1D array [0..8]
    n_pieces = 9
    goal_state = np.arange(n_pieces)          # Correct arrangement
    initial_state = np.random.permutation(n_pieces)  # Scrambled arrangement

    print("Initial (Scrambled) State:", initial_state)
    print("Goal State:", goal_state)

    solved_state, final_cost = simulated_annealing(initial_state, goal_state)

    print("\nSolved State:", solved_state)
    print("Final Cost (Misplaced Pieces):", final_cost)
