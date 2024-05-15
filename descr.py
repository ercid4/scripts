#!/usr/bin/env python3

import os
import zipfile
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_files_in_directory(directory, key):
    cipher = AES.new(key, AES.MODE_ECB)
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path == "descr.py" or file_path.endswith(".zip"):
                continue
            with open(file_path, "rb") as f:
                content = f.read()
            try:
                decrypted_content = unpad(cipher.decrypt(content), AES.block_size)
                with open(file_path, "wb") as f:
                    f.write(decrypted_content)
            except ValueError:  # Raised when the padding is incorrect
                print(f"{file_path} no está encriptado o ya ha sido desencriptado, saltándolo.")

def main():
    with zipfile.ZipFile("key.zip", "r") as zipf:
        zipf.setpassword(b"pauul")
        with zipf.open("key.key") as key_file:
            key = key_file.read()

    decrypt_files_in_directory(".", key)  # Decrypt files in current directory

if __name__ == "__main__":
    main()



