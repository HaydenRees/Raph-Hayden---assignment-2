# The pycryptodome library is used for all the cryptography
# The Pillow library is used to open the image as well as attach a comment (in this case the encrypted message) to the metadata
# The base64 library is used only to encode binary data into text, not for encryption
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from PIL import Image
import base64
import os
import os.path

# used code from lectorial 5 files: rsa_pycryptodome_file.py
# 1. to allow paths to work on all operating systems
# 2. to ensure the keys and output directories exist before saving files to them
BASE = os.path.dirname(os.path.abspath(__file__))

os.makedirs(os.path.join(BASE, "keys"), exist_ok=True)
os.makedirs(os.path.join(BASE, "output"), exist_ok=True)

# used code from lectorial 5 files: aes_ofb_string.py
# 1. To generate a 32 byte key and a 16 byte random value using get_random_bytes()
def generate_aes_key_and_iv():
    key = get_random_bytes(32)
    iv = get_random_bytes(16)

    return key, iv

# used code from lectorial 5 files: aes_ofb_string.py, aes_cfb_file.py and rsa_pycryptodome_file.py
# 1. to encode the string into bytes to then be encrypted by AES
# 2. To create a new AES cipher using CFB mode
# 3. to write the AES key to the keys directory
def aes_encryption(message, key, iv, aes_key_path):
    message_bytes = message.encode()
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_message = iv + cipher.encrypt(message_bytes)

    with open(aes_key_path, "wb") as aes_key_file:
        aes_key_file.write(key)

    return encrypted_message

# The function uses Pillow's save method with the optional comment parameter which stores the base64 encoded ciphertext into the JPEG file's metadata
def embed_comment(encrypted_message, input_image_path, output_path):
    # Takes the binary ciphertext and turns it into a text compatible format
    encoded_message = base64.b64encode(encrypted_message)

    with Image.open(input_image_path) as img:
        img.save(output_path, "JPEG", comment=encoded_message)

    return encoded_message

# Uses .info.get("comment") to safely retrieve the encoded comment from the stego image
def extract_comment(stego_image_path):
    with Image.open(stego_image_path) as stego_img:
        encoded_comment = stego_img.info.get("comment")

    # if no comment is found in the stego image metadata, print a message to the user and return early
    if encoded_comment == None:
        print("No message was found in image metadata")
        return None
    # converts base64 format into bytes
    encrypted_data = base64.b64decode(encoded_comment)

    # the returned data contains the IV followed by the ciphertext
    return encrypted_data

# Uses code from lectorial 5 files: aes_cfb_file.py
# 1. to create a new AES cipher in CFB mode to decrypt the comment
# 2. to ensure the comment was returned to a string format using .decode()
def decrypt_comment(encrypted_data, aes_key_path):
    # splits the first 16 bytes from the rest
    iv = encrypted_data[:16]
    # the rest of the data is assigned as the encrypted comment
    encrypted_comment = encrypted_data[16:]

    with open(aes_key_path, "rb") as aes_key_file:
        key = aes_key_file.read()

    cipher_decrypt = AES.new(key, AES.MODE_CFB, iv)

    comment_bytes = cipher_decrypt.decrypt(encrypted_comment)
    # .decode() to return to the original string
    comment_string = comment_bytes.decode()

    return comment_string

if __name__ == "__main__":
    image_path = os.path.join(BASE, "input", "image.jpg")
    image_aes_key_path = os.path.join(BASE, "keys", "image_aes_key")
    stego_image_path = os.path.join(BASE, "output", "stego_image.jpg")

    message = ""

    while not message.strip():
        message = input("Enter a message that will be hidden: ")
    
    key, iv = generate_aes_key_and_iv()
    encrypted_data = aes_encryption(message, key, iv, image_aes_key_path)
    encoded_message = embed_comment(encrypted_data, image_path, stego_image_path)
    extracted_data = extract_comment(stego_image_path)

    # stops the program from continuing to decryption if no comment exists in the stego image metadata
    if extracted_data is not None:
        recovered_message = decrypt_comment(extracted_data, image_aes_key_path)

        # Checking if the recovered message matches the message entered by the user
        if message == recovered_message:
            message_match = True
        else:
            message_match = False

        # prints all values necessary, using .decode() and .hex() to improve readability
        print("Original Message:", message)
        print("AES Key:", key.hex())
        print("IV:", iv.hex())
        print("Encrypted Data:", encrypted_data.hex())
        print("Base64 Text:", encoded_message.decode())
        print("Recovered Message:", recovered_message)
        print("Messages Match:", message_match)


    