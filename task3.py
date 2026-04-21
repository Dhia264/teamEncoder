import random
from itertools import combinations

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


def legitimate_channel(x, max_errors=1):
    err = get_error_vector(len(x), max_errors)
    y = [(x[i] + err[i]) % 2 for i in range(len(x))]
    return y, err


# ---- encoder from task 2 ----

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


# ---- task 3: deterministic decoder D : Y -> M ----

def hamming_distance(a, b):
	return sum((a[i] != b[i]) for i in range(len(a)))


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


def bits_to_str(bits):
	return "".join(map(str, bits))


# ---- verification 1: encoder + decoder ----
print("verification 1: encoder + decoder")

num_trials_1 = 20
ok_1 = 0

for _ in range(num_trials_1):
	u = random.choice(message_space)
	x = random_binning_encode(u)
	x_hat, u_hat = deterministic_decode(x)

	success = (u_hat == u)
	if success:
		ok_1 += 1

	print(
		f"u={bits_to_str(u)}  x={bits_to_str(x)}  "
		f"x_hat={bits_to_str(x_hat)}  u_hat={bits_to_str(u_hat)}  ok={success}"
	)

print(f"correct decodings: {ok_1}/{num_trials_1}")


# ---- verification 2: encoder + legitimate channel + decoder ----
print("\nverification 2: encoder + legitimate channel + decoder")

num_trials_2 = 200
ok_2 = 0

for _ in range(num_trials_2):
	u = random.choice(message_space)
	x = random_binning_encode(u)
	y, err = legitimate_channel(x, r_bound)
	x_hat, u_hat = deterministic_decode(y)

	success = (u_hat == u)
	if success:
		ok_2 += 1

print(f"correct decodings with channel: {ok_2}/{num_trials_2}")

if ok_2 == num_trials_2:
	print("no decoding errors observed, as expected for up to 1 channel error.")
else:
	print("some decoding errors observed.")
