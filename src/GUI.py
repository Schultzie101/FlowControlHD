#---IMPORT LIBARYS---
import numpy as np
import struct
import customtkinter as ctk
from customtkinter import filedialog
import serial 
#--matplotlib imports--
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import matplotlib.animation as animation
import mplcyberpunk
import colorsys
import time 
import pyrealtime as prt

## Stylize matplotlib 
plt.rcParams['figure.facecolor'] = "#272727" 
plt.rcParams['axes.facecolor'] = "#272727"
plt.rcParams['grid.color'] = "#6E6E6E"


class RGBTEXT(ctk.CTkFrame):
    def __init__(self, master, text, font=("Arial", 16), speed=30, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.offset = 0.0
        self.speed = speed
        self.labels = [ctk.CTkLabel(self, text=c, font=font) for c in text]
        for lbl in self.labels:
            lbl.pack(side="left", padx=0)
        self.animation()

    def animation(root):
        n = len(root.labels)
        for i, lbl in enumerate(root.labels):
            hue = ((i / n) + root.offset) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.6, 1.0)
            lbl.configure(text_color=f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}')
        root.offset += 0.01
        root.after(root.speed, root.animation)


#--import file--
def OPEN_FILE():
    file_path = filedialog.askopenfilename(parent=root, title='Select a CSV file to import', filetypes= [("CSV Files", "*csv"),])
    if file_path:
        file_selected.configure(text=file_path)
    #--Load selected file into an array--
    global array 
    array = np.loadtxt(file_path, delimiter=',')
    global array_bytes 
    array_bytes = array.astype (np.float32).tobytes()

    #import array into text box. 
    array_textbox.insert("1.0", array)

#--Run serial--
def UPLOAD_ARRAY():
    #Serial 
    global ser
    ser = serial.Serial(serial_port, baud_rate)  
    # wait for arduino to reset.  
    time.sleep(2)
    ser.write(array_bytes)
    print("The array has been uploaded sucessfully!")
    time.sleep(0.5)


# #CSV Graph window 
def GRAPH_WINDOW():
    #--Setup matplotlib graph--
    #Note: Since the CSV files only include Y values, this line creates the x values.
    fig, ax_preview = plt.subplots()
    x_array = np.linspace(0,1,num=array.size)
    ax_preview.plot(x_array,array, color="#FF95BE")
    ax_preview.set_title("CSV Graph (PREVIEW)")
    ax_preview.set_xlabel("Time(Seconds)")
    ax_preview.set_ylabel("Blood-Flow Velocity (Noramized)")
    mplcyberpunk.add_glow_effects(gradient_fill=True)
    plt.show()

def LIVE_GRAPH_WINDOW():
    #Pyrealtime 
    serial_layer = prt.SerialReadLayer(device_name=serial_port, baud_rate=baud_rate)
    prt.TimePlotLayer(serial_layer, window_size=200, ylim=(90, 256))
    prt.LayerManager.session().run()
    

if __name__== "__main__":
    #---INITIALIZE CTK--
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("/home/emma/Documents/PlatformIO/Unsorted-Seed2Stem-2026-/Projects/Realistic Pulse 2 Digital/src/pink.json")

    # ---GUI--- 
    root = ctk.CTk()
    root.title("FlowControl-HD")
    root.geometry("890x710")
    window_frame = ctk.CTkFrame(master=root, fg_color="transparent")

    #setup main-window centering 
    window_frame.pack(pady=20,padx=20,fill="both",expand=True)
    window_frame.grid_columnconfigure(0, weight=1)
    window_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
    title_text = RGBTEXT(window_frame, text="[ FlowControl-HD ]", font=("Arial",40, "bold"))
    title_text.grid(column=0,row=0)


    # --Textbox for selected file--
    array_textbox = ctk.CTkTextbox(master=window_frame, width=850, height=400,)
    array_textbox.grid(column=0, row=3)
    #Serial port. 
    serial_port = "/dev/ttyACM0"
    baud_rate = 115200


    #Buttons for main window
    import_file = ctk.CTkButton(master=window_frame, text="Import File", 
                                font=("Arial",25,"bold"), width=400, height=50, command=OPEN_FILE)
    import_file.grid(column=0, row=1)

    #--Show current selected file--
    file_selected = ctk.CTkLabel(master=window_frame, text="No file is currently selected. DO NOT OPEN GRAPH!!")
    file_selected.grid(column=0,row=2)

    # Preview Graph
    still_graph = ctk.CTkButton(master=window_frame, text="Preview",  font=("Arial",25,"bold"), width=700, height=45,command=GRAPH_WINDOW)
    still_graph.grid(column=0, row=4,)

    #Upload Array
    upload_array = ctk.CTkButton(master=window_frame, text="Upload Array",  font=("Arial",25,"bold"), width=700, height=45,command=UPLOAD_ARRAY)
    upload_array.grid(column=0, row=5,)

    #Live graph
    live_graph  = ctk.CTkButton(master=window_frame, text="Live Graph",  font=("Arial",25,"bold"), width=700, height=45,command=LIVE_GRAPH_WINDOW)
    live_graph.grid(column=0, row=6,)

    root.mainloop()
