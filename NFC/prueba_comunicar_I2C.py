#!/usr/bin/env python

from pn532pi import Pn532, Pn532I2c

# Crear una nueva instancia de la clase Pn532I2c
i2c = Pn532I2c(1)
# Crear una nueva instancia de la clase Pn532
nfc = Pn532(i2c)

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
except KeyboardInterrupt:
    # Manejar la interrupción por teclado y finalizar el programa de manera segura
    print("Interrupción por teclado, finalizando...")
