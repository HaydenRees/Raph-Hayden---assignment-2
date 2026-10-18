import os
import os.path

# Allow paths to work on all operating systems
BASE = os.path.dirname(os.path.abspath(__file__))
#calculation of GCD using euclidian algorithm
def gcd(a, b):
    while b!= 0:
        a, b = b, a % b
    return a
#Using extended Euclidian algorithm to find private key exponent
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
#generating keys (pub + priv)
def generateKeys():
    p = 2027
    q = 2039

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    d = multiplicativeInverse(e, phi)

    return (e, n), (d, n)
#encryptes messageToEncrypte using public key
def encrypt(public_key, messageToEncrypt):
    e, n = public_key
    cipher = pow(messageToEncrypt, e, n)

    return cipher
#decrypts ciphertext using private key
def decrypt(private_key, cipherText):
    d, n = private_key
    plainText = pow(cipherText, d, n)

    return plainText

if __name__ == '__main__':

    inputDir = os.path.join(BASE, 'input')
    os.makedirs(inputDir, exist_ok=True)
    task2_file = os.path.join(inputDir, 'task2.txt')

    studentID_str = "3844483"
    messageInt = int(studentID_str)

    publicKey, privateKey = generateKeys()
    print("Public Key (e, n): ", publicKey)
    print("Private Key (d, n): ", privateKey)

    encryptedMsg = encrypt(publicKey, messageInt)
    print("Encrypted int: ", encryptedMsg)

    decryptMsgInt = decrypt(privateKey, encryptedMsg)
    decryptedMsgStr = str(decryptMsgInt)
    print("Decrypted string: ", decryptedMsgStr)

    with open(task2_file, 'w') as f:
        f.write(decryptedMsgStr)