import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

API_URL = "https://aes.cryptohack.org/ecb_oracle"

def get_encrypted_data(data: str) -> bytes:
    """
    Надсилає запит до серверного API та повертає зашифровані дані у вигляді байтів.
    """
    response = requests.get(f"{API_URL}{data}/")
    if response.status_code == 200:
        try:
            json_response = response.json()
            return bytes.fromhex(json_response["ciphertext"])
        except ValueError:
            print("Не вдалося обробити відповідь як JSON")
            print(response.text)
            return None
    else:
        print(f"Помилка: {response.status_code}")
        print(response.text)
        return None

def detect_block_size() -> int:
    """
    Визначає розмір блоку, який використовує шифрування (найчастіше AES = 16).
    """
    initial_length = len(get_encrypted_data("A"))
    i = 2
    while True:
        data = "A" * i
        new_length = len(get_encrypted_data(data))
        if new_length > initial_length:
            return new_length - initial_length
        i += 1

def is_ecb_mode(block_size: int) -> bool:
    """
    Перевіряє, чи дійсно використовується режим ECB (однакові блоки дають однаковий результат).
    """
    test_input = "A" * (block_size * 4)
    encrypted = get_encrypted_data(test_input)
    blocks = [encrypted[i:i+block_size] for i in range(0, len(encrypted), block_size)]
    return len(blocks) != len(set(blocks))  

def decrypt_flag():
    block_size = detect_block_size()
    print(f"[+] Block size: {block_size}")

    if not is_ecb_mode(block_size):
        print("[-] Не ECB режим!")
        return

    print("[+] Режим ECB підтверджено.")

    known_bytes = b""
    max_flag_length = 64  

    for i in range(max_flag_length):
        padding_length = block_size - (len(known_bytes) % block_size) - 1
        padding = b"A" * padding_length
        encrypted_block = get_encrypted_data(padding.decode())

        block_index = (len(known_bytes) // block_size) * block_size
        target_block = encrypted_block[block_index:block_index + block_size]

        found = False
        for b in range(32, 127): 
            guess = padding + known_bytes + bytes([b])
            encrypted_guess = get_encrypted_data(guess.decode())
            guess_block = encrypted_guess[block_index:block_index + block_size]
            if guess_block == target_block:
                known_bytes += bytes([b])
                print(f"[+] Знайдено: {known_bytes.decode(errors='ignore')}")
                found = True
                break

        if not found:
            print("[!] Дальше не знайдено символів. Можливо, кінець FLAG.")
            break

        if known_bytes.endswith(b'}'):
            print("[+] Завершено! FLAG знайдено.")
            break

    return known_bytes.decode()

if __name__ == "__main__":
    flag = decrypt_flag()
    print(f"\n[✔] FLAG: {flag}")
