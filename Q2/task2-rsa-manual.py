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
def generateKeys(public_key_path, private_key_path):
    p = 2027
    q = 2039

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    d = multiplicativeInverse(e, phi)

    # writing formatted public and private key pairs to their separate files
    with open(public_key_path, "wt") as public_key_file:
        public_key_file.write(f"{e}, {n}")

    with open(private_key_path, "wt") as private_key_file:
        private_key_file.write(f"{d}, {n}")

    return (e, n), (d, n)
#encryptes messageToEncrypte using public key
def encrypt(public_key, messageToEncrypt, encrypted_message_path):
    e, n = public_key
    cipher = pow(messageToEncrypt, e, n)

    # writing encrypted message to file
    with open(encrypted_message_path, "wt") as encrypted_message_file:
        encrypted_message_file.write(f"{cipher}")

    return cipher
#decrypts ciphertext using private key
def decrypt(private_key, cipherText, decrypted_message_path):
    d, n = private_key
    plainText = pow(cipherText, d, n)

    # writing decrypted message to file
    with open(decrypted_message_path, "wt") as decrypted_message_file:
            decrypted_message_file.write(f"{plainText}")

    return plainText

if __name__ == '__main__':

    # creating paths for necessary files, using BASE in order for it to work on all operating systems
    inputDir = os.path.join(BASE, 'input')
    os.makedirs(inputDir, exist_ok=True)
    public_key_path = os.path.join(BASE, "keys", "public_key.txt")
    private_key_path = os.path.join(BASE, "keys", "private_key.txt")
    encrypted_message_path = os.path.join(BASE, "output", "encrypted_message.txt")
    decrypted_message_path = os.path.join(BASE, "output", "decrypted_message.txt")

    studentID_str = "3844483"
    messageInt = int(studentID_str)

    publicKey, privateKey = generateKeys(public_key_path, private_key_path)
    print("Public Key (e, n): ", publicKey)
    print("Private Key (d, n): ", privateKey)

    encryptedMsg = encrypt(publicKey, messageInt, encrypted_message_path)
    print("Encrypted int: ", encryptedMsg)

    decryptMsgInt = decrypt(privateKey, encryptedMsg, decrypted_message_path)
    decryptedMsgStr = str(decryptMsgInt)
    print("Decrypted string: ", decryptedMsgStr)
