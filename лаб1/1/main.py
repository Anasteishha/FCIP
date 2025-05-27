import string
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

italian_alphabet = "ABCDEFGHILMNOPQRSTUVZabcdefghilmnopqrstuvz"

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shifted = chr(((ord(char.upper()) - 65 + shift) % 26) + 65)
            if char.islower():
                shifted = shifted.lower()
            result += shifted
        else:
            result += char
    return result

def vertical_permutation(text, key):
    while len(text) % len(key) != 0:
        text += ' '
    matrix = [text[i:i+len(key)] for i in range(0, len(text), len(key))]
    permuted_text = ''.join(''.join(row[i] for row in matrix) for i in sorted(range(len(key)), key=lambda x: key[x]))
    return permuted_text

def horizontal_permutation(text, key):
    while len(text) % len(key) != 0:
        text += ' '
    row_length = len(key)
    rows = [text[i:i + row_length] for i in range(0, len(text), row_length)]
    permuted_text = ''.join(rows[i] for i in sorted(range(len(rows)), key=lambda x: key[x % len(key)]))
    return permuted_text

def plot_histogram(text, title):
    letter_counts = Counter(char.upper() for char in text if char.isalpha() and char.upper() in italian_alphabet)
    letters = list(italian_alphabet.upper())
    frequencies = [letter_counts.get(letter, 0) for letter in letters]
    plt.figure(figsize=(10, 4))
    plt.bar(letters, frequencies)
    plt.title(title)
    plt.xlabel("Літери")
    plt.ylabel("Частота")
    plt.tight_layout()
    plt.show()

def chi_square_test(text, expected_freq):
    observed_freq = Counter(char.upper() for char in text if char.isalpha() and char.upper() in italian_alphabet)
    observed_counts = np.array([observed_freq.get(letter, 0) for letter in italian_alphabet.upper()])
    expected_counts = np.array([expected_freq] * len(italian_alphabet))
    chi_square = np.sum((observed_counts - expected_counts) ** 2 / expected_counts)
    return chi_square

if __name__ == "__main__":
    text = "La vita e bella"
    expected_freq = len(text) / len(italian_alphabet)

    caesar_encrypted = caesar_cipher(text, 3)
    print("Цезар зашифрований текст:", caesar_encrypted)
    plot_histogram(caesar_encrypted, "Гістограма: Шифр Цезаря")
    print(f"Хи-квадрат для шифру Цезаря: {chi_square_test(caesar_encrypted, expected_freq)}\n")

    key_vertical = [3, 1, 2]
    vertical_encrypted = vertical_permutation(text, key_vertical)
    print("Вертикальна перестановка:", vertical_encrypted)
    plot_histogram(vertical_encrypted, "Гістограма: Вертикальна перестановка")
    print(f"Хи-квадрат для вертикальної перестановки: {chi_square_test(vertical_encrypted, expected_freq)}\n")

    key_horizontal = [2, 1, 3]
    horizontal_encrypted = horizontal_permutation(text, key_horizontal)
    print("Горизонтальна перестановка:", horizontal_encrypted)
    plot_histogram(horizontal_encrypted, "Гістограма: Горизонтальна перестановка")
    print(f"Хи-квадрат для горизонтальної перестановки: {chi_square_test(horizontal_encrypted, expected_freq)}")
