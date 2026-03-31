import SimAnn
import KSAT

# Generate a problem to solve.
# This generate a K-SAT instance with N=100 variables and M=350 Clauses
ksat = KSAT.KSAT(200, 500, 3)

## Optimize it.
best, acc_rates = SimAnn.simann(ksat,
                     mcmc_steps = 5000, anneal_steps = 30,
                     beta0 = 0.01, beta1 = 5.0,
                     
                     debug_delta_cost = False) # set to True to enable the check


# plot the acceptance rates
import matplotlib.pyplot as plt

plt.plot(acc_rates, marker='o')
plt.title("Acceptance Rate vs. Annealing Step")
plt.xlabel("Annealing Step")
plt.ylabel("Acceptance Rate")
plt.grid(True)
plt.show()
