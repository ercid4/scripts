from pn532 import *

def setup():
    global pn532
    pn532 = PN532_I2C(debug=False, reset=20, req=16)
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
    pn532.SAM_configuration()

def write_data_to_card():
    print('Waiting for a card...')
    uid = None
    while uid is None:
        uid = pn532.read_passive_target(timeout=0.5)
    print('Found card with UID:', [hex(i) for i in uid])
    data = bytearray(b'Hola' + b'\x00' * 12)  # Datos a escribir
    if pn532.mifare_classic_authenticate_block(uid, 4, 0x61, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
        if pn532.mifare_classic_write_block(4, data):
            print('Data written to card')

if __name__ == '__main__':
    setup()
    write_data_to_card()
