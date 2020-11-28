# ee437_LIDAR_Project
Group Project for EE 437

The goal of this application is to develop a GUI application to display data from a LIDAR sensor. The library used to achieve this is the [adafruit_rplidar](https://circuitpython.readthedocs.io/projects/rplidar/en/latest/api.html#module-adafruit_rplidar) which leverages the LIDAR binaries and serial connection.
The program also needs to export data to data to different format which will be implemented in a latter release.

To setup the environment, activate the virtual environment by running 

```source ./RPi_lidar/bin/activate```

Then, run ```sudo ./setup.sh``` to install numpy raspberrypi dependencies

After that, connect the LIDAR sensor, then run ```python main.py``` to start the program.

