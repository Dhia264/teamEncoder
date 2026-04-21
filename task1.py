import numpy as np
import matplotlib.pyplot as plt
import random

# ---- parameters from the task ----
# x is given as 1001000
x_input = [1, 0, 0, 1, 0, 0, 0]

r_bound = 1   # max errors for Bob
s_bound = 3   # max errors for Eve

num_trials = 2**14   # number of simulations (at least 16384)

def get_error_vector(n, max_errors):
    possible_errors = []
    
    # try all possible weights from 0 up to max_errors
    for weight in range(max_errors + 1):
        from itertools import combinations
        
        # get all ways to choose 'weight' positions
        for indices in combinations(range(n), weight):
            err = [0] * n
            
            # put 1s in the chosen positions
            for i in indices:
                err[i] = 1
                
            possible_errors.append(err)
    
    # pick one randomly (uniform)
    return random.choice(possible_errors)


# store outputs here
y_results = []
z_results = []

# run the experiment many times
for _ in range(num_trials):
    
    # generate independent errors for Bob and Eve
    err_y = get_error_vector(7, r_bound)
    err_z = get_error_vector(7, s_bound)
    
    # XOR with x (mod 2 addition)
    y = [(x_input[i] + err_y[i]) % 2 for i in range(7)]
    z = [(x_input[i] + err_z[i]) % 2 for i in range(7)]
    
    # save as strings so it's easier to count later
    y_results.append("".join(map(str, y)))
    z_results.append("".join(map(str, z)))


# ---- plotting part ----
def plot_results(data, title):
    # get unique outputs
    unique_vals = sorted(list(set(data)))
    
    # compute probabilities manually
    counts = [data.count(v) / num_trials for v in unique_vals]
    
    plt.figure(figsize=(12, 5))
    plt.bar(unique_vals, counts)
    
    plt.title(title)
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("empirical probability")
    
    plt.tight_layout()
    plt.show()


print("plotting results...")

plot_results(y_results, "Bob distribution p(y|x), r=1")
plot_results(z_results, "Eve distribution p(z|x), s=3")