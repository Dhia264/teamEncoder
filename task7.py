from collections import Counter
import random
import matplotlib.pyplot as plt
import math
# CODEBOOK 
codebook = [
    "0000000","1000110","0100101","1100011",
    "0010011","1010101","0110110","1110000",
    "0001111","1001001","0101010","1101100",
    "0011100","1011010","0111001","1111111"
]

messages = ["000","001","010","011","100","101","110","111"]

# TASK 2 — encoder 
def xor_bits(a, b):
    return "".join(str(int(x)^int(y)) for x, y in zip(a, b))

def encoder(d):
    d_bar = xor_bits(d, "111")
    valid = [cw for cw in codebook
             if cw[:4] == "0" + d or cw[:4] == "1" + d_bar]
    return random.choice(valid)

# TASK 3 — decoder + helper functions
def hamming_distance(a, b):
	return sum((a[i] != b[i]) for i in range(len(a)))

def ones_complement(bits):
    return [1 - b for b in bits]

codewords = [[int(b) for b in cw] for cw in codebook]

def deterministic_decode(y):
	# step 1: find x_hat = argmin d_H(y, a) over a in X'
	distances = [hamming_distance(y, cw) for cw in codewords]
	min_dist = min(distances)
	x_hat = codewords[distances.index(min_dist)]

	# step 2: recover u_hat from x_hat_1 (first bit)
	if x_hat[0] == 0:
		u_hat = x_hat[1:4]
	else:
		u_hat = ones_complement(x_hat[1:4])

	return x_hat, u_hat

def decoder(y):
    # convert string to list of ints for deterministic_decode
    if isinstance(y, str):
        y = [int(b) for b in y]
    
    _, u_hat = deterministic_decode(y)
    
    # convert list of ints back to string to match the rest of the code
    return "".join(map(str, u_hat))

# TASK 6 — BSC 
def BSC(X, e):
    if isinstance(X, str):
        X = [int(b) for b in X]
    B = []
    for bit in X:
        if e > random.random():
            B.append(1 - bit)
        else:
            B.append(bit)
    return "".join(map(str, B))

# TASK 7 

#PART 1 - Reliability Plot
def reliability(trials, epsilons,fixed_eps):
    P_error_list = []
    
    p_err_at_target = 0

    for epsilon in epsilons:
        error = 0
        for _ in range(trials):
            u = random.choice(messages)
            x = encoder(u)
            y = BSC(x, epsilon) 
            hat = decoder(y)
            if hat != u:
                error += 1
        
        prob = error / trials
        P_error_list.append(prob)
        
        # Store fixed epsilon result
        if abs(epsilon - fixed_eps) < 0.001:
            p_err_at_target = prob
            
        print(f"Epsilon {epsilon:.2f} completato.")

    plt.figure(figsize=(10, 6))
    plt.plot(epsilons, P_error_list, marker='o', color='red', label='Hamming [7,4,3]')
    plt.title('Reliability of the communication system')
    plt.xlabel('epsilon (BSC error probability)')
    plt.ylabel('Probability of Error (P_err)')
    plt.grid(True)
    plt.savefig(f"grafic-reliability-{fixed_eps}.png")
    
    return p_err_at_target

#PART 2 - Secrecy Plot
def secrecy(delta,trials, fixed_eps): 
    leaked_info = []

    for d in delta:
        pairs = []
        # Generate (U,Z) samples
        for _ in range(trials):
            u = random.choice(messages)
            x = encoder(u)
            z = BSC(x, d) 
            pairs.append((u, z))
        
        count_u = Counter([p[0] for p in pairs])
        count_z = Counter([p[1] for p in pairs])
        count_uz = Counter(pairs)
        # Empirical mutual information I(U;Z)
        i_uz = 0
        for (u, z), c_uz in count_uz.items():
            p_uz = c_uz / trials
            p_u = count_u[u] / trials
            p_z = count_z[z] / trials
            i_uz += p_uz * math.log2(p_uz / (p_u * p_z))
        
        leaked_info.append(i_uz)
        
        print(f"Delta {d:.2f} -> I(U;Z) = {i_uz:.4f} bit")

    plt.figure(figsize=(10, 6))
    plt.plot(delta, leaked_info, 'r-s', label='Leaked Information $\hat{I}(U;Z)$')
    plt.axhline(y=0, color='black', linestyle='--')
    plt.title('System Secrecy: Leaked Information vs Eve\'s Noise')
    plt.xlabel('Delta ($\delta$)')
    plt.ylabel('Information (bits)')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"grafic-secrecy-{fixed_eps}.png")
    return leaked_info

