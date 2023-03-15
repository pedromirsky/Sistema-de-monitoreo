import Adafruit_DHT as dht
sensor = dht.DHT22

def sensar():
    continuar = True
    while continuar:
        dato =  input("Ingrese una letra: ")
        humedad, temperatura = dht.read_retry(sensor, 4)
        print("Tempeatura = ", temperatura, ". Humedad = ", humedad)
        if dato == 'z':
            continuar = False
            print("Finalizacion del programa.")     
        else:
            pass

sensar()