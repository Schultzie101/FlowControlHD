#---IMPORTANT: Having both ther serial monitor and python script running simontaniously (cant spell) is NOT compatible.

import serial 
import numpy as np
import time

serial_port = "/dev/ttyACM0"
baud_rate = 115200
file_path = "/home/emma/Documents/PlatformIO/Unsorted-Seed2Stem-2026-/Projects/Realistic Pulse 2 Digital/csv files/pulse.csv"


array = np.loadtxt(file_path, delimiter=',')
array_bytes = array.astype (np.float32).tobytes()
#array_bytes = array[:8].astype (np.float32).tobytes()


#import array into text box. 
# array_textbox.insert("1.0", array)

#Serial 
ser = serial.Serial(serial_port, baud_rate)  
# wait for arduino to reset.  
time.sleep(2)
# format = '<' + 'f' * len(array[:16])
 # Send the binary data
ser.write(array_bytes)
print(array_bytes)
# time.sleep(1)

while True:
    line = ser.readline().decode('utf=8').strip()
    if not line: 
        break 
    print(f"[ser]: {line}")
ser.close()