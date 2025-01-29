import RPi.GPIO as GPIO
import time


motor_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin,GPIO.OUT)

#Frequence de 1000 Hz (le moteur recevra un signal qui switch on/off 1000 fois par seconde)
#ça serait interessant de le faire varier?
pwm = GPIO.PWM(motor_pin, 1000)
pwm.start(0)

try:
    while True:
        for dc in range(0,101,5):
            #DutyCycle:Indique le ratio des fois que le signal est a 0
            pwm.ChangeDutyCycle(dc)
            print(f"speed{dc}%")
            time.sleep(2)
except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup()

