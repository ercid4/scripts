import RPi.GPIO as GPIO
from pn532 import *

try:
    # Crear una nueva instancia de la clase PN532_I2C
    pn532 = PN532_I2C(debug=False, reset=20, req=16)
    # Obtener la versión del firmware del módulo PN532
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
    # Configurar el módulo PN532 para comunicarse con tarjetas MiFare
    pn532.SAM_configuration()
    print("Esperando una tarjeta NFC...")
    # Leer el ID (UID) de cualquier tarjeta NFC que esté en el rango del lector
    uid = pn532.read_passive_target(timeout=0.5)
    while uid is None:
        print('.', end="")
        uid = pn532.read_passive_target(timeout=0.5)
    print("Tarjeta detectada con UID: %s" % [hex(i) for i in uid])
    new_text = input('Introduce el texto a escribir en la tarjeta: ')
    print("Por favor, acerca de nuevo la tarjeta para escribir los datos en ella.")
    # Convertir el texto en bytes y rellenar hasta 16 bytes
    data = bytearray(new_text.ljust(16), 'utf-8')
    # Esperar a que la tarjeta esté en el rango de nuevo
    while pn532.read_passive_target(timeout=0.5) is None:
        pass
    # Escribir los datos en el bloque 4 de la tarjeta
    if pn532.mifare_classic_write_block(4, data):
        print("Escrito")
    else:
        print("Error al escribir en la tarjeta")
except KeyboardInterrupt:
    print("Interrupción por teclado, finalizando...")
except Exception as e:
    print("Error: ", e)
finally:
    GPIO.cleanup()
