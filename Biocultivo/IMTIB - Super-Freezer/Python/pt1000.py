import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c)


ord = 6000
pend = 58.52713

def sensar():
    continuar = True
    while continuar:
        dato =  input("Ingrese una letra: ")
        y = AnalogIn(ads, ADS.P0, ADS.P1)
        x = (y.value - ord)/pend
        print("{0:.1f}".format(float(x)), " grados")
        if dato == 'z':
            continuar = False
            print("Finalizacion del programa.")     
        else:
            pass

sensar()