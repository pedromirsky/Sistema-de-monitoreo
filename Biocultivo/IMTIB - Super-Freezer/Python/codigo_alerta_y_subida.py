# Librerias
from tkinter import *
import pyrebase
import random
import time 
from datetime import datetime
from email.message import EmailMessage
import smtplib
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c)

# Parametro para PT1000
ord = 6000
pend = 58.52713

# Funcion Email
def email_alert(subject, body, to):

    msg = EmailMessage()

    msg.set_content(body)

    msg['subject'] = subject

    msg['to'] = to

    #esto es QUIEN lo manda

    user = "monitortemperaturaiuhi@gmail.com"

    msg['from'] = user

    password = "ingenieriabiomedica1" #esta la obtengo desde MyAccount

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(user, password)

    server.send_message(msg)

    server.quit()
listaDeMails = ["andrea.cajal@hospitalitaliano.org.ar", "tamara.pinero@hospitalitaliano.org.ar"]

# Firebase Configuracion de conexion
firebaseConfig = {
    "apiKey": "AIzaSyBrGwM_jZCwwk3T-3dRPFq1hU2q2Gumo28",
    "authDomain": "r-pi-5fa93.firebaseapp.com",
    "databaseURL": "https://r-pi-5fa93-default-rtdb.firebaseio.com",
    "projectId": "r-pi-5fa93",
    "storageBucket": "r-pi-5fa93.appspot.com",
    "messagingSenderId": "72246664319",
    "appId": "1:72246664319:web:210c416fcdbdde4cc2b34a"
};
firebase=pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

maximo = 10
root = Tk()
root.title('Centro de Monitoreo')
varaibleSuperF = StringVar()
running = True  # Global flag
alarmaActivada = False # Global flag
tiempo_incio = ""# Global flag


def scanning():
    if running: 

        # Definicion de variables locales
        contador = 0
        TsensadaAcumulada = 0
        tpoInicialAlarma = datetime.now()
        tpoInicialPromedio = datetime.now()
        intervaloAlarma1 = 600
        intervalorAlarma2 = 300

        try:
            # PT1000
            temperaturaSuperF = AnalogIn(ads, ADS.P0, ADS.P1)
            valor_temperaturaSuperF = (temperaturaSuperF.value - ord)/pend
            Tmin_superF = -70
            Tmax_superF = -90

            # Impresion de variables
            valor_temperaturaSuperF = round(valor_temperaturaSuperF,2)
            print("Temperatura Super Freezer")
            print(valor_temperaturaSuperF)

            varaibleSuperF.set(str(valor_temperaturaSuperF))
            root.update()

            # Log de variables a Firebase
            # Temperatura Super-Freezer
            dataTemperaturaSuperF = {"TemperaturaSuperFreezer":valor_temperaturaSuperF}
            db.child("SuperFreezer-TemperaturaActual").set(dataTemperaturaSuperF)
            db.child("SuperFreezer-TemepraturaRegistro").push(dataTemperaturaSuperF)

            # Email de Alerta
            global alarmaActivada

            TsensadaAcumulada = TsensadaAcumulada + valor_temperaturaSuperF

            Tpromedio = TsensadaAcumulada / contador
            tpoFinalPromedio = datetime.now()
            delayPromedio =  tpoFinalPromedio - tpoInicialPromedio

            if valor_temperaturaSuperF < Tmax_superF or valor_temperaturaSuperF > Tmin_superF:
                tpoFinalAlarma = datetime.now()
                delta = tpoFinalAlarma- tpoInicialAlarma
                delayAlarma = delta.seconds

                if delayAlarma > intervaloAlarma1: 
                    if delayAlarma > intervalorAlarma2:
                        alarmaActivada = False

                    while alarmaActivada == False:
                        dateTimeObj=datetime.now()
                        fecha = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)") #ojo aca la hora que toma
                        alertSuperFreezer={"TempAlerta":valor_temperaturaSuperF,'Date': fecha}

                        if valor_temperaturaSuperF < Tmax_superF or valor_temperaturaSuperF > Tmin_superF:
                            db.child("TempAlerta").push(alertSuperFreezer)

                        if __name__ == '__main__': 
                            for mail in listaDeMails:
                                if valor_temperaturaSuperF < Tmax_superF or valor_temperaturaSuperF > Tmin_superF: 
                                    email_alert("Alerta de Temperatura", fecha + " -> Temp: " + str(valor_temperaturaSuperF), mail)
                                tpoInicialAlarma = datetime.now()
                                alarmaActivada = True
        except KeyboardInterrupt:
            print("Press Ctrl + C to terminate while statement")
            pass
        # After 5 minutes, call scanning again (create a recursive loop)
        root.after(300000 , scanning())

# Configuracion de la puesta en marcha
def start():
    """Enable scanning by setting the global flag to True."""
    global running
    running = True

def stop():
    """Stop scanning by setting the global flag to False."""
    global running
    running = False
root.title("Title")
root.geometry("500x500")

app = Frame(root)
app.pack()

start = Button(app, text="Start Scan", command=start)
stop = Button(app, text="Stop", command=stop)

labelTxtTemp = Label(app,text = "Temperatura Super-Freezer Actual:",font=("Verdana",21))
labelTxtTemp.pack()
labelTemp = Label(app,textvariable=varaibleSuperF,font=("Verdana",18))
labelTemp.pack()

start.pack()
stop.pack()

root.after(300000 , scanning)  # After 5 minutes, call scanning
root.mainloop()