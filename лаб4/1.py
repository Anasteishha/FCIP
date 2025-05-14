import requests
from pwn import xor
# Отримання шифртексту для "00"*32
plaintext = "00" * 32
enc_url = f"https://aes.cryptohack.org/lazy_cbc/encrypt/{plaintext}/"
response = requests.get(enc_url).json()
# Перевірка отримання шифртексту
if 'ciphertext' in response:
    ciphertext = response['ciphertext']
    print("Ciphertext received:", ciphertext)
    # Розділ на блоки по 32 hex символи = 16 байт
    C0 = ciphertext[:32]
    C1 = ciphertext[32:]
    # Формування нового шифртексту (правильно формуємо шифртекст)
    zero_block = "00" * 16  # "0000000000000000" - 16 нулів
    crafted_ciphertext = C0 + zero_block + C0  # C0 + zero_block + C0
    # Дебаг: введення сформованого шифртексту для перевірки
    print("Crafted ciphertext:", crafted_ciphertext)
    # Відправка у receive
    recv_url = f"https://aes.cryptohack.org/lazy_cbc/receive/{crafted_ciphertext}/"
    recv_response = requests.get(recv_url).json()
    # Дебаг: введення відповіді сервера для перевірки
    print("Response from receive:", recv_response)
    # Перевірка, чи є помилка у форматі hex
    if 'error' in recv_response:
        print("Error returned by server:", recv_response['error'])
        try:
            # Отримання розшифрованих даних у hex
            plaintext_blocks = bytes.fromhex(recv_response['error'].replace("Invalid plaintext: ", ""))
            # Відновлення P0 і P2
            P0 = plaintext_blocks[:16]
            P2 = plaintext_blocks[32:48]
            # Відновлення KEY = P0 ⊕ P2
            key = xor(P0, P2).hex()
            print("KEY:", key)
            # Отримання флагу
            flag_url = f"https://aes.cryptohack.org/lazy_cbc/get_flag/{key}/"
            flag_response = requests.get(flag_url).json()
            print("FLAG:", flag_response['plaintext'])

        except ValueError:
            print("Received error in non-hex format:", recv_response['error'])
    else:
        print("No error in response. Full response:", recv_response)

else:
    print("Failed to retrieve ciphertext:", response)
