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


def idle():
    while True:
        print('start idle mode')
        rainbow_cycle(0.002)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(CONTROL_PIN_4, GPIO.OUT)
        dc4 = angle_to_duty_cycle(rota)
        pwm4 = GPIO.PWM(CONTROL_PIN_4, PWM_FREQ)
        pwm4.start(0)
        pwm4.ChangeDutyCycle(dc4)

        for i in range(3):
            rainbow_cycle(0.002)
            time.sleep(3)

        pixels.fill((0, 0, 0))
        pixels.show()

        pwm4.stop()
        GPIO.cleanup()

        time.sleep(5)


def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.16 * PWM_FREQ * angle / 180)
    return duty_cycle


def angle_to_duty_cycle_9g(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle


try:
    idle()
finally:
    print('finish clean up')
    GPIO.cleanup()
    pixels.fill((0, 0, 0))
    pixels.show()
