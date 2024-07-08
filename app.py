import cv2
from ultralytics import YOLO
import threading
from concurrent.futures import ThreadPoolExecutor
import serial
import json
import time

# Load YOLO model
model = YOLO("yenilmodelm.pt")

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
        name = labels[int(label)]
        # if name == 'awtoulag':
        if name in obyekt_sany:
            obyekt_sany[name] += 1
        else:
            obyekt_sany[name] = 1

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

    if jem == 0:
        t = 30
    else:
        kopeltmek = uly * 100
        bolmek = kopeltmek // jem
        kop = bolmek * 60
        t = kop // 100

    m = 60 - t
    if (total_sany1 == 0 or total_sany2 == 0) or (total_sany1 == 0 and total_sany2 == 0):
        with ThreadPoolExecutor() as executor:
            executor.submit(send_star_patterns, 30, 30, True, False, 'COM22')
            executor.submit(send_star_patterns, 30, 30, False, True, 'COM5')
    elif total_sany1 < total_sany2:
        with ThreadPoolExecutor() as executor:
            executor.submit(send_star_patterns, t, m, False, True, 'COM22')
            executor.submit(send_star_patterns, t, m, True, False, 'COM5')
    elif total_sany1 > total_sany2:
        with ThreadPoolExecutor() as executor:
            executor.submit(send_star_patterns, t, m, True, False, 'COM22')
            executor.submit(send_star_patterns, t, m, False, True, 'COM5')

def send_star_patterns(count1, count2, red, green, com_port='COM22', json_filename="number.json", baud_rate=115200):
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

            def send_pattern(pattern, red, green):
                json_data = {
                    "red": red,
                    "green": green,
                    "data": pattern
                }
                ser.write(json.dumps(json_data).encode('utf-8') + b'\n')
                time.sleep(0.1)

            reversed_items = list(star_patterns.items())[:count1][::-1]
            for name, pattern in reversed_items:
                print(f"Ugradylan san: {name}")
                if pattern[0] == 2:
                    send_pattern(pattern, False, False)
                else:
                    send_pattern(pattern, red, green)
                time.sleep(1)

            time.sleep(3)
            reversed_items2 = list(star_patterns.items())[:count2][::-1]
            for name, pattern in reversed_items2:
                print(f"Ugradylan san: {name}")
                if pattern[0] == 2:
                    send_pattern(pattern, False, False)
                else:
                    send_pattern(pattern, not red, not green)
                time.sleep(1)
    except serial.SerialException as e:
        print(f"Error: {e}")
        return

def main():
    cap1 = cv2.VideoCapture(1)
    cap2 = cv2.VideoCapture(0)

    if not cap1.isOpened() or not cap2.isOpened():
        print("Error: Could not open video capture devices.")
        return

    try:
        while True:
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            if not ret1 or not ret2:
                break

            process_frames(frame1, frame2)
    finally:
        cap1.release()
        cap2.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
