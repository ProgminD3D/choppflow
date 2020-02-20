import RPi.GPIO as GPIO 
import time
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
#pulsos_por_minuto = 0
#tot_pulsos = 0
#constante = 0.10 / 60
#tempo_novo = 0.0

count = 0
start_counter = False
total = 0
def countPulse(channel):
    global count
    if start_counter:
        count += 1

GPIO.add_event_detect(16, GPIO.FALLING, callback=countPulse)

try:
    while True:
        start_counter = True
        time.sleep(1)
        # print(GPIO.input(16))
        start_counter = False
        flow = (count  * 2.25) / 1000
        count = 0
        total += 1.035 * flow
        print(f"{time.time()} {flow} {total}")
        #print("Litros por minuto",round(pulsos_por_minuto * constante,2)) 
        #print("Total de Litros",round(tot_pulsos * constante,2))
except KeyboardInterrupt:
    print('Bye')
except:
    pass

GPIO.cleanup()

