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

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

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

    try:
        # Grab the first data point in the queue
        scan_points = data_queue.get()

        if scan_points:
            # Clear the polar plot
            ax.clear()
            if export:
                filename = "export" + datetime.datetime.now() + ".csv"
                export_file = open(filename, "w")
            # Loop through the list of data points
            for angle in range(360):
                # Assign a distance for each angle
                distance = scan_points[angle]
                # Convert angle from degrees to radians
                radians = angle * pi / 180.0
                if export:
                    export_file.writeline(f'{distance}, {angle}')
                # Plot the data points on the polar graph
                ax.plot(radians, distance, "ro", alpha=1)
            if export:
                messagebox.showinfo("Success","Data exported to " + filename)
                export = False
        # Draw the figure
        ax.figure.canvas.draw()

    except Exception as e:
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

def save_data():
    global export
    export = not export
    return




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

    save = Button(buttons, width=20, height=3, command=save_data, text="Save", bg="blue", fg="white", font=helv36)  # save button (TO-DO)
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

    Call the GUI loop
    window.mainloop()

