import RPi.GPIO as GPIO
from pn532 import *

def is_ascii(data):
    return all(b < 128 for b in data)

try:
    # Crear una nueva instancia de la clase PN532_I2C
    pn532 = PN532_I2C(debug=False, reset=20, req=16)
    # Obtener la versión del firmware del módulo PN532
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
    # Configurar el módulo PN532 para comunicarse con tarjetas MiFare
    pn532.SAM_configuration()
    print("Esperando una tarjeta NFC...")
    while True:
        # Leer el ID (UID) de cualquier tarjeta NFC que esté en el rango del lector
        uid = pn532.read_passive_target(timeout=0.5)
        if uid is not None:
            print("Tarjeta detectada con UID: %s" % [hex(i) for i in uid])
            print("Leyendo el contenido de la tarjeta...")
            # Leer los datos del bloque 4 de la tarjeta
            data = pn532.mifare_classic_read_block(4)
            if data is not None:
                # Verificar si los datos son ASCII válidos antes de intentar decodificar
                if is_ascii(data):
                    # Convertir los datos a texto
                    text = bytes(data).decode('utf-8').rstrip()
                    print("Texto leído de la tarjeta: %s" % text)
                else:
                    print("Los datos leídos de la tarjeta no son ASCII válidos.")
            else:
                print("Error al leer de la tarjeta")
        else:
            print('.', end="")
except KeyboardInterrupt:
    print("Interrupción por teclado, finalizando...")
except Exception as e:
    print("Error: ", e)
finally:
    GPIO.cleanup()
