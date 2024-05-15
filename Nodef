# Verificar si el script se está ejecutando como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

# Si no se está ejecutando como administrador, volver a ejecutar el script con privilegios elevados
if (-not $isAdmin) {
    Write-Host "Este script requiere permisos de administrador. Se solicitarán permisos de elevación."
    Start-Sleep -Seconds 2
    Start-Process powershell.exe -Verb RunAs -ArgumentList ("-File `"$PSCommandPath`"")
    Exit
}

# Deshabilitar las funcionalidades de Windows Defender
$registryPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender"
if (!(Test-Path $registryPath)) {
    New-Item -Path $registryPath -Force | Out-Null
}
Set-ItemProperty -Path $registryPath -Name "DisableAntiSpyware" -Value 1 -Type DWORD -Force | Out-Null

# Detener y deshabilitar los servicios de Windows Defender
$serviceList = @("WdNisSvc", "WinDefend")
foreach ($svc in $serviceList) {
    Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
    Set-Service -Name $svc -StartupType Disabled -ErrorAction SilentlyContinue
}

# Deshabilitar los controladores de Windows Defender
$driverList = @("WdnisDrv", "wdboot", "wdfilter")
foreach ($drv in $driverList) {
    if (Test-Path "HKLM:\SYSTEM\CurrentControlSet\Services\$drv") {
        Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\$drv" -Name Start -Value 4 -Force | Out-Null
    }
}

# Eliminar archivos y carpetas de Windows Defender
$wdDirectory = "C:\Windows\System32\drivers\wd\"
if (Test-Path $wdDirectory) {
    Remove-Item $wdDirectory -Recurse -Force -ErrorAction SilentlyContinue
}

$programFilesDefender = "C:\Program Files\Windows Defender"
if (Test-Path $programFilesDefender) {
    Remove-Item $programFilesDefender -Recurse -Force -ErrorAction SilentlyContinue
}

$programDataDefender = "C:\ProgramData\Microsoft\Windows Defender"
if (Test-Path $programDataDefender) {
    Remove-Item $programDataDefender -Recurse -Force -ErrorAction SilentlyContinue
}

# Deshabilitar el servicio de Windows Update
$serviceName = "wuauserv"
Stop-Service -Name $serviceName -Force -ErrorAction SilentlyContinue
Set-Service -Name $serviceName -StartupType Disabled -ErrorAction SilentlyContinue

# Establecer el servicio de Windows Update en deshabilitado a través del Registro
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\$serviceName" -Name "Start" -Value 4 -Force | Out-Null
