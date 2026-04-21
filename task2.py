import random

# message space
messages = [
    "000","001","010","011",
    "100","101","110","111"
]

#given codebook 
codebook = [
"0000000","1000110","0100101","1100011",
"0010011","1010101","0110110","1110000",
"0001111","1001001","0101010","1101100",
"0011100","1011010","0111001","1111111"
]

# XOR strings
def xor_bits(a, b):
    return "".join(str(int(x)^int(y)) for x, y in zip(a, b))

# encoder
def random_binning_encoder(d):
    
    # compute complement d_bar = d XOR 111
    d_bar = xor_bits(d, "111")
    
    valid_codewords = []
    
    for cw in codebook:
        prefix = cw[:4]
        
        # check prefix rule
        if prefix == "0" + d or prefix == "1" + d_bar:
            valid_codewords.append(cw)
    
    # must have exactly 2 codewords
    if len(valid_codewords) != 2:
        print("Error: bin size is not 2")
    
    # choose randomly
    chosen = random.choice(valid_codewords)
    
    return chosen, valid_codewords


# verification 
print("Testing encoder with different messages:\n")

for d in messages:
    chosen, bin_set = random_binning_encoder(d)
    
    print(f"message: {d}")
    print(f"bin: {bin_set}")
    print(f"chosen codeword: {chosen}")
    print("-" * 40)
