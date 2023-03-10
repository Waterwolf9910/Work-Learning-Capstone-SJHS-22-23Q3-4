import adafruit_crickit as _crickit
import adafruit_matrixkeypad as matrixkeypad
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import sense_hat
import time
import rpi_lcd
import busio
import digitalio
import board
import typing
import enum

crickit = _crickit.crickit
sense = sense_hat.SenseHat()
# lcd = rpi_lcd.LCD(0x27, 1, 16, 2)
lcd_cols = 16
lcd_rows = 2
lcd = character_lcd.Character_LCD_I2C(board.I2C(board.SCL, board.SDA), 16, 2, 0x27)
class Direction(enum.Enum):
    LEFT = enum.auto()
    CENTER = enum.auto()
    RIGHT = enum.auto()

def LCDText(text: str, line: typing.Optional[int] = lcd_rows, dir: Direction = Direction.LEFT):
    if (len(text) > lcd_cols):
        raise OverflowError(f"You cannot have more than {lcd_cols} characters in a line")
    if (line > lcd_rows):
        raise IndexError(f"Line cannot be greater than {lcd_rows}")
    if (line < 1):
        raise IndexError("Line cannout be less than 1")
    lcd.message = text.rjust(lcd_cols) if dir == Direction.RIGHT else text.center(lcd_cols) if dir == Direction.CENTER else text.ljust(lcd_cols)

selection: int = -1
msg_set = False
sub_selection: int = 0
loop = False
int_val = 0
bool_val = False
float_val = .5
# https://learn.adafruit.com/matrix-keypad/python-circuitpython
_keys = ( (2,5,8,0), (1,4,7,'*'), (3,6,9,'#'), ('a','b','c','d') )
key_rows = [digitalio.DigitalInOut(x) for x in (board.D12,board.D16,board.D20,board.D21)]
key_cols = [digitalio.DigitalInOut(y) for y in (board.D6,board.D13,board.D19,board.D26)]
keypad = matrixkeypad.Matrix_Keypad(key_rows, key_cols, _keys)

def servo():
    while True:
        crickit.servo_1.angle = 0
        time.sleep(.05)
        crickit.servo_1.angle = 90
        time.sleep(.05)
        crickit.servo_1.angle = 180
        time.sleep(.05)
        crickit.servo_1.angle = 90
        time.sleep(.05)

def motor():
    crickit.dc_motor_1.throttle = .25
    time.sleep(1.5) #allow the fan to fully spin up
    time.sleep(3) # wait for three seconds
    crickit.dc_motor_1.throttle = 0 # Stop the Fan
    time.sleep(.5)
    crickit.continuous_servo_1.throttle = .5

# Only Gets Left, Right, and Middle
def touchmotor(touch: sense_hat.InputEvent):
    global msg_set
    _motor = crickit.dc_motor_1
    _motor.throttle = 0 if _motor.throttle == None else _motor.throttle
    if (not msg_set):
        msg_set = True
        LCDText("Motor: Off", 2, Direction.CENTER)
    if (touch.action == "pressed"):
        if (touch.direction == "middle"):
            if (_motor.throttle > 0):
                _motor.throttle = 0
                LCDText("Motor: Off", 2, Direction.CENTER)
                # sense.show_message("Off", 0.1, (255, 0, 0))
            else:
                _motor.throttle = .35
                LCDText("Motor: On", 2, Direction.CENTER)
                # sense.show_message("On", 0.1, (0, 255, 0))

ps_reverse = False
def pulseservo(touch: sense_hat.InputEvent):
    global sub_selection, ps_reverse
    name = "Servo"
    if (touch.action == "pressed"):
        if (touch.direction == "left"):
            sub_selection = sub_selection-1 if sub_selection > 0 else 8
            if (sub_selection > 3):
                name = f"Cont. {name}"
            if (sub_selection == 8):
                LCDText(f"Reverse: {'true' if ps_reverse else 'false'}")
            if (not msg_set):
                LCDText(f"{name} {(sub_selection%4)+1}", 2, "center")
            return
        elif (touch.direction == "right"):
            sub_selection = sub_selection+1 if sub_selection < 8 else 0
            if (sub_selection > 3):
                name = f"Cont. {name}"
            if (sub_selection == 8):
                LCDText(f"Reverse: {'true' if ps_reverse else 'false'}")
            if (not msg_set):
                LCDText(f"{name} {(sub_selection%4)+1}", 2, "center")
            return

        if (sub_selection > 3):
            name = f"Cont. {name}"
        if (sub_selection == 8):
            LCDText(f"Reverse: {'true' if ps_reverse else 'false'}")
        if (not msg_set):
            LCDText(f"{name} {(sub_selection%4)+1}", 2, "center")

        if (touch.direction == "middle"):
            if (sub_selection == 0):
                crickit.servo_1.angle = 180 if crickit.servo_1.angle == 0 else 180
            if (sub_selection == 1):
                crickit.servo_2.angle = 180 if crickit.servo_2.angle == 0 else 180
            if (sub_selection == 2):
                crickit.servo_3.angle = 180 if crickit.servo_3.angle == 0 else 180
            if (sub_selection == 3):
                crickit.servo_4.angle = 180 if crickit.servo_4.angle == 0 else 180

            if (sub_selection == 4):
                crickit.continuous_servo_1.throttle = 0 if crickit.continuous_servo_1.throttle == 1 else 1
            if (sub_selection == 5):
                crickit.continuous_servo_2.throttle = 0 if crickit.continuous_servo_2.throttle == 1 else 1
            if (sub_selection == 6):
                crickit.continuous_servo_3.throttle = 0 if crickit.continuous_servo_3.throttle == 1 else 1
            if (sub_selection == 7):
                crickit.continuous_servo_4.throttle = 0 if crickit.continuous_servo_4.throttle == 1 else 1
            if (sub_selection == 8):
                ps_reverse = not ps_reverse

