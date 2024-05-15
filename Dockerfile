# Usamos una imagen base de Ubuntu
FROM ubuntu:latest

# Actualizamos e instalamos Samba
RUN apt-get update && apt-get install -y samba

# Creamos los usuarios y establecemos sus contraseñas
RUN useradd -ms /bin/bash autorizado && echo "autorizado:aut1" | chpasswd
RUN useradd -ms /bin/bash no_autorizado && echo "no_autorizado:noaut1" | chpasswd

# Creamos los usuarios de Samba
RUN (echo "aut1"; echo "aut1") | smbpasswd -a -s autorizado
RUN (echo "noaut1"; echo "noaut1") | smbpasswd -a -s no_autorizado

# Creamos el directorio base /samba
RUN mkdir /samba

# Creamos las carpetas
RUN mkdir /samba/autorizado /samba/no_autorizado

# Cambiamos el propietario de las carpetas a nuestros usuarios
RUN chown autorizado:autorizado /samba/autorizado
RUN chown no_autorizado:no_autorizado /samba/no_autorizado

# Configuramos Samba
RUN echo -e "[global]\nworkgroup = WORKGROUP\nsecurity = user\nmap to guest = Never\n\n[autorizado]\npath = /samba/autorizado\nread only = no\nbrowsable = yes\nvalid users = autorizado\n\n[no_autorizado]\npath = /samba/no_autorizado\nread only = no\nbrowsable = yes\nvalid users = no_autorizado" > /etc/samba/smb.conf

# Exponemos el puerto de Samba
EXPOSE 137/udp 138/udp 139 445

# Iniciamos Samba
CMD ["smbd", "--foreground", "--no-process-group"]


