#!/usr/bin/env python3

import os
import zipfile
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def desencrypt(directory, key):
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
            except ValueError:  
                print(f"{file_path} no está encriptado o ya ha sido desencriptado, saltándolo.")

def main():
    with zipfile.ZipFile("key.zip", "r") as zipf:
        zipf.setpassword(b"sysadmin")
        with zipf.open("key.key") as key_file:
            key = key_file.read()

    desencrypt(".", key)  # Desencripta en el directorio actual

if __name__ == "__main__":
    main()


