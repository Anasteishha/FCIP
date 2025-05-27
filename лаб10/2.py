import hmac
import hashlib

# Виконує симетричний ключовий ланцюг
def kdf_chain(chain_key: bytes):
    message_key = hmac.new(chain_key, b'0', hashlib.sha256).digest()
    next_chain_key = hmac.new(chain_key, b'1', hashlib.sha256).digest()
    return message_key, next_chain_key
# Симуляція обміну кількома повідомленнями
def simulate_message_exchange(initial_chain_key: bytes, count: int):
    print("Стартова симуляція Double Ratchet\n")
    ck = initial_chain_key
    for i in range(count):
        message_key, ck = kdf_chain(ck)
        print(f"Повідомлення {i+1}:")
        print(f"Message Key: {message_key.hex()}")
        print(f"New Chain Key: {ck.hex()}\n")

if __name__ == "__main__":
    # Початковий ланцюговий ключ 
    initial_chain_key = b'super_secret_root_key_32_bytes_lng'
    simulate_message_exchange(initial_chain_key, count=5)

