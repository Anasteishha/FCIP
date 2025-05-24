from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# Завантаження відкритого ключа
with open("lector_pub.pem", "rb") as f:
    public_key = load_pem_public_key(f.read())

# Завантаження повідомлення з hex
with open("lector_message.txt", "r") as msg_file:
    message = bytes.fromhex(msg_file.read().strip())

# Завантаження підпису з hex
with open("lector_signature.txt", "r") as sig_file:
    signature = bytes.fromhex(sig_file.read().strip())

# Перевірка підпису
try:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Підпис дійсний.")
except Exception as e:
    print("Підпис недійсний.")
    print("Причина:", str(e))
