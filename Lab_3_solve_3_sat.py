# 
import random
from generate_k_sat import generate_k_sat

def evaluate(solution, clauses):
    """Return number of satisfied clauses"""
    satisfied = 0
    for clause in clauses:
        if any((lit > 0 and solution[abs(lit)-1]) or (lit < 0 and not solution[abs(lit)-1]) for lit in clause):
            satisfied += 1
    return satisfied

def random_assignment(n):
    return [random.choice([True, False]) for _ in range(n)]

def neighbors(current):
    n = len(current)
    nbrs = []
    for i in range(n):
        neighbor = current.copy()
        neighbor[i] = not neighbor[i]
        nbrs.append(neighbor)
    return nbrs

# ------------------------------
# Hill-Climbing
# ------------------------------
def hill_climbing(clauses, max_iterations=1000):
    n = max(abs(lit) for clause in clauses for lit in clause)
    current = random_assignment(n)
    current_score = evaluate(current, clauses)

    for _ in range(max_iterations):
        nbrs = neighbors(current)
        nbr_scores = [evaluate(nb, clauses) for nb in nbrs]
        best_score = max(nbr_scores)
        if best_score <= current_score:
            break
        best_neighbor = nbrs[nbr_scores.index(best_score)]
        current, current_score = best_neighbor, best_score
        if current_score == len(clauses):
            break
    return current, current_score

def beam_search(clauses, beam_width=3, max_iterations=100):
    n = max(abs(lit) for clause in clauses for lit in clause)
    beam = [random_assignment(n) for _ in range(beam_width)]

    for _ in range(max_iterations):
        candidates = []
        for assignment in beam:
            candidates.extend(neighbors(assignment))
        candidates = sorted(candidates, key=lambda x: evaluate(x, clauses), reverse=True)
        beam = candidates[:beam_width]

        for assignment in beam:
            if evaluate(assignment, clauses) == len(clauses):
                return assignment, len(clauses)
    best_assignment = max(beam, key=lambda x: evaluate(x, clauses))
    return best_assignment, evaluate(best_assignment, clauses)

def variable_neighborhood_descent(clauses, max_iterations=1000):
    n = max(abs(lit) for clause in clauses for lit in clause)
    current = random_assignment(n)
    current_score = evaluate(current, clauses)
    
    for _ in range(max_iterations):
        improved = False
        for k in [1,2,3]:
            nbrs = []
            indices = list(range(n))
            if k == 1:
                for i in indices:
                    neighbor = current.copy()
                    neighbor[i] = not neighbor[i]
                    nbrs.append(neighbor)
            elif k == 2:
                for i in indices:
                    for j in indices:
                        if i < j:
                            neighbor = current.copy()
                            neighbor[i] = not neighbor[i]
                            neighbor[j] = not neighbor[j]
                            nbrs.append(neighbor)
            else:
                for i in indices:
                    for j in indices:
                        for l in indices:
                            if i < j < l:
                                neighbor = current.copy()
                                neighbor[i] = not neighbor[i]
                                neighbor[j] = not neighbor[j]
                                neighbor[l] = not neighbor[l]
                                nbrs.append(neighbor)
            best_score = current_score
            best_neighbor = current
            for nb in nbrs:
                score = evaluate(nb, clauses)
                if score > best_score:
                    best_score = score
                    best_neighbor = nb
                    improved = True
            current, current_score = best_neighbor, best_score
            if current_score == len(clauses):
                return current, current_score
        if not improved:
            break
    return current, current_score

if _name_ == "_main_":
    k = 3
    m = 5
    n = 4
    clauses = generate_k_sat(k, m, n, seed=42)
    print("Generated 3-SAT clauses:")
    print(clauses)

    print("\n--- Hill-Climbing ---")
    solution, score = hill_climbing(clauses)
    print("Satisfied clauses:", score, "/", len(clauses))
    print("Solution:", solution)

    print("\n--- Beam Search ---")
    solution, score = beam_search(clauses, beam_width=3)
    print("Satisfied clauses:", score, "/", len(clauses))
    print("Solution:", solution)

    print("\n--- Variable Neighborhood Descent ---")
    solution, score = variable_neighborhood_descent(clauses)
    print("Satisfied clauses:", score, "/", len(clauses))
    print("Solution:", solution)
