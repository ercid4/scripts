#!/usr/bin/env python

from pn532pi import Pn532, Pn532Spi

# Crear una nueva instancia de la clase Pn532Spi
spi = Pn532Spi()
# Crear una nueva instancia de la clase Pn532
nfc = Pn532(spi)

try:
    # Iniciar la comunicación con el módulo PN532
    nfc.begin()
    # Configurar el módulo PN532 para comunicarse con tarjetas NFC
    nfc.SAMConfig()
    print("Esperando una tarjeta NFC...")
    while True:
        # Leer el ID (UID) de cualquier tarjeta NFC que esté en el rango del lector
        uid = nfc.readPassiveTargetID()
        if uid is not None:
            print("Tarjeta detectada con UID: %s" % uid)
            # Leer el texto almacenado en la tarjeta NFC
            text = nfc.mifareclassic_ReadNDEFText(uid)
            if text is not None:
                print("Texto leído de la tarjeta: %s" % text)
            else:
                print("Error al leer el texto de la tarjeta")
            print("Ahora coloca tu tarjeta para escribir")
            # Solicitar al usuario que introduzca los nuevos datos a escribir en la tarjeta
            new_text = input('Nuevos datos:')
            # Escribir los nuevos datos en la tarjeta
            if nfc.mifareclassic_WriteNDEFText(uid, new_text):
                print("Escrito")
            else:
                print("Error al escribir en la tarjeta")
except KeyboardInterrupt:
    # Manejar la interrupción por teclado y finalizar el programa de manera segura
    print("Interrupción por teclado, finalizando...")
