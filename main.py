# RPLIDAR Script

from pyrplidar import PyRPlidar
import time
from tkinter import *

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import json, math


"""Global Variables"""
# Boolean to control whether the program loop is running
lidar_program_running = True

# Lidar sensor being controlled by the program
lidar_sensor = PyRPlidar()

# LIDAR motor speed
lidar_motor_speed = 10

window = Tk()

data = []

def debug_data():
    with open("message.txt", "r") as f:
        for line in f:
            pos = json.loads(line.split(" ", 1)[1].replace("'", '"').replace("False","false"))
            print(f'{math.floor(pos["distance"])}, <{math.floor(pos["angle"])}>')
            data.append(pos)
            
    return


def setup_sensor():
    # Setup LIDAR
    lidar_sensor.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)

    # Set LIDAR Motor
    lidar_sensor.set_motor_pwm(lidar_motor_speed)
    time.sleep(2)

    return


def setup_gui():
    # INSERT Setup elements of GUI
    window.title("Lidar Applicataion")

    window.rowconfigure(0, minsize=100, weight=1)

    window.columnconfigure(1, minsize=100, weight=1)
    buttons = Frame(window)
    buttons.grid(row=0, column=0)
    start = Button(buttons, text="Start")
    start.pack()
    stop = Button(buttons, text="Stop")
    stop.pack()
    save = Button(buttons, text="Save")
    save.pack()

    plot = Frame(master=window)
    plot.grid(row=0, column=1)



    r = np.arange(0, 2, 0.01)
    theta = 2 * np.pi * r
    figure = plt.Figure(figsize=(5,4), dpi=100)
    ax = figure.add_subplot(111, projection='polar')
    ax.plot(theta, r)
    ax.set_rmax(2)
    ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
    ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.grid(True)

    # ax.set_title("A line plot on a polar axis", va='bottom')
    # plt.show()

    canvas = FigureCanvasTkAgg(figure, plot)
    canvas.get_tk_widget().pack()    

    # lbl = Label(window, text="hello")
    # lbl.pack()
    # buttons.pack()
    # window.geometry("300x200")
    return


def stop_sensor():
    # Perform actions required to stop the LIDAR sensor
    lidar_sensor.stop()
    lidar_sensor.set_motor_pwm(0)

    lidar_sensor.disconnect()

    return


def stop_gui():
    # INSERT code to stop the GUI gracefully
    
    return


def collect_scan_rotation(input_scan_generator):
    # Collect the number of points that are found in one full rotation

    # Create an empty list of points
    output_points = []

    for count, scan in enumerate(input_scan_generator()):
        output_points.append(scan)

        if scan.start_flag:
            break

    return output_points


def stop_program():
    # INSERT Potential Stop button handler
    global lidar_program_running
    lidar_program_running = False


def increase_motor_speed():
    # INSERT Increment the motor speed of the LIDAR (Potential button handler)
    global lidar_motor_speed

    lidar_sensor.stop()

    # rpm by which the motor speed is increasing
    increment = 10

    if (lidar_motor_speed + increment) <= 500:
        lidar_motor_speed += increment

    lidar_sensor.set_motor_pwm(lidar_motor_speed)

    lidar_sensor.start_scan()

    return


def decrease_motor_speed():
    # INSERT Decrement the motor speed of the LIDAR (Potential button handler)
    global lidar_motor_speed

    # rpm by which the motor speed is increasing
    decrement = 10

    if (lidar_motor_speed - decrement) >= 0:
        lidar_motor_speed -= decrement

    lidar_sensor.set_motor_pwm(lidar_motor_speed)

    return


def draw_points(input_points):
    # INSERT updates points drawn on GUI
    for point in input_points:
        print(point)


if __name__ == "__main__":
    # global lidar_program_running
    # global lidar_sensor
    # global lidar_motor_speed

    # Call setup code for sensor
    # setup_sensor()

    # # Call setup code for GUI
    debug_data()
    setup_gui()

    # # Create scan generator to grab LIDAR scan data
    # scan_generator = lidar_sensor.force_scan()

    # rotations = 0

    # while lidar_program_running:
    #     # Create an empty list of points
    #     lidar_points = collect_scan_rotation(scan_generator)

    #     rotations += 1

    #     draw_points(lidar_points)

    #     if rotations >= 10:
    #         stop_program()

    # stop_sensor()

    window.mainloop()
