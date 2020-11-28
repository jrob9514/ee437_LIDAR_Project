# RPLIDAR Script

from adafruit_rplidar import RPLidar
from math import pi, floor

from queue import Queue

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
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

scan_data = [0] * 360

data_queue = Queue()

lidar_program_running = True

window = Tk()

data = []
plot_points = []

figure = plt.Figure(figsize=(30, 30), dpi=100)
ax = figure.add_subplot(111, projection='polar')

"""
    Sets up the lidar sensor
"""


def scan(in_q):
    global scan_data

    try:
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                scan_data[min([359, floor(angle)])] = distance

            in_q.put(scan_data)
    except Exception as e:
        print("scan error: ", e)


"""
    Stops the lidar sensor
"""


def stop_sensor():
    global lidar_program_running
    try:
        print("Stopping LIDAR")
        lidar.stop()
        print("Disconnecting LIDAR")
        lidar.disconnect()

    except Exception as e:
        print("stop_sensor error: ", e)
    finally:
        lidar_program_running = False

    return


def draw_points():
    # Function for updating the GUI canvas

    try:
        scan_points = data_queue.get()

        if scan_points:
            ax.clear()

            for angle in range(360):
                distance = scan_data[angle]
                radians = angle * pi / 180.0

                ax.plot(radians, distance, "ro", alpha=1)

        ax.figure.canvas.draw()
        ax.grid(True)

    except Exception as e:
        print("draw_points error: ", e)

    finally:
        if lidar_program_running:
            window.after(100, draw_points)


"""
    This function exits the application
"""


def exit():
    try:
        stop_sensor()
    except Exception as e:
        print("exit error: ", e)
    finally:
        time.sleep(1)
        window.quit()


"""
    This function is used to setup the GUI
"""


def setup_gui():
    # INSERT Setup elements of GUI
    window.title("Lidar Applicataion")
    # window.attributes("-fullscreen", True) # sets the application to full screen
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
    save = Button(buttons, width=20, height=3, text="Save", bg="blue", fg="white", font=helv36)  # save button (TO-DO)
    save.pack()
    close = Button(buttons, width=20, height=3, text="Exit", command=exit, bg="red", fg="white",
                   font=helv36)  # close button
    close.pack()

    # frame for plot
    plot = Frame(master=window)
    plot.grid(row=0, column=1)

    # loops through the data object, plots the points, and stroes them in an array of points to streamline removal of each point
    # for elem in data:
    #   plot_points.extend(ax.plot(elem["angle"], elem["distance"], "ro"))

    # ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.grid(True)

    canvas = FigureCanvasTkAgg(figure, plot)  # adds the plot to the GUI
    canvas.get_tk_widget().pack()
    return


if __name__ == "__main__":
    # Print Lidar Information
    print(lidar.info)

    # Call setup code for GUI
    setup_gui()

    scan_thread = threading.Thread(target=scan, args=(data_queue,))

    # Set scan thread to terminate itself after program is complete
    scan_thread.setDaemon(True)

    # Start the scanning thread
    scan_thread.start()

    # Call the GUI loop
    window.mainloop()

