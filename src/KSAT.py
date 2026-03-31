import numpy as np
from copy import deepcopy

class KSAT:
    def __init__(self, N, M, K, seed = None):
        if not (isinstance(K, int) and K >= 2):
            raise Exception("k must be an int greater or equal than 2")
        self.K = K
        self.M = M
        self.N = N

        ## Optionally set up the random number generator state
        if seed is not None:
            np.random.seed(seed)
    
        # s is the sign matrix
        s = np.random.choice([-1,1], size=(M,K))
        
        # index is the matrix reporting the index of the K variables of the m-th clause 
        index = np.zeros((M,K), dtype = int)        
        for m in range(M):
            index[m] = np.random.choice(N, size=(K), replace=False)
            
        # Dictionary for keeping track of literals in clauses
        clauses = []   
        for n in range(N):
            clauses.append([i for i, row in enumerate(index) if n in row])
        
        self.s, self.index, self.clauses = s, index, clauses        
        
        ## initalize the configuration
        x = np.ones(N, dtype=int)
        self.x = x
        self.init_config()

    ## Initialize (or reset) the current configuration
    def init_config(self):
        N = self.N 
        self.x[:] = np.random.choice([-1,1], size=(N))
        
    ## cost function using eq.(4) of pdf file
    def cost(self):
        s, x, index = self.s, self.x, self.index
        # exploit broadcasting and numpy vectorization to compute the cost to recreate eq.(4) in the pdf file
        c = np.sum(np.prod((1 - s * x[index]) / 2, axis=1))
        return c

    ## Propose a valid random move. 
    def propose_move(self):
        N = self.N
        move = np.random.choice(N)
        return move
    
    ## Modify the current configuration, accepting the proposed move
    def accept_move(self, move):
        self.x[move] *= -1

    ## Compute the extra cost of the move (new-old, negative means convenient)
    def compute_delta_cost(self, move):
        clauses, x, K, index, s = self.clauses, self.x, self.K, self.index, self.s
        
        affected_clauses = clauses[move]        
        xi = x[move]                                    # variable to be flipped

        delta_cost = 0

        for clause in affected_clauses:
            satisfied_before = False
            satisfied_after = False 

            for k in range(K):
                i_literal = index[clause, k]            # index of the literal in the clause

                if s[clause, k] * x[i_literal] == 1:
                    satisfied_before = True             # clause satisfied in the current condiguration

                if i_literal == move:
                    flipped_value = -xi
                    if s[clause, k] * flipped_value == 1:
                        satisfied_after = True          # clause satisfied after the flip
                
                elif s[clause, k] * x[i_literal] == 1:
                    satisfied_after = True

            if satisfied_before and not satisfied_after:
                delta_cost += 1

            elif not satisfied_before and satisfied_after:
                delta_cost -= 1
            # reduce the cost if the clause is satisfied after the flip (better configuration, less cost)
            # increase the cost if the clause is not satisfied after the flip (worse configuration, more cost)
            
        return delta_cost
    
    ## Make an entirely independent duplicate of the current object.
    def copy(self):
        return deepcopy(self)
    
    ## The display function should not be implemented
    def display(self):
        pass
        
    # vectorized version of the compute_delta_cost function, better performance for large K
    # since we focus on 3-SAT, looping over k is not a big deal, but for larger K this is a better approach
    # def compute_delta_cost_VECT(self, move):
        # clauses, x, index, s = self.clauses, self.x, self.index, self.s
        # # x_i = x[move]                                       #current value of the selected variable to flip
        # affected_clauses = np.array(clauses[move])            #clauses containing x_i
        
        # if affected_clauses.size == 0:                        # if x_i is not in any clause the delta cost is 0
        #     return 0
        
        # #extract the indices and signs of the variables in the intrested clauses
        # indexes = index[affected_clauses]
        # signs = s[affected_clauses]
        # variables = x[indexes]
        # satisfied_before = np.any(signs * variables == 1, axis = 1)
        # satisfied_after = np.any(signs * np.where(indexes == move, -1 * variables, variables) == 1, axis=1)
        # delta_cost = np.sum(satisfied_before & ~satisfied_after) - np.sum(~satisfied_before & satisfied_after) #cost increases if a clause satisfied becomes unsatisfied and viceversa 
        
        # return delta_cost
    
    






