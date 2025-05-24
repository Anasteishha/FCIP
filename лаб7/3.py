from binascii import hexlify
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import dh, rsa, padding
from cryptography.hazmat.backends import default_backend

# 1. Генерація параметрів DH
parameters = dh.generate_parameters(generator=2, key_size=2048)
p = parameters.parameter_numbers().p
g = parameters.parameter_numbers().g
print("DH parameters:\np =", p, "\ng =", g)

# 2. Генерація ключів RSA (для підпису)
def generate_rsa_key_pair():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

# Alice генерує ключі
alice_dh_private = parameters.generate_private_key()
alice_dh_public = alice_dh_private.public_key()
alice_rsa_private = generate_rsa_key_pair()
alice_rsa_public = alice_rsa_private.public_key()

# Bob генерує ключі
bob_dh_private = parameters.generate_private_key()
bob_dh_public = bob_dh_private.public_key()
bob_rsa_private = generate_rsa_key_pair()
bob_rsa_public = bob_rsa_private.public_key()

# 3. Підпис Alice свого DH-ключа
alice_dh_bytes = alice_dh_public.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
alice_signature = alice_rsa_private.sign(
    alice_dh_bytes,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Bob перевіряє підпис Alice
try:
    alice_rsa_public.verify(
        alice_signature,
        alice_dh_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("\nBob: Підпис Alice перевірено успішно.")
except Exception as e:
    print("\nBob: Помилка перевірки підпису Alice:", e)

# 4. Підпис Bob свого DH-ключа
bob_dh_bytes = bob_dh_public.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
bob_signature = bob_rsa_private.sign(
    bob_dh_bytes,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Alice перевіряє підпис Bob
try:
    bob_rsa_public.verify(
        bob_signature,
        bob_dh_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Alice: Підпис Bob перевірено успішно.")
except Exception as e:
    print("Alice: Помилка перевірки підпису Bob:", e)

# 5. Обчислення спільного секрету
alice_shared = alice_dh_private.exchange(bob_dh_public)
bob_shared = bob_dh_private.exchange(alice_dh_public)

# 6. Вивід результатів
alice_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data'
).derive(alice_shared)

bob_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data'
).derive(bob_shared)

print("\nAlice derived key:", hexlify(alice_key))
print("Bob derived key:  ", hexlify(bob_key))
print("Keys match?", alice_key == bob_key)
