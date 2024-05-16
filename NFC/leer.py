from pn532 import *

def setup():
    global pn532
    pn532 = PN532_I2C(debug=False, reset=20, req=16)
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
    pn532.SAM_configuration()

def read_data_from_card():
    print('Waiting for a card...')
    uid = None
    while uid is None:
        uid = pn532.read_passive_target(timeout=0.5)
    print('Found card with UID:', [hex(i) for i in uid])
    if pn532.mifare_classic_authenticate_block(uid, 4, 0x61, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
        data = pn532.mifare_classic_read_block(4)
        text = data.decode('utf-8').rstrip('\x00')  # Decodifica los datos y elimina los bytes nulos
        print('Read data from card:', text)

if __name__ == '__main__':
    setup()
    read_data_from_card()


