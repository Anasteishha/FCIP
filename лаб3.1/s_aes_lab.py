SBOX = {
    0x0: 0x9, 0x1: 0x4, 0x2: 0xA, 0x3: 0xB,
    0x4: 0xD, 0x5: 0x1, 0x6: 0x8, 0x7: 0x5,
    0x8: 0x6, 0x9: 0x2, 0xA: 0x0, 0xB: 0x3,
    0xC: 0xC, 0xD: 0xE, 0xE: 0xF, 0xF: 0x7,
}
SBOX_INV = {v: k for k, v in SBOX.items()}

def sub_nib(b):
    return (SBOX[(b >> 4) & 0xF] << 4) | SBOX[b & 0xF]

def sub_nib_inv(b):
    return (SBOX_INV[(b >> 4) & 0xF] << 4) | SBOX_INV[b & 0xF]

def key_expansion(key):
    w = [0]*6
    w[0] = (key >> 8) & 0xFF
    w[1] = key & 0xFF
    RCON = [0x80, 0x30]
    for i in range(2):
        t = sub_nib((w[2*i+1] >> 4 | (w[2*i+1] << 4)) & 0xFF)
        t ^= RCON[i]
        w[2*i+2] = w[2*i] ^ t
        w[2*i+3] = w[2*i+1] ^ w[2*i+2]
    return [((w[0] << 8) | w[1]), ((w[2] << 8) | w[3]), ((w[4] << 8) | w[5])]

def shift_rows(s):
    s0 = (s >> 12) & 0xF
    s1 = (s >> 8) & 0xF
    s2 = (s >> 4) & 0xF
    s3 = s & 0xF
    return (s0 << 12) | (s3 << 8) | (s2 << 4) | (s1)

def shift_rows_inv(s):
    s0 = (s >> 12) & 0xF
    s1 = (s >> 8) & 0xF
    s2 = (s >> 4) & 0xF
    s3 = s & 0xF
    return (s0 << 12) | (s3 << 8) | (s2 << 4) | (s1)

def gf_mul(a, b):
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        hi = a & 0x8
        a <<= 1
        if hi:
            a ^= 0b10011
        b >>= 1
    return p & 0xF

def mix_columns(s):
    s0 = (s >> 12) & 0xF
    s1 = (s >> 8) & 0xF
    s2 = (s >> 4) & 0xF
    s3 = s & 0xF

    r0 = gf_mul(s0, 1) ^ gf_mul(s1, 4)
    r1 = gf_mul(s0, 4) ^ gf_mul(s1, 1)
    r2 = gf_mul(s2, 1) ^ gf_mul(s3, 4)
    r3 = gf_mul(s2, 4) ^ gf_mul(s3, 1)

    return (r0 << 12) | (r1 << 8) | (r2 << 4) | r3

def inv_mix_columns(s):
    s0 = (s >> 12) & 0xF
    s1 = (s >> 8) & 0xF
    s2 = (s >> 4) & 0xF
    s3 = s & 0xF

    r0 = gf_mul(s0, 9) ^ gf_mul(s1, 2)
    r1 = gf_mul(s0, 2) ^ gf_mul(s1, 9)
    r2 = gf_mul(s2, 9) ^ gf_mul(s3, 2)
    r3 = gf_mul(s2, 2) ^ gf_mul(s3, 9)

    return (r0 << 12) | (r1 << 8) | (r2 << 4) | r3

def add_round_key(s, k):
    return s ^ k

def encrypt(p, key):
    w = key_expansion(key)
    state = add_round_key(p, w[0])
    state = (sub_nib((state >> 8) & 0xFF) << 8) | sub_nib(state & 0xFF)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, w[1])
    state = (sub_nib((state >> 8) & 0xFF) << 8) | sub_nib(state & 0xFF)
    state = shift_rows(state)
    state = add_round_key(state, w[2])
    return state

def decrypt(c, key):
    w = key_expansion(key)
    state = add_round_key(c, w[2])
    state = shift_rows_inv(state)
    state = (sub_nib_inv((state >> 8) & 0xFF) << 8) | sub_nib_inv(state & 0xFF)
    state = add_round_key(state, w[1])
    state = inv_mix_columns(state)
    state = shift_rows_inv(state)
    state = (sub_nib_inv((state >> 8) & 0xFF) << 8) | sub_nib_inv(state & 0xFF)
    state = add_round_key(state, w[0])
    return state

# Тестування
pt = 0b1010011100110011
key = 0b0100101011110101
ct = encrypt(pt, key)
dec = decrypt(ct, key)

print(f"Plain:      {pt:016b}")
print(f"Encrypted:  {ct:016b}")
print(f"Decrypted:  {dec:016b}")
assert pt == dec, "Розшифрування не збігається з оригіналом!"
