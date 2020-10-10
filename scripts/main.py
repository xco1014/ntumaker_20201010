import RPi.GPIO as GPIO
import time
import sys

amount  = float(sys.argv[1])

CONTROL_PIN_1 = 18
CONTROL_PIN_2 = 17
CONTROL_PIN_3 = 27


PWM_FREQ = 50

sprayStop = 180
sprayAct  = 0
ferStop = 0
ferAct = 90

print(amount )


def chage(x):
    if x>=0 and x<10:
        spray(1)
        return
    elif x>=10 and x<50:
        spray(2)
        return
    elif x>=50 and x<=100:
        fertiliz(2)
        return



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

    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CONTROL_PIN_3, GPIO.OUT)
    pwm = GPIO.PWM(CONTROL_PIN_3, PWM_FREQ)
    pwm.start(0)

    dc = angle_to_duty_cycle(ferAct)
    pwm.ChangeDutyCycle(dc)
    time.sleep(0.5)
    dc = angle_to_duty_cycle(ferStop)

    pwm.ChangeDutyCycle(dc)
    pwm.stop()
    GPIO.cleanup()
    """



def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.17 * PWM_FREQ * angle / 180)
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

    time.sleep(1)
    pwm.stop()
    GPIO.cleanup()



chage(amount)