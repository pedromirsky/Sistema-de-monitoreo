# Librerias
from tkinter import *
import pyrebase
import random
import time 
from datetime import datetime
from email.message import EmailMessage
import Adafruit_DHT as dht
import smtplib

# Parametro para DHT
sensor = dht.DHT22

# Funcion Email
def email_alert(subject, body, to):

    msg = EmailMessage()

    msg.set_content(body)

    msg['subject'] = subject

    msg['to'] = to

    #esto es QUIEN lo manda

    user = "monitortemperaturaiuhi@gmail.com"

    msg['from'] = user

    password = "qexjdbhigwoanyiy" #esta la obtengo desde MyAccount

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(user, password)

    server.send_message(msg)

    server.quit()
listaDeMails = ["graciela.dabrowski@hospitalitaliano.org.ar", "emiliana.herrero@hospitalitaliano.org.ar"]

# Firebase Configuracion de conexion
firebaseConfig = {
    "apiKey": "AIzaSyBrGwM_jZCwwk3T-3dRPFq1hU2q2Gumo28",
    "authDomain": "r-pi-5fa93.firebaseapp.com",
    "databaseURL": "https://r-pi-5fa93-default-rtdb.firebaseio.com",
    "projectId": "r-pi-5fa93",
    "storageBucket": "r-pi-5fa93.appspot.com",
    "messagingSenderId": "72246664319",
    "appId": "1:72246664319:web:210c416fcdbdde4cc2b34a"
}
firebase=pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

maximo = 10
root = Tk()
root.title('Centro de Monitoreo')
variableTemp = StringVar()
variableHum = StringVar()
running = True  # Global flag
alarmaActivada = False # Global flag
tiempo_incio = ""# Global flag


def scanning():
    if running:  # Only do this if the Stop button has not been clicked

        # Definicion de variables locales
        tpoInicialAlarma = datetime.now()
        tpoInicialPromedio = datetime.now()
        intervaloAlarma = 43200

        try:
            # DHT
            humedad,temperatura = dht.read_retry(sensor,4)
            valor_temp = temperatura
            valor_hum = humedad
            Tmin_bioterio = 20
            Tmax_bioterio = 26

            # Impresion de variables
            valor_temp = round(valor_temp,2)
            valor_hum = round(valor_hum,2)
            print("Temp")
            print(valor_temp)
            print("Humedad:")
            print(valor_hum)

            variableTemp.set(str(valor_temp))
            variableHum.set(str(valor_hum))
            root.update()

            # Log de variables a Firebase
            # Temperatura DHT
            dataTemperatura={"Temperatura":valor_temp}
            db.child("BioterioTemperaturaActual").set(dataTemperatura)
            db.child("BioterioTemperaturaRegistro").push(dataTemperatura)
            # Humedad DHT
            dataHumedad={"Humedad":valor_hum}
            db.child("BioterioHumedadActual").set(dataHumedad)
            db.child("BioterioHumedadRegistro").push(dataHumedad)

            # Email de Alerta
            global alarmaActivada

            if valor_temp > Tmax_bioterio or valor_temp < Tmin_bioterio:
                tpoFinalAlarma = datetime.now()
                delta = tpoFinalAlarma - tpoInicialAlarma
                delayAlarma = delta.seconds

                if delayAlarma > intervaloAlarma:
                    alarmaActivada = False

                while alarmaActivada== False:
                    dateTimeObj=datetime.now()
                    fecha = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)") #ojo aca la hora que toma
                    alertaBioterio={"TempAlerta":valor_temp,'Date': fecha, 'HumAlerta': valor_hum}
                    if valor_temp > Tmax_bioterio or valor_temp < Tmin_bioterio:
                        db.child("BioterioAlertaRegistro").push(alertaBioterio)

                    if __name__ == '__main__': 
                        for mail in listaDeMails:
                            if valor_temp > Tmax_bioterio or valor_temp < Tmin_bioterio: 
                                email_alert("Alerta de Temperatura", fecha + " -> Temp: " + str(valor_temp) + " -> Hum: " + str(valor_hum) , mail)
                            tpoInicialAlarma = datetime.now()
                            alarmaActivada = True
        except KeyboardInterrupt:
            print("Press Ctrl + C to terminate while statement")
            pass

        # After 1 hour, call scanning again (create a recursive loop)
        root.after(3600000 , scanning())


# Configuracion de programa
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

labelTxtTemp = Label(app,text = "Temperatura Actual:",font=("Verdana",21))
labelTxtTemp.pack()
labelTemp = Label(app,textvariable=variableTemp,font=("Verdana",18))
labelTemp.pack()

labelTxtHum = Label(app,text = "Humedad Actual:",font=("Verdana",21))#,bg='light grey')
labelTxtHum.pack()
labelHum = Label(app,textvariable=variableHum,font=("Verdana",18))
labelHum.pack()

start.pack()
stop.pack()

root.after(3600000, scanning)  # After 1 second, call scanning
root.mainloop()