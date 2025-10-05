import random

def generate_k_sat(k, m, n, seed=None):
    """
    Generate a uniform random k-SAT instance.
    k: number of literals per clause
    m: number of clauses
    n: number of variables
    seed: optional random seed
    Returns: list of clauses (each clause is a list of integers)
    """
    if seed is not None:
        random.seed(seed)

    clauses = []
    for _ in range(m):
        # Randomly select k distinct variables
        variables = random.sample(range(1, n+1), k)
        clause = []
        for var in variables:
            # Randomly decide to negate variable
            literal = var if random.choice([True, False]) else -var
            clause.append(literal)
        clauses.append(clause)
    return clauses

# Example usage
if _name_ == "_main_":
    k = 3
    m = 5
    n = 4
    clauses = generate_k_sat(k, m, n, seed=42)
    print("Generated 3-SAT clauses:")
    print(clauses)
