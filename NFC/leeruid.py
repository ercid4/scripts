import time
from pn532 import *

def setup():
    global pn532
    try:
        pn532 = PN532_I2C(debug=False, reset=20, req=16)
        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
        pn532.SAM_configuration()
    except Exception as e:
        print("Error setting up PN532: " + str(e))

def loop():
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is not None:
        print('Found card with UID:', [hex(i) for i in uid])

if __name__ == '__main__':
    setup()
    while True:
        loop()
        time.sleep(1)
