# Descargar el instalador de Python y guardarlo en la carpeta temporal del sistema
$url = "https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
$install = Join-Path $env:TEMP "python-installer.exe"
Invoke-WebRequest -Uri $url -OutFile $installerPath -UseBasicParsing

# Ejecutar el instalador de Python de manera silenciosa
Start-Process -FilePath $install -ArgumentList "/quiet PrependPath=1" -Wait -WindowStyle Hidden

# Eliminar el instalador descargado
Remove-Item $install
