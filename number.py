import serial
import time
import json

def send_star_patterns(count1,count2, red , green ,com_port='COM17', json_filename="number.json",  baud_rate=115200):
    try:
        # JSON dosyasını okuyun
        with open(json_filename, 'r') as f:
            star_patterns = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_filename} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {json_filename}.")
        return

    try:
        # Seri portu açın
        with serial.Serial(com_port, baud_rate, timeout=1) as ser:
            time.sleep(2)  # Seri bağlantının kurulmasını bekleyin

            def send_pattern(pattern, red, green):
                json_data = {
                    "red": red,
                    "green": green,
                    "data": pattern
                }
                ser.write(json.dumps(json_data).encode('utf-8') + b'\n')
                time.sleep(0.10)

            # Desenleri ters sırayla gönderin
            reversed_items = list(star_patterns.items())[:count1][::-1]
            for name, pattern in reversed_items:
                # print(f"Ugradylan san: {name}")
                if pattern[0]==2:
                    send_pattern(pattern, False, False)
                else:
                    send_pattern(pattern, red, green)
                time.sleep(1)  # Her desen arasında 1 saniye bekle
                #print(com_port)
            time.sleep(3)
            reversed_items2 = list(star_patterns.items())[:count2][::-1]
            for name, pattern in reversed_items2:
                # print(f"Ugradylan san: {name}")
                if pattern[0]==2:
                    send_pattern(pattern, False, False)
                else:
                    send_pattern(pattern, not red, not green)
                time.sleep(1)
                #print(com_port)
    except serial.SerialException as e:
        print(f"Error: {e}")
        return
# json_filename = 'number.json'
# pattern_count = 15

# while True:
    
#     send_star_patterns(json_filename, pattern_count,True,False)
#     send_star_patterns(json_filename, pattern_count,False,True)