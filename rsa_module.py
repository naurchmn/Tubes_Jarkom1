import random
from math import gcd

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_large_prime():
    while True:
        num = random.randint(100, 500)
        if is_prime(num):
            return num

def mod_inverse(e, phi):
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi, e = e, temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2, x1 = x1, x
        d, y1 = y1, y

    if temp_phi == 1:
        return d + phi

def generate_keys():
    p = generate_large_prime()
    q = generate_large_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(message, public_key):
    e, n = public_key
    cipher = [(ord(char) ** e) % n for char in message]
    hex_cipher = [format(part, 'x') for part in cipher]  # konversi int ke hex
    cipher_text = ' '.join(hex_cipher)  #pake blank sbg separator
    return cipher_text

def decrypt(cipher_text, private_key):
    d, n = private_key
    hex_cipher = cipher_text.strip().split(' ')
    cipher = [int(part, 16) for part in hex_cipher]
    plain = [chr((char ** d) % n) for char in cipher]
    return ''.join(plain)
