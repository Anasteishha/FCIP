from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# Відкритий ключ лектора (PEM) — завантажуємо з файлу
with open("lector_pub.pem", "rb") as f:
    pem_public_key = f.read()

public_key = load_pem_public_key(pem_public_key)
message_text = "Я зашифрувала це повідомлення власноруч"  
message = message_text.encode('utf-8')  

# Шифруємо повідомлення за допомогою RSA-OAEP
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Записуємо зашифроване повідомлення у файл
with open("encrypted_message.bin", "wb") as f:
    f.write(ciphertext)

print("Повідомлення зашифроване і збережене у 'encrypted_message.bin'.")
