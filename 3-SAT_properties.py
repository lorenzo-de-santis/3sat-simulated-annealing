import numpy as np
import matplotlib.pyplot as plt
from KSAT import KSAT
from SimAnn import simann

## function to compute the empirical probability of solving a 3-SAT instance
## using the formula P = number of solved instances / total number of instances
def compute_empirical_probability(N, M, n_instances = 30, 
                                  anneal_steps = 10, mcmc_steps = 5000,
                                  beta0 = 0.1, beta1 = 10.0, seed = None,):
    if seed is not None:
        np.random.seed(seed)

    solved_instances = 0

    for i in range(n_instances):
        # Generate a random 3-SAT instance
        problem = KSAT(N, M, 3)

        # Solve the instance using simulated annealing, indexed 0 
        # to get only the best solution without the acceptance rate
        best_solution = simann(problem, anneal_steps, mcmc_steps, 
                                        beta0, beta1)[0]

        # Check if the problem is solved (cost = 0 means all clauses are satisfied)
        if best_solution.cost() == 0:
            solved_instances += 1

    return solved_instances / n_instances


N = 200
M = [300, 400, 500, 600, 700, 800, 900, 1000]
n_instances = 30
mcmc_steps = 5000
anneal_steps = 50
beta0 = 0.01
beta1 = 5.0

results = {}
for m in M:
    prob = compute_empirical_probability(N, m, n_instances, anneal_steps, mcmc_steps, beta0, beta1, seed = 42)
    results[m] = prob
    print(f"M = {m}, P(N={N}, M={m}) = {prob}")
    
#plot P(N,M) vs M for different values of M
plt.plot(results.keys(), results.values(), marker = 'o')
plt.xlabel("Number of Clauses (M)")
plt.ylabel("Empirical Probability P(N, M)")
plt.title("Empirical Probability P(N, M) vs M for N = 200")
plt.grid(True)
plt.show()

N_values = [300, 400, 500, 600]  # Different values of N
M_values = [600, 800, 1000, 1200, 1400, 1600] 
n_instances = 30
anneal_steps = 20
mcmc_steps = 3000
beta0 = 0.01
beta1 = 4.0

# Initialize data structures to store results
results = {}            # Dictionary to store probabilities for each N

for N in N_values:
    probabilities = []  # Store probabilities for current N
    for M in M_values:
        p = compute_empirical_probability(N, M, n_instances, 
                                          anneal_steps, mcmc_steps, 
                                          beta0, beta1)
        probabilities.append(p)
        print(f"N = {N}, M = {M}, P(N={N}, M={M}) = {p}")

    results[N] = probabilities  #save N and probabilities as a key-value pair in the dictionary

   
# Plot P(N, M) vs M for different N
for N, probs in results.items():
    plt.plot(M_values, probs, marker='o', label=f'N = {N}')
plt.xlabel("Number of Clauses (M)")
plt.ylabel("Empirical Probability P(N, M)")
plt.title("P(N, M) vs M for Different N")
plt.legend()
plt.grid(True)
plt.show()

# Collapse the curves: P(N, M) vs M / N
for N, probs in results.items():
    rescaled_M = [M / N for M in M_values]
    plt.plot(rescaled_M, probs, marker='o', label=f'N = {N}')
plt.xlabel("Rescaled Number of Clauses (M / N)")
plt.ylabel("Empirical Probability P(N, M)")
plt.title("Collapsed Curves: P(N, M) vs M / N")
plt.legend()
plt.grid(True)    
plt.show()
