import RPi.GPIO as GPIO
from pn532 import *

def write_nfc():
    try:
        pn532 = PN532_I2C(debug=False, reset=20, req=16)
        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
        pn532.SAM_configuration()
        print('Waiting for RFID/NFC card...')
        while True:
            uid = pn532.read_passive_target(timeout=0.1)
            if uid is None:
                continue
            print('\nFound card with UID:', [hex(i) for i in uid])
            url = 'smb://192.168.12.103'
            url_bytes = [ord(c) for c in url]  # Convierte la URL en una lista de valores ASCII
            # Divide la URL en partes de 16 bytes
            url_parts = [url_bytes[i:i+16] for i in range(0, len(url_bytes), 16)]
            for i, part in enumerate(url_parts):
                # Rellena la parte con ceros si es menos de 16 bytes
                part += [0] * (16 - len(part))
                # Escribe la parte en el bloque correspondiente de la tarjeta NFC
                pn532.mifare_classic_write_block(4 + i, part)
            print('URL written to NFC card.')
            break  # Sal del bucle una vez que la URL se haya escrito en la tarjeta
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    write_nfc()
