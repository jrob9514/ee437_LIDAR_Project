# RPLIDAR Script

from pyrplidar import PyRPlidar
import time

"""Global Variables"""
# Boolean to control whether the program loop is running
lidar_program_running = True

# Lidar sensor being controlled by the program
lidar_sensor = PyRPlidar()

# LIDAR motor speed
lidar_motor_speed = 10


def setup_sensor():
    # Setup LIDAR
    lidar_sensor.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)

    # Set LIDAR Motor
    lidar_sensor.set_motor_pwm(lidar_motor_speed)
    time.sleep(2)

    return


def setup_gui():
    # INSERT Setup elements of GUI

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
    setup_sensor()

    # Call setup code for GUI
    setup_gui()

    # Create scan generator to grab LIDAR scan data
    scan_generator = lidar_sensor.force_scan()

    rotations = 0

    while lidar_program_running:
        # Create an empty list of points
        lidar_points = collect_scan_rotation(scan_generator)

        rotations += 1

        draw_points(lidar_points)

        if rotations >= 10:
            stop_program()

    stop_sensor()
