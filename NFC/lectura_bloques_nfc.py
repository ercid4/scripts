import RPi.GPIO as GPIO
from pn532 import *

def read_nfc():
    try:
        # Inicializa el módulo PN532
        pn532 = PN532_I2C(debug=False, reset=20, req=16)
        ic, ver, rev, support = pn532.get_firmware_version()
        print('Encontrado PN532 con versión de firmware: {0}.{1}'.format(ver, rev))
        
        # Configura el módulo PN532 para comunicarse con las tarjetas NFC
        pn532.SAM_configuration()
        
        print('Esperando tarjeta RFID/NFC...')
        while True:
            # Intenta leer una tarjeta NFC
            uid = pn532.read_passive_target(timeout=0.1)
            
            # Si se encontró una tarjeta, imprime su UID
            if uid is not None:
                print('\nEncontrada tarjeta con UID:', [hex(i) for i in uid])
                
                # Lee los datos de todos los bloques de la tarjeta
                for block in range(4, 64):  # Asume que la tarjeta tiene 64 bloques
                    data = pn532.mifare_classic_read_block(block)
                    if data is not None:
                        # Convierte los datos a una cadena
                        data_str = ''.join([chr(b) for b in data if b != 0])
                        if data_str:
                            print('Bloque', block, 'contiene datos:', data_str)
                        else:
                            print('Bloque', block, 'está vacío y puede ser usado para almacenamiento')
                    else:
                        print('Error al leer datos del bloque', block, 'de la tarjeta')
                
                break
    except Exception as e:
        print('Error al leer datos de la tarjeta NFC:', str(e))
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    read_nfc()
