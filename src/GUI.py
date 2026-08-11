#---IMPORT LIBARYS---
import numpy as np
import customtkinter as ctk
from customtkinter import filedialog
import serial 
#--matplotlib imports--
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
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
    file_path = filedialog.askopenfilename(parent=self, title='Select a CSV file to import', filetypes= [("CSV Files", "*csv"),])
    if file_path:
        file_selected.configure(text=file_path)
        #--Load selected file into an array--
        global array 
        array = np.loadtxt(file_path, delimiter=',')
        global array_bytes 
        array_bytes = array.astype (np.float32).tobytes()

        #import array into text box. 
        array_textbox.insert("1.0", array)
        OPEN_FILE.array_imported=True
OPEN_FILE.array_imported=False

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
    UPLOAD_ARRAY.array_uploaded = True
UPLOAD_ARRAY.array_uploaded = False


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
    prt.TimePlotLayer(serial_layer, window_size=200, ylim=(0,250))
    plt.xlabel("Time (samples)")
    plt.ylabel("Volume (mL)")
    prt.LayerManager.session().run()

def ERROR_WINDOW_IMPORT():
    window = ctk.CTkToplevel(self)
    window.title("Error")
    window.geometry("700x75")
    text = ctk.CTkLabel(window, text="You have not yet imported a file. Please import a file before opening the preview graph.")
    text.pack(padx=20, pady=20)

def ERROR_WINDOW_UPLOAD():
    window = ctk.CTkToplevel(self)
    window.title("Error")
    window.geometry("500x75")
    text = ctk.CTkLabel(window, text="You have not yet uploaded your array")
    text.pack(padx=20, pady=20)

def FILE_SELECTION_CHECK():
    if OPEN_FILE.array_imported:
        GRAPH_WINDOW()
    else: 
        ERROR_WINDOW_IMPORT()

def FILE_UPLOAD_CHECK():
    if UPLOAD_ARRAY.array_uploaded:
        LIVE_GRAPH_WINDOW()
    else: 
        ERROR_WINDOW_UPLOAD()

def FILE_SELECTION_CHECK_4UP():
    if OPEN_FILE.array_imported:
        UPLOAD_ARRAY()
    else: 
        ERROR_WINDOW_IMPORT()


if __name__== "__main__":
    #---INITIALIZE CTK--
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("/home/emma/Documents/PlatformIO/Unsorted-Seed2Stem-2026-/Projects/Realistic Pulse 2 Digital/src/pink.json")

    # ---GUI--- 
    self = ctk.CTk()
    self.title("FlowControl-HD")
    self.geometry("890x710")
    self.minsize(550, 710)
    #self.resizable(False, False)

    #Three frames for scaling purposes. 
    #---------------------------------------------------------------
    window_upper = ctk.CTkFrame(master=self, fg_color="transparent")
    window_upper.pack(pady=10, padx=10, fill="x")
    window_upper.grid_columnconfigure(0, weight=1)
    window_upper.grid_rowconfigure((3), weight=0)
    window_upper.grid_rowconfigure((0), weight=0)
    window_upper.grid_rowconfigure((1,2), weight=0)

    window_middle = ctk.CTkFrame(master=self, fg_color="transparent")
    window_middle.pack(pady=10,padx=10, fill="both")
    window_lower = ctk.CTkFrame(master=self, fg_color="transparent")
    window_lower.pack(pady=10, padx=10, fill="x")
    window_lower.grid_columnconfigure([0,1,2,3], weight=1)
    window_lower.rowconfigure([0,1], weight=0)
    

    #setup main-window centering 
    window_middle.pack(pady=20,padx=20,fill="both",expand=True)
    window_middle.grid_columnconfigure(0, weight=1)
    window_middle.grid_rowconfigure((0), weight=1)
    #---------------------------------------------------------------
    title_text = RGBTEXT(window_upper, text="[ FlowControl-HD ]", font=("Arial",40, "bold"))
    title_text.grid(column=0, row=0)


    # --Textbox for selected file--
    array_textbox = ctk.CTkTextbox(master=window_middle, width=850, height=400,)
    array_textbox.grid(column=0, row=0, sticky="nsew")
    #Serial port. 
    serial_port = "/dev/ttyACM0"
    baud_rate = 115200


    #Buttons for main window
    import_file = ctk.CTkButton(master=window_upper, text="Import File", 
                                font=("Arial",25,"bold"), width=400, height=50, command=OPEN_FILE)
    import_file.grid(column=0, row=1)

    #--Show current selected file--
    file_selected = ctk.CTkLabel(master=window_upper, text="No file is currently selected.")
    file_selected.grid(column=0,row=2)

    # Preview Graph
    still_graph = ctk.CTkButton(master=window_lower, text="Preview",  font=("Arial",25,"bold"), width=700, height=60,command=FILE_SELECTION_CHECK)
    still_graph.grid(column=0, row=0,sticky="nsew")

    #Upload Array
    upload_array = ctk.CTkButton(master=window_lower, text="Upload Array",  font=("Arial",25,"bold"), width=700, height=60,command=FILE_SELECTION_CHECK_4UP)
    upload_array.grid(column=1, row=0,sticky="nsew")

    #Live graph
    live_graph  = ctk.CTkButton(master=window_lower, text="Live Graph",  font=("Arial",25,"bold"), width=700, height=60,command=FILE_UPLOAD_CHECK)
    live_graph.grid(column=2, row=0,sticky="nsew")

    self.mainloop()
