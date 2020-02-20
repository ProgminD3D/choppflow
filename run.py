import time
import chopp


chopp_flow = chopp.ChoppFlow(16)

try:
    chopp_flow.start()
    while True:
         time.sleep(1)
         print(f'Consumo: {chopp_flow.total}')
except KeyboardInterrupt:
    print('\nInterrupted by user')
except:
    pass

chopp_flow.stop()
print('bye!')

