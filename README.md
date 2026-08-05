# 🌊️ FlowControlHD
### A GUI program designed to work with Arduino UNO R3 and a motor to flow water based from values in a CSV file.
*** 
## 📌️ Prerequisites 
- Platform IO
- Python (Including: MatplotLib, Pyrealtime, Customtkinter, Pyserial)
use the following to install the required libraries:
```
pip install matplotlib
pip install mplcyberpunk
pip install pyserial
pip install customtkinter
pip install pyrealtime
```
### 🔌️ Materials
- Arduino UNO R3
    - Motor Shield: (Remove the connection between the power-supply and vin for the arduino.)
- External Power supply
- Flow sensor (Specific one used in this project linked here: https://www.digikey.ca/en/products/detail/dfrobot/SEN0549/18069228)
- Motor (Specific one used in this project linked here: https://www.kamoer.com/us/product/detail.html?id=10017)
- Plastic tubing (Specific one used in this project are: 3mm tubing & 6mm)
  
## Features
### 🌸️ User friendly interface
<img width="1307" height="715" alt="Screenshot from 2026-08-05 11-27-38" src="https://github.com/user-attachments/assets/ce9e474c-377f-42a4-94e9-6bca95110a70" />

  
  ### 📷️ Live Graph: displays output from Arduino or flow sensor over Pyserial
  <img width="600" height="405" alt="Screencastfrom2026-07-29110630AM-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/72ada6c3-df7b-43f5-b9d8-3c8ae9b2ea50" />

## How To Use
- Build & Upload 'main.cpp' to the Arduino with platform IO.
- Turn on the power supply.
- Run the python program. 
- To import a csv file into the program, click on import file. Then, the contents of the file you have selected will be displayed in the output box.
Once you have your file selected, ensure you have viewed the 'preview' graph to know the expected output. Then, click upload and now you should be able to view
live input by clicking the bottom button.

**To change Live Graph to display either Arduino or flow sensor output:**
  - Find the line near the end of "Main.cpp" which contains two comments about its function and warnings.
  - Edit "Serial.println();" to either "Serial.println(array);" or "Serial.println(flow_average);"
### ⚠️ WARNING!!!
Ensure you follow the steps in order, otherwise bugs or other issues may occur.
