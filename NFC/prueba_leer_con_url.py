import RPi.GPIO as GPIO
from pn532 import *
import webbrowser

def read_nfc():
    try:
        # Inicializa el módulo PN532
        pn532 = PN532_I2C(debug=False, reset=20, req=16)
        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
        
        # Configura el módulo PN532 para comunicarse con las tarjetas NFC
        pn532.SAM_configuration()
        
        print('Waiting for RFID/NFC card...')
        while True:
            # Intenta leer una tarjeta NFC
            uid = pn532.read_passive_target(timeout=0.1)
            
            # Si no se encontró una tarjeta, continúa con el siguiente ciclo del bucle
            if uid is None:
                continue
            
            # Si se encontró una tarjeta, imprime su UID
            print('\nFound card with UID:', [hex(i) for i in uid])
            
            # Intenta leer los datos de los bloques 4 a 9 de la tarjeta
            try:
                data_str = ''
                for i in range(4, 10):  # Asume que los datos están en los bloques de 4 a 9
                    data = pn532.mifare_classic_read_block(i)
                    data_str += ''.join([chr(b) for b in data if b != 0])  # Ignora los bytes nulos
                print('Data from NFC card:', data_str)
                
                # Si los datos comienzan con "http", asume que son una URL y abre la URL en el navegador web
                if data_str.startswith("http"):  
                    url = data_str
                    print('URL from NFC card:', url)
                    webbrowser.open(url)
            except Exception as e:
                print('Error reading NFC card data:', str(e))
    except Exception as e:
        print(e)
    finally:
        # Limpia los recursos de GPIO al finalizar
        GPIO.cleanup()

if __name__ == '__main__':
    read_nfc()
