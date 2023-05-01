import adafruit_pn532.spi as pn532
import board
import busio
import digitalio
import time
import io
import typing

nfc_card = pn532.PN532_SPI(busio.SPI(board.SCK, board.MOSI, board.MISO), digitalio.DigitalInOut(board.D5), debug=False)

print(f"PN532 Version {nfc_card.firmware_version[1]} revision {nfc_card.firmware_version[2]}")
def getNewFile(id = 0):
    _file: typing.Union[io.TextIOWrapper, None] = None
    try:
        _file = open(f"./out/output{id}.txt", 'r')
        _file.close()
        return getNewFile(id+1)
    except:
        _file = open(f"./out/output{id}.txt", 'w')
        _file.write("<Card Outputs>\n")
    return _file

not_read_count = 0
file = getNewFile()
hasOutputed = False

try:
    while True:
        # uid = nfc_card.get_passive_target(.5)
        time.sleep(.5)
        uid = nfc_card.read_passive_target(timeout=.5)
        # uid = uid2 if uid == None else uid
        if (uid == None):
            not_read_count=not_read_count+1
            if (not_read_count > 2 and hasOutputed):
                file.close()
                file = getNewFile()
                hasOutputed = False
            continue
        if (not_read_count > 2):
            print("\n\n\n\n\n")
        not_read_count = 0
        print(f"Card with UID {[hex(i) for i in uid]}")
        file.write(f"{[hex(i) for i in uid]}\n")
        hasOutputed = True
except KeyboardInterrupt:
    file.close()
