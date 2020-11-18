# RPLIDAR Script

from pyrplidar import PyRPlidar
import time
from tkinter import *
from tkinter import font as tkFont

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
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
plot_points = []

figure = plt.Figure(figsize=(30,30), dpi=100)
ax = figure.add_subplot(111, projection='polar')

"""
    DEBUG DATA GENERATION
"""
def debug_data():
    with open("message.txt", "r") as f:
        for line in f:
            pos = json.loads(line.split(" ", 1)[1].replace("'", '"').replace("False","false"))
            # print(f'{math.floor(pos["distance"])}, <{math.floor(pos["angle"])}>')
            data.append(pos)
            
    return

"""
    Sets up the lidar sensor
"""
def setup_sensor():
    # Setup LIDAR
    lidar_sensor.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)

    # Set LIDAR Motor
    lidar_sensor.set_motor_pwm(lidar_motor_speed)
    time.sleep(2)

    return


"""
    Stops the lidar sensor
"""
def stop_sensor():
    global lidar_program_running
    try:
        # Perform actions required to stop the LIDAR sensor
        lidar_sensor.stop()
        lidar_sensor.set_motor_pwm(0)

        lidar_sensor.disconnect()
        
    except Exception:
        pass
    finally:
        lidar_program_running = False

    return

def start_sensor():
    global lidar_program_running

    try:
        #Add code to resume sensor scan
        pass
    except Exception:
        pass
    finally:
        lidar_program_running = True


def collect_scan_rotation(input_scan_generator):
    # Collect the number of points that are found in one full rotation

    # Create an empty list of points
    output_points = []

    for count, scan in enumerate(input_scan_generator()):
        output_points.append(scan)

        if scan.start_flag:
            break

    return output_points

"""
    Increases lidar motor speed
"""
def increase_motor_speed():
    # INSERT Increment the motor speed of the LIDAR (Potential button handler)
    global lidar_motor_speed

    try:
        lidar_sensor.stop()

        # rpm by which the motor speed is increasing
        increment = 10

        if (lidar_motor_speed + increment) <= 500:
            lidar_motor_speed += increment

        lidar_sensor.set_motor_pwm(lidar_motor_speed)
        lidar_sensor.start_scan()
    except Exception:
        lidar_sensor.stop()

        # rpm by which the motor speed is increasing
        increment = 10

        if (lidar_motor_speed + increment) <= 500:
            lidar_motor_speed += increment

        lidar_sensor.set_motor_pwm(lidar_motor_speed)
        lidar_sensor.start_scan()
    return

"""
    Decrease lidar motor speed
"""
def decrease_motor_speed():
    # INSERT Decrement the motor speed of the LIDAR (Potential button handler)
    global lidar_motor_speed

    # rpm by which the motor speed is increasing
    decrement = 10

    if (lidar_motor_speed - decrement) >= 0:
        lidar_motor_speed -= decrement
    try:
        lidar_sensor.set_motor_pwm(lidar_motor_speed)
    except Exception:
        pass
    return


# def draw_points(input_points):
"""
    updates the points on the plot
"""
def draw_points():
    """
        TO-DO => Insert code that reads from the sensor
    """
    try:
        # code to draw points 
        # loop through the lidar values 360 at a time, set the value with a floored value of the angle as the index 
        for i in range(0, len(data)):
            data[i]["distance"] = data[i]["distance"] + 100 
            plot_points[i].remove()
            if data[i]["quality"] > 0:
                plot_points[i], = ax.plot(data[i]["angle"], data[i]["distance"], "ro")
   
        ax.figure.canvas.draw()
        ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
        ax.grid(True)
    except Exception:
        pass
    finally:
        if lidar_program_running:
            window.after(100, draw_points) # updates the plot every 10 milliseconds

"""
    This function exits the application
"""
def exit():
    try:
        stop_sensor()
    except Exception:
        pass
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
    helv36 = tkFont.Font(family='Helvetica', size=40, weight=tkFont.BOLD) # configures the font for the widgets
    window.rowconfigure(0, minsize=100, weight=1)

    window.columnconfigure(1, minsize=100, weight=1) # The main window for the application
    buttons = Frame(window)
    buttons.grid(row=0, column=0)
    start = Button(buttons, width=20, height=3, text="Start", bg="green", fg="white", font=helv36) # start scan button (TO-DO)
    start.pack()
    stop = Button(buttons, width=20, height=3, command=stop_sensor, text="Stop", fg="white", bg="black", font=helv36) # stop scan button (TO-DO)
    stop.pack()
    save = Button(buttons, width=20, height=3, text="Save", bg="blue", fg="white", font=helv36) # save button (TO-DO)
    save.pack()
    close = Button(buttons, width=20, height=3, text="Exit", command=exit, bg="red", fg="white", font=helv36) # close button
    close.pack()
    speed_label = Label(buttons, text="Speed", height=4, font=tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)) # label for speed buttons
    speed_label.pack()
    speed_buttons = Frame(buttons, width=20, height=4) # Frame for speed buttons
    speed_buttons.pack()
    decrease = Button(speed_buttons, width=8, height=4, command=decrease_motor_speed, text="-", bg="red", fg="white", font=tkFont.Font(family='Helvetica', size=45, weight=tkFont.BOLD)) # increment speed button
    decrease.grid(row=0, column=0, padx=0.3, pady=0.3)
    increase = Button(speed_buttons, width=8, height=4, command=increase_motor_speed, text="+", bg="grey", fg="white", font=tkFont.Font(family='Helvetica', size=45, weight=tkFont.BOLD)) # decrement speed button
    increase.grid(row=0, column=1, padx=0.3, pady=0.3)
     
    # frame for plot
    plot = Frame(master=window)
    plot.grid(row=0, column=1)

    # loops through the data object, plots the points, and stroes them in an array of points to streamline removal of each point
    for elem in data:
        plot_points.extend(ax.plot(elem["angle"], elem["distance"], "ro"))
    

    ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.grid(True)

    canvas = FigureCanvasTkAgg(figure, plot) # adds the plot to the GUI 
    canvas.get_tk_widget().pack()    
    return

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

    rotations = 0

    # while lidar_program_running:
    # Create an empty list of points
    # lidar_points = collect_scan_rotation(scan_generator)

    # rotations += 1

    # draw_points(lidar_points)
    draw_points()

    # if rotations >= 10:
    #     stop_program()

    # stop_sensor()

    window.mainloop()