text = ["Keypad"]
text_data = {
    "line": 0,
    "pos": 0
}

def use_keypad(touch: typing.Union[sense_hat.InputEvent, None]):
    global msg_set, loop, text, active
    keys = keypad.pressed_keys
    active = False
    if (not msg_set):
        LCDText("Keypad", 2, Direction.CENTER)
        loop = True
        msg_set = True
    if (touch != None):
        active = True
        # Delete Character at pos
        if (touch.direction == "middle"):
            _text = text[text_data["line"]]
            # Set the character at pos to empty
            _text = _text[0:text_data["pos"]-1] + ' ' + _text[text_data["pos"]:len(_text)]
            text[text_data["line"]] = _text
        elif (touch.direction == "left"):
            if (text_data["pos"] == 0):
                text_data["pos"] = 15
                text_data["line"] = text_data["line"] - 1 if text_data["line"] > 0 else len(text)
            else:
                text_data["pos"] = text_data["pos"] - 1
        elif (touch.direction == "left"):
            if (text_data["pos"] == 15):
                text_data["pos"] = 0
                text_data["line"] = text_data["line"] + 1 if text_data["line"] < len(text) else 0
            else:
                text_data["pos"] = text_data["pos"] + 1
    if (keys):
        active = True
        print(keys)
        for key in keys:
            if (text_data["pos"] == 15):
                text_data["line"] = text_data["line"]+1
                text_data["pos"] = 0
            _text = text[text_data["line"]]
            _text = _text[0:text_data["pos"]-1] + key + _text[text_data["pos"]:len(_text)]
            text[text_data["line"]] = _text
    if (active):
        lcd.cursor_position(0, 2)
        # time.sleep(.1)
        LCDText(text[text_data["line"]], 2)
        lcd.cursor_position(text_data["pos"], 2)
        # time.sleep(.1)
        time.sleep(.15)

def selectors(_touch: sense_hat.InputEvent):
    global msg_set
    if (selection == 0):
        touchmotor(_touch)
    elif (selection == 1):
        pulseservo(_touch)
    elif (selection == 2):
        use_keypad(_touch)
    elif (selection == 3):
        if (not msg_set):
            LCDText("Exit?", 2, Direction.CENTER)
            msg_set = True
        if (_touch.direction == "middle"):
            _exit(0)

def handleInput():
    global selection, active, sub_selection, msg_set, loop
    numOfSelections = 3
    time.sleep(.25)
    touch: sense_hat.InputEvent
    # touch motor = 0

    if (selection == -1):
        if (not msg_set):
            LCDText("Main Menu", 2, Direction.CENTER)
            msg_set = True
    for touch in sense.stick.get_events():
        if (touch.action == "pressed"):
            if (touch.direction == "up"):
                selection = selection+1 if selection < numOfSelections else 0
                active = False
                lcd.cursor = False
                msg_set = False
                loop = False
                sub_selection = 0
            elif (touch.direction == "down"):
                selection = selection-1 if selection > 0 else numOfSelections
                active = False
                msg_set = False
                lcd.cursor = False
                loop = False
                sub_selection = 0
            selectors(touch)
    if (loop):
        selectors(None)

def mainLoop():
    while (True):
        handleInput()

def main():
    lcd.backlight = True
    lcd.clear()
    time.sleep(.1)
    # time.sleep(1)
    lcd.blink = True
    lcd.cursor = False
    lcd.display = True
    LCDText("The Crafters", 1, Direction.CENTER)
    crickit.servo_1.angle = 0
    crickit.servo_2.angle = 0
    crickit.servo_3.angle = 0
    crickit.servo_4.angle = 0
    crickit.continuous_servo_1.throttle = 0
    crickit.continuous_servo_2.throttle = 0
    crickit.continuous_servo_3.throttle = 0
    crickit.continuous_servo_4.throttle = 0
    crickit.dc_motor_1.throttle = 0
    crickit.dc_motor_2.throttle = 0
    mainLoop()

def _exit(code: int = 0):
    lcd.backlight = False
    time.sleep(.1)
    lcd.display = False
    time.sleep(.1)
    lcd.cursor = False
    time.sleep(.1)
    lcd.clear()
    lcd.home()
    time.sleep(1.5)
    exit(code)


try:
    main()
except KeyboardInterrupt:
    _exit()