#PART 3 - Upper Bound Plot
def plot_upper_bound(p_err_bob, delta_list, leaked_info_eve, fixed_eps):

    upper_bound = [p_err_bob + i_uz for i_uz in leaked_info_eve]
    
    plt.figure(figsize=(10, 6))
    plt.plot(delta_list, upper_bound, 'm-d', linewidth=2, label=r'Upper Bound: $P[err] + I(U;Z)$')
    
    plt.axhline(y=p_err_bob, color='b', linestyle='--', alpha=0.6, label=f'P[err] (fixed eps)')
    
    plt.plot(delta_list, leaked_info_eve, 'r:', alpha=0.5, label='Leaked Info I(U;Z)')
    
    plt.title('Task 7.3 - Upper Bound on Unconditional Security')
    plt.xlabel('Delta ($\delta$)')
    plt.ylabel('Security Metric (bits / prob)')
    plt.grid(True, which='both', linestyle=':', alpha=0.7)
    plt.legend()
    plt.savefig(f"grafic-upperbound-{fixed_eps}.png")
    return upper_bound

#PART 4 - Total Variation Distance Plot
def total_variation( delta, trials, fixed_eps, upper_bound):
    dv_list = []

    # All possible 7-bit outputs for Z
    all_possible_z = [format(i, '07b') for i in range(128)]

    print(f"Computing dV with epsilon={fixed_eps}...")
    for d in delta:
        triplets = []
        for _ in range(trials):
            u = random.choice(messages)
            x = encoder(u)
            y = BSC(x, fixed_eps) 
            z = BSC(x, d) 
            hat = decoder(y)
            triplets.append((u, hat, z))
        
        count_uhatz = Counter(triplets)
        count_u = Counter([t[0] for t in triplets])
        count_z = Counter([t[2] for t in triplets])
        
        dv = 0
        # Full empirical dV computation 
        for u in messages:
            p_u = count_u[u] / trials
            for hat_u in messages:
                indicator = 1.0 if u == hat_u else 0.0
                for z in all_possible_z: 
                    p_real = count_uhatz[(u, hat_u, z)] / trials
                    p_z = count_z[z] / trials
                    
                    # Ideal system distribution
                    p_ideal = p_u * indicator * p_z
                    dv += abs(p_real - p_ideal)
        
        current_dv = 0.5 * dv
        dv_list.append(current_dv)
        print(f"Delta {d:.2f} -> dV = {current_dv:.4f}")

    plt.figure(figsize=(10, 6))
    plt.plot(delta, upper_bound, 'm--', linewidth=2, label='Upper Bound ($P_{err} + I(U;Z)$)')
    plt.plot(delta, dv_list, 'g-o', label='Total Variation Distance ($d_V$)')
    plt.title(f'Unconditional Security: dV vs Upper Bound (ε={fixed_eps})')
    plt.xlabel('Delta')
    plt.ylabel('Value')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    plt.savefig(f"grafic-total_variation-{fixed_eps}.png")

# PART 5 - Secrecy Capacity Plot
#helper function 

def binary_entropy(p):
        if p == 0 or p == 1:
            return 0.0
        return -p * math.log2(p) - (1-p) * math.log2(1-p)

#main function
def secrecy_capacity_plot(delta, fixed_eps):
    
    cs = []
    for d in delta:
        # Wiretap BSC secrecy capacity
        if abs(fixed_eps - 0.5) <= abs(d - 0.5):
            cs.append(0.0)
        else:
            cs.append(max(0.0, binary_entropy(d) - binary_entropy(fixed_eps)))
    
    plt.figure(figsize=(10, 6))
    plt.plot(delta, cs, 'b-o')
    plt.title(f'Secrecy Capacity (ε={fixed_eps})')
    plt.xlabel('δ')
    plt.ylabel('Cs [bit/channel use]')
    plt.grid(True)
    plt.savefig(f"grafic-secrecy-capacity-{fixed_eps}.png")


def task7():
    trials = 2**14
    epsilons = [a * 0.01 for a in range(0, 51)]
    delta = [a * 0.01 for a in range(0, 51)]
    fixed_eps = 0.10
    
    p_err_fixed = reliability(trials,epsilons,fixed_eps) 
        
    leaked_info = secrecy(delta, trials, fixed_eps)

    upper_bound =plot_upper_bound(p_err_fixed, delta, leaked_info, fixed_eps)

    total_variation( delta, trials, fixed_eps,upper_bound)
    
    secrecy_capacity_plot(delta, fixed_eps)

if __name__ == "__main__":
    print("=== TASK 7 ===")
    task7() 