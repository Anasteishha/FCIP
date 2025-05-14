from chacha20 import chacha20_encrypt, chacha20_decrypt

# Визначаємо ключ, nonce, лічильник і текст для шифрування
key = b"0123456789abcdef0123456789abcdef"
nonce1 = b"abc123456789"  # перший nonce
nonce2 = b"xyz987654321"  # другий nonce
plaintext = b"Hello, ChaCha20!"

# Тест 1: однаковий nonce і лічильник
cipher1 = chacha20_encrypt(key, nonce1, 1, plaintext)
plain1 = chacha20_decrypt(key, nonce1, 1, cipher1)

# Тест 2: інший nonce
cipher2 = chacha20_encrypt(key, nonce2, 1, plaintext)

# Тест 3: інший лічильник
cipher3 = chacha20_encrypt(key, nonce1, 2, plaintext)

# Виведення результатів
print("Оригінал:", plaintext)
print("Шифртекст 1:", cipher1)
print("Розшифрований 1:", plain1)
print("Шифртекст 2 (інший nonce):", cipher2)
print("Шифртекст 3 (інший лічильник):", cipher3)
