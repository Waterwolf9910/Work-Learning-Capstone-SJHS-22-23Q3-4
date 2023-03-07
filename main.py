import adafruit_crickit
import adafruit_matrixkeypad
import sense_hat
import time
import rpi_lcd
import digitalio
import board
import typing

crickit = adafruit_crickit.crickit
sense = sense_hat.SenseHat()
lcd = rpi_lcd.LCD(0x27, 1, 16, 2)
selection: int = 2
msg_set = False
sub_selection: int = 0
loop = True
int_val = 0
bool_val = False
float_val = .5
# https://learn.adafruit.com/matrix-keypad/python-circuitpython
_keys = ( (1,2,3,'a'), (4,5,6,'b'), (7,8,9,'c'), ('*',0,'#','d') )
rows = [digitalio.DigitalInOut(x) for x in (board.D12,board.D16,board.D20,board.D21)]
cols = [digitalio.DigitalInOut(y) for y in (board.D6,board.D13,board.D19,board.D26)]
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, _keys)

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
    _motor.throttle = 0 if _motor.throttle is None else _motor.throttle
    if (not msg_set):
        msg_set = True
        lcd.text("Motor: Off", 2, 'center')
    if (touch.action is "pressed"):
        if (touch.direction is "middle"):
            if (_motor.throttle > 0):
                _motor.throttle = 0
                lcd.text("Motor: Off", 2, 'center')
                # sense.show_message("Off", 0.1, (255, 0, 0))
            else:
                _motor.throttle = .35
                lcd.text("Motor: On", 2, 'center')
                # sense.show_message("On", 0.1, (0, 255, 0))

ps_reverse = False
def pulseservo(touch: sense_hat.InputEvent):
    global sub_selection, ps_reverse
    name = "Servo"
    if (touch.action is "pressed"):
        if (touch.direction is "left"):
            sub_selection = sub_selection-1 if sub_selection > 0 else 8
            if (sub_selection > 3):
                name = f"Cont. {name}"
            if (sub_selection is 8):
                lcd.text(f"Reverse: {'true' if ps_reverse else 'false'}")
            if (not msg_set):
                lcd.text(f"{name} {(sub_selection%4)+1}", 2, "center")
            return
        elif (touch.direction is "right"):
            sub_selection = sub_selection+1 if sub_selection < 8 else 0
            if (sub_selection > 3):
                name = f"Cont. {name}"
            if (sub_selection is 8):
                lcd.text(f"Reverse: {'true' if ps_reverse else 'false'}")
            if (not msg_set):
                lcd.text(f"{name} {(sub_selection%4)+1}", 2, "center")
            return

        if (sub_selection > 3):
            name = f"Cont. {name}"
        if (sub_selection is 8):
            lcd.text(f"Reverse: {'true' if ps_reverse else 'false'}")
        if (not msg_set):
            lcd.text(f"{name} {(sub_selection%4)+1}", 2, "center")

        if (touch.direction is "middle"):
            if (sub_selection is 0):
                crickit.servo_1.angle = 180 if crickit.servo_1.angle is 0 else 180
            if (sub_selection is 1):
                crickit.servo_2.angle = 180 if crickit.servo_2.angle is 0 else 180
            if (sub_selection is 2):
                crickit.servo_3.angle = 180 if crickit.servo_3.angle is 0 else 180
            if (sub_selection is 3):
                crickit.servo_4.angle = 180 if crickit.servo_4.angle is 0 else 180

            if (sub_selection is 4):
                crickit.continuous_servo_1.throttle = 0 if crickit.continuous_servo_1.throttle is 1 else 1
            if (sub_selection is 5):
                crickit.continuous_servo_2.throttle = 0 if crickit.continuous_servo_2.throttle is 1 else 1
            if (sub_selection is 6):
                crickit.continuous_servo_3.throttle = 0 if crickit.continuous_servo_3.throttle is 1 else 1
            if (sub_selection is 7):
                crickit.continuous_servo_4.throttle = 0 if crickit.continuous_servo_4.throttle is 1 else 1
            if (sub_selection is 8):
                ps_reverse = not ps_reverse

def use_keypad(touch: typing.Union[sense_hat.InputEvent, None]):
    keys = keypad.pressed_keys
    if (keys):
        print(keys)
    time.sleep(.25)

def handleInput():
    global selection, active, sub_selection, msg_set, loop
    numOfSelections = 3
    time.sleep(.25)
    touch: sense_hat.InputEvent
    def selectors(_touch: sense_hat.InputEvent):
        if (selection is 0):
            touchmotor(_touch)
        elif (selection is 1):
            pulseservo(_touch)
        elif (selection is 2):
            use_keypad(_touch)
        elif (selection is 3):
            if (not msg_set):
                lcd.text("Exit?", 2)
                msg_set = True
            if (_touch.direction is "middle"):
                _exit(0)
    # touch motor = 0

    if (selection is -1):
        if (not msg_set):
            lcd.text("Main Menu", 2, 'center')
            msg_set = True
    for touch in sense.stick.get_events():
        if (touch.action is "pressed"):
            if (touch.direction is "up"):
                selection = selection+1 if selection < numOfSelections else 0
                active = False
                msg_set = False
                loop = False
                sub_selection = 0
            elif (touch.direction is "down"):
                selection = selection-1 if selection > 0 else numOfSelections
                active = False
                msg_set = False
                loop = False
                sub_selection = 0
            selectors(touch)
    if (loop):
        selectors(None)

def mainLoop():
    while (True):
        handleInput()

def main():
    lcd.clear()
    lcd.text("The Crafters", 1, 'center')
    time.sleep(1)
    crickit.servo_1.angle = 0
    crickit.servo_2.angle = 0
    crickit.servo_3.angle = 0
    crickit.servo_4.angle = 0
    crickit.continuous_servo_1.throttle = 0
    crickit.continuous_servo_2.throttle = 0
    crickit.continuous_servo_3.throttle = 0
    crickit.continuous_servo_4.throttle = 0
    mainLoop()

def _exit(code: int = 0):
    lcd.backlight = False
    time.sleep(.5)
    lcd.clear()
    time.sleep(1.5)
    exit(code)


try:
    main()
except KeyboardInterrupt:
    _exit()
