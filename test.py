import serial
import time

# Arduino'nun bağlı olduğu seri portu ve baud rate'i ayarlayın
ser = serial.Serial('COM8', 115200)  # 'COM3' Windows için. Linux/Mac'te '/dev/ttyUSB0' olabilir.

time.sleep(2)  # Arduino'nun resetlenmesini bekleyin

def set_pin(pin, state):
    if pin == 8:
        if state == 'HIGH':
            ser.write(b'8')
        elif state == 'LOW':
            ser.write(b'0')
    elif pin == 9:
        if state == 'HIGH':
            ser.write(b'9')
        elif state == 'LOW':
            ser.write(b'1')

# D8 pinini HIGH yap
set_pin(8, 'HIGH')
time.sleep(1)  # 1 saniye bekle

# D8 pinini LOW yap
set_pin(8, 'LOW')
time.sleep(1)  # 1 saniye bekle

# D9 pinini HIGH yap
set_pin(9, 'HIGH')
time.sleep(1)  # 1 saniye bekle

# D9 pinini LOW yap
set_pin(9, 'LOW')
time.sleep(1)  # 1 saniye bekle

ser.close()  # Seri portu kapat
