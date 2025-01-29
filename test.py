import RPi.GPIO as GPIO
import time


motor_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin,GPIO.OUT)

pwm = GPIO.PWM(motor_pin, 1000)
pwm.start(0)

try:
    while True:
        for dc in range(0,101,5):
            pwm.ChangeDutyCycle(dc)
            print(f"speed{dc}%")
            time.sleep(2)
except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup()

