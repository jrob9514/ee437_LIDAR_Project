# RPLIDAR Script

from adafruit_rplidar import RPLidar
from math import pi, floor
import datetime
from queue import Queue
from tkinter import messagebox
import time
from tkinter import *
from tkinter import font as tkFont

import threading
import subprocess

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import os

"""Global Variables"""

# Default port for USB devices
PORT_NAME = '/dev/ttyUSB0'
# Global variable for LIDAR sensor
lidar = RPLidar(None, PORT_NAME)
# Data queue used for passing data from the scan thread to the GUI thread
data_queue = Queue(maxsize=10)

# GUI Global variables
lidar_program_running = True
window = Tk()
figure = plt.Figure(figsize=(30, 30), dpi=100)
ax = figure.add_subplot(111, projection='polar')
export = False
save_menu = ""

def scan():
    # Function for generating lidar scan data

    global lidar_program_running

    # Create array of scan data
    scan_data = [0]*360

    try:
        # Iterate through the scans produced by the LIDAR
        for single_scan in lidar.iter_scans():
            for (_, angle, distance) in single_scan:
                scan_data[min([359, floor(angle)])] = distance

            if not data_queue.full():
                data_queue.put(scan_data)

    except Exception as e:
        print("scan error: ", e)

    finally:
        lidar_program_running = False


"""
    Stops the lidar sensor
"""


def stop_sensor():
    # Function for stopping the LIDAR scanner gracefully
    try:
        print("Stopping LIDAR")
        lidar.stop()

        time.sleep(2)

        print("Disconnecting LIDAR")
        lidar.disconnect()

    except Exception as e:
        print("stop_sensor error: ", e)

    return


def draw_points():
    # Function for updating the GUI canvas
    global export
    data_export = []
    try:
        # Grab the first data point in the queue
        scan_points = data_queue.get()
        
        if scan_points:
            # Clear the polar plot
            ax.clear()
            # Loop through the list of data points
            for angle in range(360):
                # Assign a distance for each angle
                distance = scan_points[angle]
                # Convert angle from degrees to radians
                radians = angle * pi / 180.0
                if export:
                    data_export.append([angle, distance])
                # Plot the data points on the polar graph
                ax.plot(radians, distance, "ro", alpha=1)
            if export:
                export = False
                show_save_menu(data_export)
                
        # Draw the figure
        ax.figure.canvas.draw()

    except Exception as e:
        # FOR DEBUG ---
        # if export:
        #     export = False
        #     for i in range(0,20):
        #         data_export.append([i, "test"])
        #     show_save_menu(data_export)
        print("draw_points error: ", e)
    finally:
        if lidar_program_running:
            window.after(100, draw_points)


def exit():
    try:
        stop_sensor()
    except Exception as e:
        print("exit error: ", e)
    finally:
        time.sleep(1)
        window.quit()

def save_data(val: list, loc: str):
    global save_menu

    filename = f'/home/pi/{loc}/export_{datetime.datetime.now().strftime("%d-%m-%Y_%I:%M_%s")}.csv'
    
    export_file = open(filename, "w")
    export_file.write(f'Angle,Distance \n')
    # Loop through the list of data points
    for elem in val:
        export_file.write(f'{elem[0]}, {elem[1]} \n')
    messagebox.showinfo("Success","Data exported to " + filename, parent=save_menu)
    save_menu.destroy()
    return

def show_save_menu(val):
    global save_menu

    
    print("exporting")
    helv36 = tkFont.Font(family='Helvetica', size=40, weight=tkFont.BOLD)  # configures the font for the widgets

    disks = subprocess.check_output("cd ~ && ls -d */", shell=True).decode("utf8").replace("/","").split("\n")[0:-1] # uses this command to get the disk names and stores them in a list
    
    save_menu = Toplevel(window)
    popup = Frame(save_menu)
    popup.place(relx = 0.5,  
                   rely = 0.5, 
                   anchor = 'center') 
    save_menu.geometry(f'{window.winfo_screenwidth()}x{window.winfo_screenheight()}')  # Size of the window 
    save_menu.title("Export to:")
    my_str1 = StringVar()
    l1 = Label(popup,  textvariable=my_str1, width=20, font=tkFont.Font(family='Helvetica', size=30, weight=tkFont.BOLD) )
    l1.grid(row=1, column=1)
    my_str1.set("Save to:")

    # listbox with disk names
    items = Listbox(popup, width=30, height=15, font=tkFont.Font(family='Helvetica', size=30, weight=tkFont.BOLD))
    ct = 0
    for disk in disks:
        items.insert(ct, disk)
        ct+=1

    items.grid(row=2, column=1)
    save_button = Button(popup, width=20, height=3, text="Save", command=lambda: save_data(val=val, loc=disks[items.curselection()[0]]), bg="red", fg="white",
                   font=helv36)
    save_button.grid(row=3, column=1)
    

def start_export():
    global export
    export = True

def setup_gui():
    # This function setps up the GUI

    # Set window title
    window.title("Lidar Applicataion")
    # Set window to fill entire screen
    window.geometry(f'{window.winfo_screenwidth()}x{window.winfo_screenheight()}')
    helv36 = tkFont.Font(family='Helvetica', size=40, weight=tkFont.BOLD)  # configures the font for the widgets
    window.rowconfigure(0, minsize=100, weight=1)

    window.columnconfigure(1, minsize=100, weight=1)  # The main window for the application
    buttons = Frame(window)
    buttons.grid(row=0, column=0)

    start = Button(buttons, width=20, height=3, text="Start", command=draw_points, bg="green", fg="white",
                   font=helv36)  # start scan button (TO-DO)
    start.pack()

    stop = Button(buttons, width=20, height=3, command=stop_sensor, text="Stop", fg="white", bg="black",
                  font=helv36)  # stop scan button (TO-DO)
    stop.pack()

    save = Button(buttons, width=20, height=3, command=start_export, text="Save", bg="blue", fg="white", font=helv36)  # save button (TO-DO)
    save.pack()

    close = Button(buttons, width=20, height=3, text="Exit", command=exit, bg="red", fg="white",
                   font=helv36)  # close button
    close.pack()

    # frame for plot
    plot = Frame(master=window)
    plot.grid(row=0, column=1)

    ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.grid(True)

    canvas = FigureCanvasTkAgg(figure, plot)  # adds the plot to the GUI
    canvas.get_tk_widget().pack()
    return


if __name__ == "__main__":
    # Program entry point

    # Print Lidar Information
    print(lidar.info)

    # Call setup code for GUI
    setup_gui()

    # Create thread for running scanner
    scan_thread = threading.Thread(target=scan)

    # Set scan thread to terminate itself after program is complete
    scan_thread.setDaemon(True)

    # Start the scanning thread
    scan_thread.start()

    # Call the GUI loop
    window.mainloop()

