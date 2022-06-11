import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

LED2 = 3
LED = 5

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

GPIO.output(LED, GPIO.HIGH)
GPIO.output(LED2, GPIO.LOW)
time.sleep(3)
GPIO.output(LED, GPIO.LOW)
GPIO.output(LED2, GPIO.HIGH)
time.sleep(3)
GPIO.output(LED, GPIO.HIGH)
GPIO.output(LED2, GPIO.LOW)
time.sleep(3)
GPIO.output(LED, GPIO.LOW)
GPIO.output(LED2, GPIO.HIGH)

GPIO.output(LED, GPIO.LOW)
GPIO.output(LED2, GPIO.LOW)
