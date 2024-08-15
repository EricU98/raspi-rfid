import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pyautogui
import time

reader = SimpleMFRC522()

def convert_uid_to_decimal(uid_bytes):
    # UID ist eine Liste von vier Bytes: [Byte1, Byte2, Byte3, Byte4]
    decimal_id = (uid_bytes[0] << 24) + (uid_bytes[1] << 16) + (uid_bytes[2] << 8) + uid_bytes[3]
    return decimal_id

try:
    while True:
        print("Warte auf Tag...")
        id, text = reader.read()
        # Extrahiere die UID-Bytes manuell
        uid_bytes = [147, 126, 218, 155]  # Ersetzen Sie dies durch Ihre UID-Byte-Werte
        decimal_id = convert_uid_to_decimal(uid_bytes)
        print("Gelesen: ID: %s" % decimal_id)
        pyautogui.write(str(decimal_id))
        pyautogui.press('enter')
        time.sleep(1)
finally:
    GPIO.cleanup()
