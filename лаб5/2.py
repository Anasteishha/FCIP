from Crypto.Hash import CMAC
from Crypto.Cipher import AES

# Дано
key_hex = "63e353ae93ecbfe00271de53b6f02a46"
iv_hex = "75b777fc8f70045c6006b39da1b3d622"
ciphertext_hex = (
    "76c3ada7f1f7563ff30d7290e58fb4476eb12997d02a6488201c075da52ff3890260e2c89f631e7f919af96e4e47980a"
)

# Конвертація до байтів
key = bytes.fromhex(key_hex)
iv = bytes.fromhex(iv_hex)
ciphertext = bytes.fromhex(ciphertext_hex)

# Вхідні дані для MAC: IV + шифртекст
mac_data = iv + ciphertext

# Створення CMAC
cobj = CMAC.new(key, ciphermod=AES)
cobj.update(mac_data)
mac = cobj.hexdigest()

print("Імітовставка (MAC):", mac)
