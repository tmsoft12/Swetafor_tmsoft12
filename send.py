import serial
import json
import time

# Seri port bağlantısını başlat
ser = serial.Serial('COM17', 115200) # Arduino'nun bağlı olduğu seri portu belirtin, baud oranı ile birlikte

# Arduino'ya JSON gönderme fonksiyonu
def send_json(red, green, data):
    json_data = {
        "red": red,
        "green": green,
        "data": data
    }
    ser.write(json.dumps(json_data).encode('utf-8') + b'\n')

# Veri setleri
data = {
    "1": [0, 0, 0, 0, 0, 0, 0,   # 0. satır
          0, 0, 0, 1, 0, 0, 0,   # 1. satır
          0, 0, 1, 1, 0, 0, 0,   # 2. satır
          0, 0, 0, 1, 0, 0, 0,   # 3. satır
          0, 0, 0, 1, 0, 0, 0,   # 4. satır 
          0, 0, 0, 1, 0, 0, 0,   # 5. satır
          0, 0, 0, 0, 0, 0, 0],  # 6. satır

    "2": [0, 0, 0, 0, 0, 0, 0,   # 0. satır
          0, 0, 1, 1, 1, 0, 0,   # 1. satır
          0, 0, 0, 0, 1, 0, 0,   # 2. satır
          0, 0, 1, 1, 1, 0, 0,   # 3. satır
          0, 0, 1, 0, 0, 0, 0,   # 4. satır
          0, 0, 1, 1, 1, 0, 0,   # 5. satır
          0, 0, 0, 0, 0, 0, 0]   # 6. satır
}

try:
    for key in data:
        send_json(red=True, green=True, data=data[key])
        for d in data:
            dd= int(d)
            print(dd)
            time.sleep(dd)  # 1 saniye bekle

except KeyboardInterrupt:
    print("Program kapatıldı.")

# Programın sonlandığını belirt
print("Tüm veri setleri gönderildi, program sonlandırıldı.")
