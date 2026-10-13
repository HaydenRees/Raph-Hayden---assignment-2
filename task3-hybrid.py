

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import os.path

# used code from lectorial 5 to allow paths to work on all operating systems
BASE = os.path.dirname(os.path.abspath(__file__))

# Ensures the keys and output directories exist before saving files to them
os.makedirs(os.path.join(BASE, "keys"), exist_ok=True)
os.makedirs(os.path.join(BASE, "output"), exist_ok=True)

# used code from lectorial 5 files: rsa_pycryptodome_file.py 
# 1. to generate an RSA key pair
# 2. store the RSA key pair in the keys directory.
def generate_keys():
    key = RSA.generate(3072)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Save private key to keys directory
    with open(os.path.join(BASE, "keys", "private.cryptodome.pem"), "wb") as private:
        private.write(private_key)

    # Save public key to keys directory
    with open(os.path.join(BASE, "keys", "public.cryptodome.pem"), "wb") as public:
        public.write(public_key)

    return private_key, public_key

# used code from lectorial 5 files: aes_ofb_string.py
# 1. To generate a 16 byte random value using get_random_bytes()
def generate_aes_key_and_iv():
    key = get_random_bytes(32)
    iv = get_random_bytes(16)

    return key, iv

# used code from lectorial 5 files: aes_cfb_file.py, aes_ofb_string.py
# 1. to create an AES cipher using CFB mode 
# 2. to open the input file to encrypt the contents
def aes_encryption(input_file_path, output_file_path, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    with open(input_file_path, 'rb') as in_file:
        encrypted_data = cipher.encrypt(in_file.read())

    with open(output_file_path, 'wb') as out_file:
        out_file.write(iv + encrypted_data)

    return encrypted_data

# used code from lectorial 5 files: rsa_pycryptodome_file.py 
# 1. to create the OAEP cipher 
# 2. encrypt the AES key using that cipher
# 3. write the encrypted AES key to a file
def encrypt_aes_key(aes_key, public_key_path, output_file_path):
    with open(public_key_path, "rb") as in_file:
        public_key = RSA.import_key(in_file.read())

    cipher = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher.encrypt(aes_key)

    with open(output_file_path, "wb") as out_file:
        out_file.write(encrypted_aes_key)

    return encrypted_aes_key

# used code from lectorial 5 files: rsa_pycryptodome_file.py
# 1. to decrypt the AES key using the .decrypt() method
def decrypt_aes_key(encrypted_aes_key_path, private_key_path):
    with open(encrypted_aes_key_path, "rb") as aes_key_file:
        encrypted_aes_key = aes_key_file.read() 

    with open(private_key_path, "rb") as private_key_file:
        private_key = RSA.import_key(private_key_file.read())

    cipher = PKCS1_OAEP.new(private_key)
    aes_key = cipher.decrypt(encrypted_aes_key)

    return aes_key

# Used code from lectorial 5 files: aes_cfb_file.py
# 1. To read the encrypted file
# 2. To split the 16 bytes IV from the encrypted data
# 3. To generate an AES cipher in CFB mode
# 4. To decrypt the encrypted data
# 5. To write the decrypted data to an output file 
def aes_decryption(aes_key, encrypted_file_path, output_file_path):
    with open(encrypted_file_path, "rb") as encrypted_file:
        iv = encrypted_file.read(16)
        encrypted_data = encrypted_file.read()

    cipher_decrypt = AES.new(aes_key, AES.MODE_CFB, iv)
    decrypted_data = cipher_decrypt.decrypt(encrypted_data)

    with open(output_file_path, "wb") as out_file:
        out_file.write(decrypted_data)

    return decrypted_data, iv


if __name__ == "__main__":
    input_path = os.path.join(BASE, "input", "task2.txt")
    public_key_path = os.path.join(BASE, "keys", "public.cryptodome.pem")
    private_key_path = os.path.join(BASE, "keys", "private.cryptodome.pem")
    enc_aes_key_path = os.path.join(BASE, "keys", "enc_aes_key")
    enc_task2_path = os.path.join(BASE, "output", "task2_enc")
    dec_task2_path = os.path.join(BASE, "output", "task2_dec.txt")

    # RSA private and public keys
    private_key, public_key = generate_keys()
    # AES key and IV
    key, iv = generate_aes_key_and_iv()
    # Encrypted Task 2
    enc_task2 = aes_encryption(input_path, enc_task2_path, key, iv)
    # Encrypted AES key
    enc_aes_key = encrypt_aes_key(key, public_key_path, enc_aes_key_path)
    # Decrypted AES key by friend
    dec_aes_key = decrypt_aes_key(enc_aes_key_path, private_key_path)
    # Decrypted Task 2 and recovered IV by friend
    dec_task2, recovered_iv = aes_decryption(dec_aes_key, enc_task2_path, dec_task2_path)

    # saves the contents of the original input file for comparison
    with open(input_path, "rb") as input_file:
        original_input = input_file.read()

    # compares the original values and verifies they match after decryption
    if original_input == dec_task2:
        file_match = True
    else:
        file_match = False

    if key == dec_aes_key:
        key_match = True
    else:
        key_match = False

    if iv == recovered_iv:
        iv_match = True
    else:
        iv_match = False


    # prints all values required
    print("RSA Private Key:", private_key.decode())
    print("RSA Public Key:", public_key.decode())
    print("AES Key:", key.hex())
    print("IV:", iv.hex())
    print("Encrypted AES Key:", enc_aes_key.hex())
    print("Recovered IV:", recovered_iv.hex())
    print("Decrypted AES Key:", dec_aes_key.hex())
    print("Encrypted Data:", enc_task2.hex())
    print("Decrypted Data:", dec_task2.decode())
    print("Files Match:", file_match)
    print("AES Keys Match:", key_match)
    print("IVs Match:", iv_match)


