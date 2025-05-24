from argon2 import PasswordHasher

# Ініціалізація хешера
ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16
)

# Список паролів
passwords = [
    "qwertyuiop",
    "sofPed-westag-jejzo1",
    "f3Fg#Puu$EA1mfMx2",
    "TIMCfJDkKBRm9/zwcFbHhE6zaMcSxR7nke1mJKcVqXpvCzg69d7Mf2quanMoAfmPJXyqT4gyGpLoL1lTHoqmwVmaUwrpOPRecB8GAU17eUJJHiksv3qrqcVxhgpMkX/UlKaLdFSwFIr7cVoJmBqQ/buWzxJNCIo7qbtIi3fSi62NwMHh"
]

# Хешування
hashes = [ph.hash(pw) for pw in passwords]

# Запис до файлу
with open("hashed_passwords.txt", "w") as f:
    for h in hashes:
        f.write(h + "\n")
