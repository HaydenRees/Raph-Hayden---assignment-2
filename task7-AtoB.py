from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import os.path

BASE = os.path.dirname(os.path.abspath(__file__))

os.makedirs(os.path.join(BASE, "keys"), exist_ok=True)
os.makedirs(os.path.join(BASE, "output"), exist_ok=True)

def get_user_input():
    studentId = input("Enter your student ID (numbers only): ")
    firstName = input("Enter your first name: ")
    lastName = input("Enter your last name: ")

    prime1 = int(input("Enter prime 1 (>1,000,000): "))
    prime2 = int(input("Enter prime 2 (>1,000,000): "))

    plainText = input("Enter plaintext message (min 3 alphabetic chars): ")

    return studentId, firstName, lastName, prime1, prime2, plainText

def encryption(prime1, prime2, plainText, keyPath, cipherPath):

    n = prime1 * prime2
    e = 65537

    key = RSA.construct(n, e)

    