import random
import math
from itertools import combinations
import matplotlib.pyplot as plt

# ---- parameters from the task ----

# message space M = {0,1}^3
message_space = [
	[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
	[1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]
]

# [7,4,3] Hamming codewords X'
codewords = [
	[0, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 1, 1, 0],
	[0, 1, 0, 0, 1, 0, 1],
	[1, 1, 0, 0, 0, 1, 1],
	[0, 0, 1, 0, 0, 1, 1],
	[1, 0, 1, 0, 1, 0, 1],
	[0, 1, 1, 0, 1, 1, 0],
	[1, 1, 1, 0, 0, 0, 0],
	[0, 0, 0, 1, 1, 1, 1],
	[1, 0, 0, 1, 0, 0, 1],
	[0, 1, 0, 1, 0, 1, 0],
	[1, 1, 0, 1, 1, 0, 0],
	[0, 0, 1, 1, 1, 0, 0],
	[1, 0, 1, 1, 0, 1, 0],
	[0, 1, 1, 1, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1]
]

r_bound = 1  # max errors for Bob
s_bound = 3  # max errors for Eve

num_trials = 2**14


# ---- channel code from task 2 ----

def get_error_vector(n, max_errors):
	possible_errors = []

	for weight in range(max_errors + 1):
		for indices in combinations(range(n), weight):
			err = [0] * n

			for i in indices:
				err[i] = 1

			possible_errors.append(err)

	return random.choice(possible_errors)


def eavesdropper_channel(x, max_errors=3):
	err = get_error_vector(len(x), max_errors)
	z = [(x[i] + err[i]) % 2 for i in range(len(x))]
	return z, err


# ---- encoder from task 3 ----

def ones_complement(bits):
	return [1 - b for b in bits]


def random_binning_encode(u):
	d_bar = ones_complement(u)

	prefix_a = [0] + u
	prefix_b = [1] + d_bar

	bin_candidates = [
		cw for cw in codewords
		if cw[:4] == prefix_a or cw[:4] == prefix_b
	]

	return random.choice(bin_candidates)


def bits_to_str(bits):
	return "".join(map(str, bits))


# ---- simulation: encoder + eavesdropper channel ----
print(f"simulating {num_trials} encoder + eavesdropper channel realizations...")

u_results = []
z_results = []

for _ in range(num_trials):
	u = random.choice(message_space)
	x = random_binning_encode(u)
	z, _ = eavesdropper_channel(x, s_bound)

	u_results.append(bits_to_str(u))
	z_results.append(bits_to_str(z))


# ---- plot p_{z|u}(· | d) for all d in M ----
print("plotting p(z|u=d) for all d in M...")

all_u_vals = sorted(set(u_results))
all_z_vals = sorted(set(z_results))

fig, axes = plt.subplots(2, 4, figsize=(18, 7))
axes = axes.flatten()

for idx, d in enumerate(all_u_vals):
	z_given_d = [z_results[i] for i in range(num_trials) if u_results[i] == d]
	count_d = len(z_given_d)

	probs = [z_given_d.count(c) / count_d for c in all_z_vals]

	axes[idx].bar(range(len(all_z_vals)), probs)
	axes[idx].set_title(f"p(z | u={d})")
	axes[idx].set_xticks([])
	axes[idx].set_ylabel("probability")

plt.suptitle("Conditional distribution p(z|u=d) for all d in M")
plt.tight_layout()
plt.savefig("task4_pzu.png", dpi=150)
print("plot saved to task4_pzu.png")


# ---- empirical joint distribution p_hat_{u,z}(d, c) ----
joint = {}
for i in range(num_trials):
	pair = (u_results[i], z_results[i])
	joint[pair] = joint.get(pair, 0) + 1

for key in joint:
	joint[key] /= num_trials


# ---- empirical marginal distributions p_hat_u(d) and p_hat_z(c) ----
p_u = {}
for d in u_results:
	p_u[d] = p_u.get(d, 0) + 1
for d in p_u:
	p_u[d] /= num_trials

p_z = {}
for c in z_results:
	p_z[c] = p_z.get(c, 0) + 1
for c in p_z:
	p_z[c] /= num_trials

print("\nempirical marginal p_u(d):")
for d in sorted(p_u):
	print(f"  p_u({d}) = {p_u[d]:.6f}")

print(f"\nempirical marginal p_z(c): {len(p_z)} distinct z values observed")


# ---- empirical entropy H(u) ----
H_u = -sum(p * math.log2(p) for p in p_u.values() if p > 0)
print(f"\nempirical entropy H(u) = {H_u:.6f} bits")


# ---- empirical mutual information I_hat(u; z) ----
I_uz = 0.0
for (d, c), p_joint in joint.items():
	if p_joint > 0:
		I_uz += p_joint * math.log2(p_joint / (p_u[d] * p_z[c]))

print(f"empirical mutual information I_hat(u; z) = {I_uz:.6f} bits")

if I_uz < 1e-3:
	print("I(u;z) ≈ 0: u and z are nearly independent — perfect secrecy achieved.")
else:
	print("I(u;z) > 0: some information about u is leaked to Eve.")
