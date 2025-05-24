from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# 1. Генерація ключів RSA і збереження у файли
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

with open("student_private.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("student_public.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("Ключі згенеровано та збережено у файли student_private.pem і student_public.pem.")

# 2. Зашифрувати повідомлення відкритим ключем

message = "Я зашифрувала це повідомлення власноруч".encode('utf-8')  # тепер це bytes # Твоє текстове повідомлення
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Завантаження публічного ключа з файлу
with open("student_public.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open("encrypted_message.bin", "wb") as f:
    f.write(ciphertext)

print("Повідомлення зашифроване та записане у encrypted_message.bin.")

# 3. Розшифрувати повідомлення приватним ключем

# Завантаження приватного ключа з файлу
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Завантаження зашифрованого повідомлення
with open("encrypted_message.bin", "rb") as f:
    encrypted_message = f.read()

decrypted_message = private_key.decrypt(
    encrypted_message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Розшифроване повідомлення:", decrypted_message.decode("utf-8"))

# 4. Записати розшифроване повідомлення у текстовий файл
with open("task-2-message.txt", "w", encoding="utf-8") as f:
    f.write(decrypted_message.decode("utf-8"))
