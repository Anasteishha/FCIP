import struct

def rotate(v, c):
    return ((v << c) & 0xffffffff) | (v >> (32 - c))

def little_endian(b):
    return struct.unpack("<I", b)[0]

def to_bytes_le(val):
    return struct.pack("<I", val)

def chacha20_init_state(key: bytes, counter: int, nonce: bytes):
    constants = b"expand 32-byte k"
    key_words = [little_endian(key[i:i+4]) for i in range(0, 32, 4)]
    nonce_words = [little_endian(nonce[i:i+4]) for i in range(0, 12, 4)]

    return [
        little_endian(constants[0:4]), little_endian(constants[4:8]),
        little_endian(constants[8:12]), little_endian(constants[12:16]),
        *key_words,
        counter,
        *nonce_words
    ]

def quarter_round(state, a, b, c, d):
    state[a] = (state[a] + state[b]) & 0xffffffff
    state[d] ^= state[a]
    state[d] = rotate(state[d], 16)

    state[c] = (state[c] + state[d]) & 0xffffffff
    state[b] ^= state[c]
    state[b] = rotate(state[b], 12)

    state[a] = (state[a] + state[b]) & 0xffffffff
    state[d] ^= state[a]
    state[d] = rotate(state[d], 8)

    state[c] = (state[c] + state[d]) & 0xffffffff
    state[b] ^= state[c]
    state[b] = rotate(state[b], 7)

def chacha20_block(key, counter, nonce):
    state = chacha20_init_state(key, counter, nonce)
    working_state = state[:]

    for _ in range(10):  
        quarter_round(working_state, 0, 4, 8, 12)
        quarter_round(working_state, 1, 5, 9, 13)
        quarter_round(working_state, 2, 6, 10, 14)
        quarter_round(working_state, 3, 7, 11, 15)
   
        quarter_round(working_state, 0, 5, 10, 15)
        quarter_round(working_state, 1, 6, 11, 12)
        quarter_round(working_state, 2, 7, 8, 13)
        quarter_round(working_state, 3, 4, 9, 14)

    for i in range(16):
        working_state[i] = (working_state[i] + state[i]) & 0xffffffff

    return b''.join(to_bytes_le(word) for word in working_state)

def chacha20_encrypt(key, nonce, counter, plaintext):
    ciphertext = bytearray()
    block_count = 0

    for i in range(0, len(plaintext), 64):
        block = chacha20_block(key, counter + block_count, nonce)
        block_count += 1
        chunk = plaintext[i:i+64]
        keystream = block[:len(chunk)]
        ciphertext += bytes([a ^ b for a, b in zip(chunk, keystream)])

    return bytes(ciphertext)

# Симетричний процес: дешифрування — те саме, що шифрування
chacha20_decrypt = chacha20_encrypt

key = b"0123456789abcdef0123456789abcdef"
nonce1 = b"abc123456789"
nonce2 = b"xyz987654321"
plaintext = b"Hello, ChaCha20!"

# Тест 1: однаковий nonce і лічильник
cipher1 = chacha20_encrypt(key, nonce1, 1, plaintext)
plain1 = chacha20_decrypt(key, nonce1, 1, cipher1)

# Тест 2: інший nonce
cipher2 = chacha20_encrypt(key, nonce2, 1, plaintext)

# Тест 3: інший лічильник
cipher3 = chacha20_encrypt(key, nonce1, 2, plaintext)

print("Оригінал:", plaintext)
print("Шифртекст 1:", cipher1)
print("Розшифр. 1:", plain1)
print("Шифртекст 2 (інший nonce):", cipher2)
print("Шифртекст 3 (інший лічильник):", cipher3)
