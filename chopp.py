import RPi.GPIO as GPIO 
import time
import threading


class ChoppFlow(threading.Thread):
    def __init__(self, pin):
         threading.Thread.__init__(self)
         self.pin = pin
         self.start_counter = False
         self.is_running = False
         self.count = 0
         self.total = 0
         self.flow = 0

    def config(self):
         GPIO.setmode(GPIO.BOARD)
         GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
         GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.count_pulse)

    def count_pulse(self):
         if self.start_counter:
             self.count += 1

    def run(self):
         self.config()
         self.is_running = True
         while self.is_running:
             self.start_counter = True
             time.sleep(0.5)
             self.start_counter = False
             self.flow = (self.count * 2.25) / 500
             self.count = 0
             self.total += 1.03 * self.flow

    def stop(self):
         self.is_running = False
         self.join()
         GPIO.cleanup()



