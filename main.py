#librairies importées
from pathlib import Path
from time import sleep
from sense_hat import SenseHat
from gpiozero import CPUTemperature
from datetime import datetime
from orbit import ISS, ephemeris
from skyfield.api import load

#définitions des variables
maison = Path(__file__).parent.resolve()
data_file = maison / "data.csv"
capteur = SenseHat()
timescale = load.timescale()
O = [0, 0, 0]  # Nothing
A = [255, 255, 255]  # White
B=  [100, 100, 200]  #Blue
C=  [100, 200, 100]  #Green
D=  [200, 100, 100] # Red
logo_led = [
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, A, B, A, C, O, O,
O, O, B, A, C, A, O, O,
O, O, A, C, A, D, O, O,
O, O, C, A, D, A, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O
]

def arrondir(n):
    return int(n * 1000)/1000

#création et écriture du fichier de stockage
with open(data_file, "w", buffering=1) as f:
    f.write("time, temperature of the sensor, temperature of the processor,L:light or D:dark\n")
    for i in range(1078):
        t = timescale.now()
        temp = capteur.get_temperature()
        cpu = CPUTemperature()
        tempreal = arrondir(temp)
        tempproc = arrondir(cpu.temperature)
        mtnt = datetime.now()
        heure = mtnt.strftime("%H")
        minutes = mtnt.strftime("%M")
        secondes = mtnt.strftime("%S")
        capteur.set_pixels(logo_led)
        sleep(5)
        capteur.clear()
        sleep(5)
        f.write(f"{heure}h {minutes}min {secondes}sec, {tempreal}°C, {tempproc}°C,")
        if ISS.at(t).is_sunlit(ephemeris):
            f.write("L\n")
        else:
            f.write("D\n")

