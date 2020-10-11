import RPi.GPIO as GPIO
import time
import sys
import board
import neopixel


pixel_pin = board.D12

# The number of NeoPixels
num_pixels = 16
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.8, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


amount = float(sys.argv[1])

CONTROL_PIN_1 = 18
CONTROL_PIN_2 = 17
CONTROL_PIN_3 = 27
CONTROL_PIN_4 = 23


PWM_FREQ = 50

sprayStop = 0
sprayAct = 180
ferStop = 135
ferAct = 35
fer2Stop = 180
fer2Act = 90
rota = 45
print(amount)


def change(x):
    if x == -1:
        spray(4)
        return
    if x >= 0 and x < 10:
        spray(3)
        return
    elif x >= 10 and x < 50:
        spray(5)
        return
    elif x >= 50 and x < 100:
        fertiliz(1)
        return
    elif x >= 100:
        ultimate()


def ultimate():
    print("ultimate")
    rainbow_cycle(0.002)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN_1, GPIO.OUT)
    GPIO.setup(CONTROL_PIN_2, GPIO.OUT)
    GPIO.setup(CONTROL_PIN_4, GPIO.OUT)
    pwm1 = GPIO.PWM(CONTROL_PIN_1, PWM_FREQ)
    pwm2 = GPIO.PWM(CONTROL_PIN_2, PWM_FREQ)
    pwm4 = GPIO.PWM(CONTROL_PIN_4, PWM_FREQ)
    pwm1.start(0)
    pwm2.start(0)
    pwm4.start(0)
    dc = angle_to_duty_cycle(sprayAct)
    pwm1.ChangeDutyCycle(dc)
    dc2 = angle_to_duty_cycle(ferAct)
    pwm2.ChangeDutyCycle(dc2)
    dc4 = angle_to_duty_cycle(rota)
    pwm4.ChangeDutyCycle(dc4)
    time.sleep(2)

    dc2 = angle_to_duty_cycle(ferStop)
    pwm2.ChangeDutyCycle(dc2)

    time.sleep(2)

    dc = angle_to_duty_cycle(sprayStop)
    pwm1.ChangeDutyCycle(dc)

    pixels.fill((0, 0, 0))
    pixels.show()

    time.sleep(1)
    pwm1.stop()
    pwm2.stop()
    pwm4.stop()
    GPIO.cleanup()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN_3, GPIO.OUT)
    pwm = GPIO.PWM(CONTROL_PIN_3, PWM_FREQ)
    pwm.start(0)

    dc = angle_to_duty_cycle_9g(fer2Act)
    pwm.ChangeDutyCycle(dc)
    time.sleep(1)
    dc = angle_to_duty_cycle_9g(fer2Stop)
    pwm.ChangeDutyCycle(dc)

    time.sleep(1)
    pwm.stop()
    GPIO.cleanup()


def fertiliz(t):
    print("fertiliz")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN_2, GPIO.OUT)
    pwm = GPIO.PWM(CONTROL_PIN_2, PWM_FREQ)
    pwm.start(0)

    dc = angle_to_duty_cycle(ferAct)
    pwm.ChangeDutyCycle(dc)
    time.sleep(t)
    dc = angle_to_duty_cycle(ferStop)
    pwm.ChangeDutyCycle(dc)

    time.sleep(1)
    pwm.stop()
    GPIO.cleanup()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN_3, GPIO.OUT)
    pwm = GPIO.PWM(CONTROL_PIN_3, PWM_FREQ)
    pwm.start(0)

    dc = angle_to_duty_cycle_9g(fer2Act)
    pwm.ChangeDutyCycle(dc)
    time.sleep(1)
    dc = angle_to_duty_cycle_9g(fer2Stop)
    pwm.ChangeDutyCycle(dc)

    time.sleep(2)
    pwm.stop()
    GPIO.cleanup()


def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.16 * PWM_FREQ * angle / 180)
    return duty_cycle


def angle_to_duty_cycle_9g(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle


def spray(t):
    print("spray")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN_1, GPIO.OUT)
    pwm = GPIO.PWM(CONTROL_PIN_1, PWM_FREQ)
    pwm.start(0)

    dc = angle_to_duty_cycle(sprayAct)
    pwm.ChangeDutyCycle(dc)
    time.sleep(t)
    dc = angle_to_duty_cycle(sprayStop)
    pwm.ChangeDutyCycle(dc)

    time.sleep(2)
    pwm.stop()
    GPIO.cleanup()


try:
    change(amount)
finally:
    GPIO.cleanup()
    pixels.fill((0, 0, 0))
    pixels.show()

try:
    chage(amount)
finally:
    GPIO.cleanup()
    pixels.fill((0, 0, 0))
    pixels.show()
