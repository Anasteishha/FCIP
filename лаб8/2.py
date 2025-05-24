from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes

# Крок 1: Генерація ключової пари ECDSA
def generate_keys():
    # Генерація приватного ключа на кривій secp256k1
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()

    # Збереження приватного ключа у формат PEM 
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    # Збереження публічного ключа у формат PEM
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    print("Генерація ключів")
    print("Приватний ключ (PEM):")
    print(pem_private.decode())
    print("Публічний ключ (PEM):")
    print(pem_public.decode())

    return private_key, public_key

# Крок 2: Підпис повідомлення і перевірка підпису
def sign_and_verify(private_key, public_key):
    message = b"Hello, ECDSA!"  
    signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))

    print("\nПідпис і перевірка")
    print("Повідомлення для підпису:", message)
    print("Підпис (bytes):", signature)

    # Запис підпису у файл для збереження
    with open("signature.bin", "wb") as f:
        f.write(signature)

    # Перевірка підпису за допомогою публічного ключа
    try:
        public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        print("Перевірка підпису: підпис вірний!")
    except Exception:
        print("Перевірка підпису: підпис некоректний!")

# Крок 3: Реалізація протоколу Еліптичного Діффі-Геллмана (ECDH) на заданій кривій
class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    # Обчислення оберненого елемента по модулю p
    def inverse_mod(self, x):
        return pow(x, self.p - 2, self.p)

    # Додавання двох точок на кривій
    def point_add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        if P != Q:
            # Формула для додавання двох різних точок
            lamb = ((y2 - y1) * self.inverse_mod(x2 - x1)) % self.p
        else:
            # Формула для подвоєння точки
            if y1 == 0:
                return None
            lamb = ((3 * x1 * x1 + self.a) * self.inverse_mod(2 * y1)) % self.p

        x3 = (lamb * lamb - x1 - x2) % self.p
        y3 = (lamb * (x1 - x3) - y1) % self.p

        return (x3, y3)

    # Множення точки на скаляр k 
    def scalar_mult(self, k, P):
        R = None  
        Q = P
        while k > 0:
            if k & 1:
                R = self.point_add(R, Q)
            Q = self.point_add(Q, Q)
            k >>= 1
        return R

def ecdh_demo():
    print("\nECDH на власній кривій")
    curve = EllipticCurve(a=2, b=3, p=97)
    G = (3, 6)

    a = 5 
    b = 7 
    # Обчислення відкритих ключів 
    A = curve.scalar_mult(a, G)
    B = curve.scalar_mult(b, G)

    print("Відкритий ключ A = aG =", A)
    print("Відкритий ключ B = bG =", B)

    # Обчислення спільного секрету
    S1 = curve.scalar_mult(a, B)
    S2 = curve.scalar_mult(b, A)

    print("Спільний секрет, обчислений як aB =", S1)
    print("Спільний секрет, обчислений як bA =", S2)
    print("Секрет однаковий:", S1 == S2)

    with open("shared_secret.txt", "w") as f:
        f.write(str(S1))

# Головна частина
if __name__ == "__main__":
    priv_key, pub_key = generate_keys()
    sign_and_verify(priv_key, pub_key)
    ecdh_demo()
