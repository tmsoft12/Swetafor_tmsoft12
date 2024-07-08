import cv2
from ultralytics import YOLO
import threading
import time
import serial



import json

def send_star_patterns(json_filename, count, com_port='COM8', baud_rate=115200):
    try:
        with open(json_filename, 'r') as f:
            star_patterns = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_filename} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {json_filename}.")
        return
    try:
        
        with serial.Serial(com_port, baud_rate, timeout=1) as ser:
            time.sleep(2)  

            def send_pattern(pattern):
                for row in pattern:
                    for value in row:
                        ser.write(bytes([value]))
                        time.sleep(0.01)

          
            reversed_items = [(name, pattern) for name, pattern in star_patterns.items()][:count][::-1]
            for name, pattern in reversed_items:
                print(f"Gönderilen desen: {name}")
                send_pattern(pattern)
                time.sleep(1)  
    except serial.SerialException as e:
        print(f"Error: {e}")
        return




model = YOLO("agyrmodelx.pt")


labels = [
    'adam', 'welosiped', 'awtoulag', 'motosikl', 'ucar', 'awtobus', 'otly', 'awtoulag',
    'gayyk', 'svetofor', 'yangyn gidranty', 'durmak belgisi', 'awtoulag duralgo olceyji', 'uzyn oturgyc',
    'gus', 'pisik', 'it', 'at', 'goyun', 'sygyr', 'pil', 'ayy', 'zebra',
    'zirafa', 'arka asylyan sumka', 'sayawan', 'el sumka', 'galstuk', 'çemodan', 'frisbe',
    'buzda tayylyan liza', 'snoubord', 'sport topy', 'bat borek', 'beysbol tayagy', 'beysbol ellik',
    'skeytbord', 'surfboard', 'tennis raketasy', 'cuyse', 'wino cuysesi', 'kase bokal',
    'cennek', 'pycak', 'cemce', 'jam', 'banan', 'alma', 'sandwic', 'pyrtykal',
    'brokoli', 'kasir', 'hot dog', 'pizza', 'donut', 'tort', 'oturgyc', 'diwan',
    'kuyzedaki gul', 'krowat dusek', 'iywicilyan stol', 'hajathana', 'telewizor', 'noutbuk', 'myska sycan',
    'pult', 'klawiatura', 'telefon', 'mikrawolnowka', 'dyhowka', 'toster', 'umwalnik',
    'holodilnik', 'kitap', 'sagat', 'waza', 'gaycy', 'oyunjak ayy', 'sac fen',
    'dis cotga'
]

model_lock = threading.Lock()

def count_objects(frame, obyekt_sany):
    with model_lock:
        results = model(frame)
    for i in range(len(results[0].boxes)):
        score = results[0].boxes.conf[i]
        label = results[0].boxes.cls[i]
        if score < 0.2:
            continue
        name = labels[int(label)]

        if name in obyekt_sany:
            obyekt_sany[name] += 1
        else:
            obyekt_sany[name] = 1
def process_frames(frame1, frame2):
    obyekt_sany1 = {}
    obyekt_sany2 = {}

    thread1 = threading.Thread(target=count_objects, args=(frame1, obyekt_sany1))
    thread2 = threading.Thread(target=count_objects, args=(frame2, obyekt_sany2))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
   
    total_sany2 = sum(obyekt_sany2.values())  # Total count from second camera
    total_sany1 = sum(obyekt_sany1.values()) 
    jem = total_sany2 + total_sany1
    uly = 1
    if(total_sany2>total_sany1):
        uly = total_sany2
    elif(total_sany2 ==0 and total_sany1 ==0):
        return
    else:
        uly = total_sany1
        
    kopeltmek = uly * 100
    bolmek = kopeltmek // jem
    kop = bolmek * 60
    t = kop // 100
    if(total_sany2 ==0 or total_sany1 ==0):
        t = 30
    print("cam1",total_sany1)
    print("cam2",total_sany2)     
    print(t)
   
    if total_sany1 > total_sany2:
        print("cam1")
        time.sleep(2)
        send_star_patterns('number.json', t)
        time.sleep(t)
      
    elif total_sany1 < total_sany2:
        print("cam2")

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

while cap1.isOpened() and cap2.isOpened():
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        break

    process_frames(frame1, frame2)

cap1.release()
cap2.release()