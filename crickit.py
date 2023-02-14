import adafruit_crickit
import sense_hat
import time
import rpi_lcd
import typing

crickit = adafruit_crickit.crickit
sense = sense_hat.SenseHat()
lcd = rpi_lcd.LCD(0x27, 1, 16, 2)
selection: int = 0
msg_set = False
sub_selection: int = 0
int_val = 0
bool_val = False
float_val = .5

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

def pulseservo(touch: sense_hat.InputEvent):
    global sub_selection
    name = "Servo"
    if (touch.action is "pressed"):
        if (touch.direction is "left"):
            sub_selection = sub_selection-1 if sub_selection > 0 else 7
            return
        elif (touch.direction is "right"):
            sub_selection = sub_selection+1 if sub_selection < 7 else 0
            return

        if (sub_selection > 3):
            name = f"Cont. {name}"

        if (not msg_set):
            lcd.text(f"{name} Off", 2, "center")

        if (sub_selection is 0):
            crickit.servo_1.angle = 180 if crickit.servo_1 < 179 else 0
        if (sub_selection is 1):
            crickit.servo_2.angle = 180 if crickit.servo_2 < 179 else 0
        if (sub_selection is 2):
            crickit.servo_3.angle = 180 if crickit.servo_3 < 179 else 0
        if (sub_selection is 3):
            crickit.servo_4.angle = 180 if crickit.servo_4 < 179 else 0

        if (sub_selection is 4):
            crickit.continuous_servo_1.throttle = 0 if crickit.continuous_servo_1 < 1 else 1
        if (sub_selection is 5):
            crickit.continuous_servo_2.throttle = 0 if crickit.continuous_servo_2 < 1 else 1
        if (sub_selection is 6):
            crickit.continuous_servo_3.throttle = 0 if crickit.continuous_servo_3 < 1 else 1
        if (sub_selection is 7):
            crickit.continuous_servo_4.throttle = 0 if crickit.continuous_servo_4 < 1 else 1


def handleInput():
    global selection, active, sub_selection
    time.sleep(.25)
    touch: sense_hat.InputEvent
    # touch motor = 0
    print_exitq: bool = False

    for touch in sense.stick.get_events():
        if (touch.action is "pressed"):
            if (touch.direction is "up"):
                selection = selection+1 if selection < 1 else 0
                print_exitq = False
                active = False
                msg_set = False
                sub_selection = 0
            elif (touch.direction is "down"):
                selection = selection-1 if selection > 0 else 1
                print_exitq = False
                active = False
                msg_set = False
                sub_selection = 0
        if (selection is 0):
            touchmotor(touch)
        elif (selection is 1):
            if (not print_exitq):
                lcd.text("Exit?", 2)
                print_exitq = True
            if (touch.direction is "middle"):
                _exit(0)

def mainLoop():
    while (True):
        handleInput()

def main():
    lcd.clear()
    lcd.text("The Crafters", 1, 'center')
    time.sleep(1)
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
