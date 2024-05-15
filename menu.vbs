Dim objShell, UserName

#Obtener el nombre de usuario del usuario actual
UserName = CreateObject("WScript.Network").UserName

Set objShell = CreateObject("WScript.Shell")

#Construir el comando para ejecutar el script de PowerShell con el nombre de usuario como argumento
strCommand = "powershell.exe -ExecutionPolicy Bypass -File SMBcredentials.ps1 -username " & UserName

#Ejecutar el comando y redirigir la salida a un archivo
objShell.Run strCommand & " > datos.txt", 0

Set objShell = Nothing

