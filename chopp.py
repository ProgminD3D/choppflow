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
        self.consumed = 0
        self.total = 0
        self.flow = 0
        self.consumers = []
        self.selected_user = -1

    def to_json(self):
        return {
           'meta': {
                'consumed': self.consumed,
                'total': self.total
            },
            'users': self.consumers
        }

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
            self.flow = 1.03 * (self.count * 2.25) / 500
            self.count = 0
            self.consumed += self.flow
            if self.selected_user != -1:
                self.consumers[self.selected_user]['consumed'] += self.flow

    def stop(self):
        self.is_running = False
        if self.is_alive():
            self.join()
        GPIO.cleanup()
