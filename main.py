# RPLIDAR Script

from pyrplidar import PyRPlidar
import time

"""Global Variables"""
# Boolean to control whether the program loop is running
lidar_program_running = True

# Lidar sensor being controlled by the program
lidar_sensor = PyRPlidar()

# LIDAR motor speed
lidar_motor_speed = 250


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
    global lidar_program_running

    lidar_program_running = False


def draw_points(input_points):
    for point in input_points:
        print(point)


if __name__ == "__main__":
    global lidar_program_running
    global lidar_sensor
    global lidar_motor_speed

    # Setup LIDAR
    lidar_sensor.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)

    # Set LIDAR Motor
    lidar_sensor.set_motor_pwm(250)
    time.sleep(2)

    # Create scan generator to grab LIDAR scan data
    scan_generator = lidar_sensor.force_scan()

    rotations = 0

    while lidar_program_running:
        # Create an empty list of points
        lidar_points = collect_scan_rotation(scan_generator)

        rotations += 1

        draw_points(lidar_points)

        if rotations >= 10:
            lidar_program_running = False

    lidar_sensor.stop()
    lidar_sensor.set_motor_pwm(0)

    lidar_sensor.disconnect()
