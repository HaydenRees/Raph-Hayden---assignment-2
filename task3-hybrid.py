from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import os.path

# used code from lectorial 5 to allow paths to work on all operating systems
BASE = os.path.dirname(os.path.abspath(__file__))

# used code from lectorial 5, file: rsa_pycryptodome_file.py to generate an RSA key pair
# and store it in the keys directory.
def generate_keys():
    key = RSA.generate(3072)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Ensures the keys directory exists before saving files to it
    os.makedirs(os.path.join(BASE, "keys"), exist_ok=True)

    # Save private key to keys directory
    with open(os.path.join(BASE, "keys", "private.cryptodome.pem"), "wb") as private:
        private.write(private_key)

    # Save public key to keys directory
    with open(os.path.join(BASE, "keys", "public.cryptodome.pem"), "wb") as public:
        public.write(public_key)

    return private_key, public_key

def generate_aes_key_and_iv():
    key = get_random_bytes(32)
    iv = get_random_bytes(16)

    return key, iv








