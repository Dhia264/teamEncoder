import numpy as np
import matplotlib.pyplot as plt
import random
from itertools import combinations

# ---- parameters from the task ----

# input x = 1001000
x_input = [1, 0, 0, 1, 0, 0, 0]

r_bound = 1   # max errors for Bob
s_bound = 3   # max errors for Eve

num_trials = 2**14   # number of simulations (>= 16384)


def get_error_vector(n, max_errors):
    possible_errors = []
    
    for weight in range(max_errors + 1):
        for indices in combinations(range(n), weight):
            err = [0] * n
            
            for i in indices:
                err[i] = 1
                
            possible_errors.append(err)
    
    return random.choice(possible_errors)


# ---- storage ----
y_results = []
z_results = []

# ---- simulation ----
for _ in range(num_trials):
    
    # independent errors
    err_y = get_error_vector(7, r_bound)
    err_z = get_error_vector(7, s_bound)
    
    # XOR (mod 2)
    y = [(x_input[i] + err_y[i]) % 2 for i in range(7)]
    z = [(x_input[i] + err_z[i]) % 2 for i in range(7)]
    
    # store as strings
    y_results.append("".join(map(str, y)))
    z_results.append("".join(map(str, z)))


# ---- plotting ----
def plot_results(data, title):
    unique_vals = sorted(list(set(data)))
    probs = [data.count(v) / num_trials for v in unique_vals]
    
    plt.figure(figsize=(12, 5))
    plt.bar(unique_vals, probs)
    
    plt.title(title)
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("empirical probability")
    
    plt.tight_layout()
    plt.show()


print("plotting distributions...")

plot_results(y_results, "Bob distribution p(y|x), r=1")
plot_results(z_results, "Eve distribution p(z|x), s=3")


# ---- conditional independence check ----
print("\nchecking if y and z are conditionally independent...")

# joint distribution
joint = {}
for i in range(num_trials):
    pair = (y_results[i], z_results[i])
    joint[pair] = joint.get(pair, 0) + 1

# normalize
for key in joint:
    joint[key] /= num_trials

# compare p(y,z) with p(y)p(z) for a few samples
print("\nsome comparisons (p(y,z) vs p(y)*p(z)):")

for i in range(10):
    y_val = y_results[i]
    z_val = z_results[i]
    
    p_y = y_results.count(y_val) / num_trials
    p_z = z_results.count(z_val) / num_trials
    p_joint = joint[(y_val, z_val)]
    
    print(f"{p_joint:.6f}  vs  {p_y * p_z:.6f}")