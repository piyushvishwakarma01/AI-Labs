

import numpy as np
import matplotlib.pyplot as plt



print("\n Q3: Error Tolerance for Stored Patterns \n")

# 4 patterns (25 bits each), columns are patterns
X = np.array([
    [ 1,  1,  1,  1, -1, -1,  1, -1, -1,  1, -1,  1, -1, -1,  1, -1,  1, -1, -1,  1, -1,  1,  1,  1, -1],
    [ 1,  1,  1,  1,  1, -1, -1, -1,  1, -1, -1, -1, -1,  1, -1,  1, -1, -1,  1, -1,  1,  1,  1, -1, -1],
    [-1,  1,  1,  1,  1,  1, -1, -1, -1, -1,  1, -1, -1, -1, -1,  1, -1, -1, -1, -1, -1,  1,  1,  1,  1],
    [ 1, -1, -1, -1,  1,  1,  1, -1,  1,  1,  1, -1,  1, -1,  1,  1, -1, -1, -1,  1,  1, -1, -1, -1,  1]
]).T

num_bits, num_patterns = X.shape


W = np.zeros((num_bits, num_bits))
for i in range(num_patterns):
    W += np.outer(X[:, i], X[:, i])
np.fill_diagonal(W, 0)
W /= num_patterns


def recall(pattern):
    y = pattern.copy()
    for _ in range(15):  # sufficient for convergence
        y_new = np.sign(W @ y)
        if np.all(y_new == y):
            break
        y = y_new
    return y


tolerance = np.zeros(num_patterns, dtype=int)

for p in range(num_patterns):
    original = X[:, p]
    for flips in range(1, num_bits + 1):
        idx = np.random.choice(num_bits, flips, replace=False)
        distorted = original.copy()
        distorted[idx] *= -1
        recovered = recall(distorted)
        if not np.array_equal(recovered, original):
            tolerance[p] = flips - 1
            break

print("Error tolerance (bits) for each stored pattern:")
for i, t in enumerate(tolerance):
    print(f"Pattern {i+1}: tolerates {t} bit flips")




print("\n Q4: Eight-Rook Problem \n")

def generate_initial_board():
    board = np.zeros((8,8), dtype=int)
    rook_positions = np.random.choice(64, 8, replace=False)
    for pos in rook_positions:
        board[pos//8, pos%8] = 1
    return board

def energy(board):
    E = 0

    # Each row must have exactly 1 rook
    for i in range(8):
        E += (board[i].sum() - 1)**2

    # Each column must have exactly 1 rook
    for j in range(8):
        E += (board[:, j].sum() - 1)**2

    return E

def hopfield_eight_rook(board, iterations=1000):
    E = energy(board)

    for _ in range(iterations):
        # choose positions to swap
        r1, c1 = np.random.randint(8), np.random.randint(8)
        r2, c2 = np.random.randint(8), np.random.randint(8)

        if board[r1,c1] == 1 and board[r2,c2] == 0:
            # tentative swap
            board[r1,c1], board[r2,c2] = 0, 1
            new_E = energy(board)

            if new_E > E:  # revert if energy did not decrease
                board[r1,c1], board[r2,c2] = 1, 0
            else:
                E = new_E

    return board, E

initial = generate_initial_board()
print("Initial Energy:", energy(initial))

final_board, final_E = hopfield_eight_rook(initial.copy())
print("Final Energy:", final_E)

plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.title("Initial Board")
plt.imshow(initial, cmap='binary')
plt.subplot(1,2,2)
plt.title("Final Board")
plt.imshow(final_board, cmap='binary')
plt.show()



print("\n Q5: TSP (10 Cities)\n")

np.random.seed(0)
num_cities = 10

city_coords = np.random.rand(num_cities, 2) * 50

# Distance matrix
dist = np.zeros((num_cities, num_cities))
for i in range(num_cities):
    for j in range(num_cities):
        dist[i,j] = np.linalg.norm(city_coords[i] - city_coords[j])

print("Number of neurons in Hopfield TSP = 10 cities × 10 positions = 100 neurons")
print("Number of weights = 100 × 100 =", 100*100)

# Simple stochastic TSP solver
def tsp_energy(tour):
    return sum(dist[tour[i], tour[(i+1)%num_cities]] for i in range(num_cities))

tour = np.random.permutation(num_cities)
best_tour = tour.copy()
best_cost = tsp_energy(tour)

for _ in range(50000):
    i, j = np.random.choice(num_cities, 2, replace=False)
    new_tour = tour.copy()
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    new_cost = tsp_energy(new_tour)
    if new_cost < best_cost:
        best_cost = new_cost
        best_tour = new_tour.copy()
    tour = new_tour

print("\nBest Tour Found:", best_tour)
print("Minimum Path Cost:", best_cost)

# Plot solution
plt.figure(figsize=(8,6))
plt.scatter(city_coords[:,0], city_coords[:,1], c='red')
for i, coord in enumerate(city_coords):
    plt.text(coord[0], coord[1], str(i+1))

for i in range(num_cities):
    p1 = city_coords[best_tour[i]]
    p2 = city_coords[best_tour[(i+1)%num_cities]]
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-')

plt.title("TSP Route (Hopfield Network Approximation)")
plt.show()

