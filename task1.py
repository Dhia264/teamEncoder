import numpy as np
import matplotlib.pyplot as plt
import random
from itertools import combinations

# parameters
x_input = [1, 0, 0, 1, 0, 0, 0]

r_bound = 1
s_bound = 3

num_trials = 2**14  # >= 16384

# function to generate uniform error vectors
def get_error_vector(n, max_errors):
    possible_errors = []
    
    for weight in range(max_errors + 1):
        for indices in combinations(range(n), weight):
            err = [0] * n
            for i in indices:
                err[i] = 1
            possible_errors.append(err)
    
    return random.choice(possible_errors)


#simulation 
y_results = []
z_results = []

for _ in range(num_trials):
    
    err_y = get_error_vector(7, r_bound)
    err_z = get_error_vector(7, s_bound)
    
    y = [(x_input[i] + err_y[i]) % 2 for i in range(7)]
    z = [(x_input[i] + err_z[i]) % 2 for i in range(7)]
    
    y_results.append("".join(map(str, y)))
    z_results.append("".join(map(str, z)))


# plotting 
def plot_distribution(data, title):
    unique_vals = sorted(set(data))
    probs = [data.count(v) / num_trials for v in unique_vals]
    
    plt.figure(figsize=(12, 5))
    plt.bar(unique_vals, probs)
    plt.title(title)
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("empirical probability")
    plt.tight_layout()
    plt.show()


print("Plotting distributions...")
plot_distribution(y_results, "p(y|x) with r=1")
plot_distribution(z_results, "p(z|x) with s=3")


# conditional independence check 
print("\nChecking conditional independence...")

# joint distribution
joint = {}
for i in range(num_trials):
    pair = (y_results[i], z_results[i])
    joint[pair] = joint.get(pair, 0) + 1

# normalize
for key in joint:
    joint[key] /= num_trials

# compute max error
max_diff = 0

for (y_val, z_val), p_joint in joint.items():
    p_y = y_results.count(y_val) / num_trials
    p_z = z_results.count(z_val) / num_trials
    
    diff = abs(p_joint - p_y * p_z)
    if diff > max_diff:
        max_diff = diff

print(f"Maximum difference |p(y,z) - p(y)p(z)| = {max_diff:.6f}")
