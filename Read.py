import RPi.GPIO as GPIO
import spidev
import time
import pyautogui

# SPI-Initialisierung
spi = spidev.SpiDev()
spi.open(0, 0)  # Öffne SPI-Port 0, Device (CS) 0
spi.max_speed_hz = 1000000  # Setze die Geschwindigkeit

# GPIO-Initialisierung
RST_PIN = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(RST_PIN, GPIO.OUT)
GPIO.output(RST_PIN, 1)

# Funktion zum Schreiben auf den MFRC522
def spi_write(address, value):
    spi.xfer([address << 1, value])

# Funktion zum Lesen vom MFRC522
def spi_read(address):
    result = spi.xfer([address << 1 | 0x80, 0])
    return result[1]

# Reset des MFRC522
def mfrc522_reset():
    spi_write(0x01, 0x0F)

# Funktion zum Lesen der UID
def read_uid():
    spi_write(0x0D, 0x07)  # Setze Bit Framing
    spi_write(0x01, 0x0C)  # Sende Antikollisionsbefehl
    response = spi.xfer([0x93, 0x20, 0, 0, 0, 0, 0])  # Sende Antikollisionsdaten
    return response[2:6]  # Extrahiere die UID

# Main-Loop
try:
    while True:
        uid = read_uid()
        if uid:
            decimal_id = (uid[3] << 24) + (uid[2] << 16) + (uid[1] << 8) + uid[0]
            formatted_id = str(decimal_id).zfill(10)
            print("UID: ", formatted_id)
            pyautogui.write(formatted_id)
            pyautogui.press('enter')
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    spi.close()
