def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def modular_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None  
    return x % m  

# Задані значення
a, n = 176, 2027
inverse = modular_inverse(a, n)
if inverse:
    print(f"Обернений елемент для {a} mod {n}: {inverse}")
    # Перевірка
    print(f"Перевірка: ({a} * {inverse}) % {n} = {(a * inverse) % n}")
else:
    print(f"Оберненого елемента для {a} mod {n} не існує.")
