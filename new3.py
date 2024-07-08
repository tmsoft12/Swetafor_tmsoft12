import cv2
from ultralytics import YOLO
import threading
import time
import serial
import json
from concurrent.futures import ThreadPoolExecutor
from number import send_star_patterns

# Load YOLO model
model = YOLO("agyrmodelx.pt")

# List of labels
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

# Create a lock object
model_lock = threading.Lock()

def count_objects(frame, obyekt_sany):
    with model_lock:
        results = model(frame)

    for i in range(len(results[0].boxes)):
        score = results[0].boxes.conf[i]
        label = results[0].boxes.cls[i]

        if score < 0.2:
            continue
        # if label == 7:
        name = labels[int(label)]
        if(name == 'awtoulag'):
            
            if name in obyekt_sany:
                obyekt_sany[name] += 1
            else:
                obyekt_sany[name] = 1
        else:
            continue

def process_frames(frame1, frame2):
    obyekt_sany1 = {}
    obyekt_sany2 = {}

    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(count_objects, frame1, obyekt_sany1)
        future2 = executor.submit(count_objects, frame2, obyekt_sany2)

        future1.result()
        future2.result()

    total_sany1 = sum(obyekt_sany1.values())
    total_sany2 = sum(obyekt_sany2.values())
    jem = total_sany2 + total_sany1
    uly = max(total_sany1, total_sany2)
    print('cam1',obyekt_sany1)
    print('cam2',obyekt_sany2)
    if jem == 0:
        t=30
    else:
        kopeltmek = uly * 100
        bolmek = kopeltmek // jem
        kop = bolmek * 60
        t = kop // 100

    # if total_sany1 == 0 or total_sany2 == 0:
    #     t = 30

    print("cam1", total_sany1)
    print("cam2", total_sany2)
    m = 60 - t
    print(t, m)
    if (total_sany1 == 0 or total_sany2 == 0) or (total_sany1 == 0 and total_sany2 == 0):
        with ThreadPoolExecutor() as executor:
            executor.submit(send_star_patterns, 30,30, True, False, 'COM17')
            executor.submit(send_star_patterns, 30,30, False, True, 'COM8')
    elif total_sany1 < total_sany2:
        with ThreadPoolExecutor() as executor:
            executor.submit(send_star_patterns, t,m, False, True, 'COM17')
            executor.submit(send_star_patterns, t,m, True, False, 'COM8')
    elif total_sany1 > total_sany2:
        with ThreadPoolExecutor() as executor:
            executor.submit(send_star_patterns, t,m, True, False, 'COM17')
            executor.submit(send_star_patterns, t,m, False, True, 'COM8')

# Open the video capture devices
cap1 = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(0)

if not cap1.isOpened() or not cap2.isOpened():
    print("Error: Could not open video capture devices.")
else:
    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        process_frames(frame1, frame2)

    # Release the video captures
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()
