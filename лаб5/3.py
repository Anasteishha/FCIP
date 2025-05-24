import hashlib
import os
import json

def derive_key(username, password):
    # Генерація випадкової "солі" для кожного користувача
    salt = os.urandom(16)  # 16 байт для солі (рекомендовано для AES-128)
    
    # Використовуємо PBKDF2 для отримання криптографічного ключа
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)  # 100000 ітерацій

    # Переконуємося, що ключ має правильну довжину (16 байт для AES-128)
    key = key[:16]

    # Зберігаємо соль та параметри користувача в JSON-файл
    user_data = {
        "username": username,
        "salt": salt.hex(),  # зберігаємо соль у вигляді hex-стрічки
        "param": "value",    # додаткові параметри, які можна зберігати
    }

    # Записуємо дані у файл
    with open('user_data.json', 'a') as f:
        json.dump(user_data, f)
        f.write('\n')

    return key

# Приклад використання:
username = "John Doe"
password = "supersecretpassword"
key = derive_key(username, password)

print(f"Generated AES-128 key: {key.hex()}")
