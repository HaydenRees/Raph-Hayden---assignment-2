import os
import os.path

BASE = os.path.dirname(os.path.abspath(__file__))
'calculation of GCD'
def gcd(a, b):
    while b!= 0:
        a, b = b, a % b
    return a

def multiplicativeInverse(e, phi):
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
    
def generateKeys():
    p = 2027
    q = 2039

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    d = multiplicativeInverse(e, phi)

    return (e, n), (d, n)

def encrypt(public_key, messageToEncrypt):
    e, n = public_key
    cipher = pow(messageToEncrypt, e, n)

    return cipher

def decrypt(private_key, cipherText):
    d, n = private_key
    plainText = pow(cipherText, d, n)

