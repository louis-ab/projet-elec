from machine import Pin
from time import sleep
from dht import DHT11

dht = DHT11(Pin(6))

pin = [
    Pin(0, Pin.OUT),
    Pin(1, Pin.OUT),
    Pin(2, Pin.OUT),
    Pin(3, Pin.OUT)]

led = [
    Pin(19, Pin.OUT),
    Pin(20, Pin.OUT),
    Pin(21, Pin.OUT)]

transi = [Pin(26, Pin.OUT), Pin(27, Pin.OUT)]

def bin(x): #convertir le nombre en binaire
    return([int(x>>(3-i))%2 for i in range(4)])

def show(x): #afficher un nombre sur le 7-segment
    val = bin(x)
    for i in range(4):
        pin[i].value(val[i])

def tempRGB(x): #la couleur en fonction de la température
    return [max(0,15-abs(x-15)), max(0,15-x), max(0,x-15)] #GBR

time = 3 #s
speed = 120 #Hz

while True:
    dht.measure()
    temp = dht.temperature()
    print("température :", temp)
    colors = tempRGB(temp)
    for i in range(time*speed):
        for j in range(15): #on allume une couleur un temps proportionnel à la valeur à chaque cycle
            for c in range(3):
                if colors[c] > j:
                    led[c].value(1)
                else:
                    led[c].value(0)
            #on pourrait mettre un sleep ici mais le temps de calcul fait que ça marche assez bien sans
        transi[0].value(1)
        transi[1].value(0) #on sélectionne un affichage avec les transistors
        show(temp//10)
        sleep(1/speed)
        transi[0].value(0)
        transi[1].value(1) #puis l'autre
        show(temp%10)
        sleep(1/speed)
    show(15) #on vide l'affichage le temps que la sonde mesure la température
