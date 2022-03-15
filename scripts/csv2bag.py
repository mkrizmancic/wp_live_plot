import argparse
import math
import pathlib
import datetime

import rospy

from wp_live_plot.msg import SensorData


def parse_data(line):
    # Read and format the data.
    data = line.split(',')
    rospy.logdebug(" \n%s", data)

    msg = SensorData()
    msg.header.stamp = rospy.Time.from_sec(datetime.datetime.strptime(data[0], '%Y-%m-%d %H:%M:%S').timestamp())
    # PCB temperature
    msg.pcb_temp = int(data[1]) / 10000  # Degrees Celsius
    # Magnetic fields
    msg.mag.x = int(data[2]) / 1000 * 100  # Micro Tesla
    msg.mag.y = int(data[3]) / 1000 * 100  # Micro Tesla
    msg.mag.z = int(data[4]) / 1000 * 100  # Micro Tesla
    msg.mag_total = math.sqrt(msg.mag.x ** 2 + msg.mag.y ** 2 + msg.mag.z ** 2)
    # Air conditions
    msg.air_temp = int(data[5]) / 10000  # Degrees Celsius
    msg.air_hum = (int(data[7]) * 3 / 4200000 - 0.1515) / (0.006707256 - 0.0000137376 * msg.air_temp)  # Percent
    msg.air_press = int(data[12]) / 100  # Millibars
    # Other external conditions
    msg.light = int(data[6]) / 799.4 - 0.75056  # Lux
    msg.rf_power = int(data[10])  # UNKNOWN
    # Differential potentials
    msg.diff_pot_CH1 = int(data[8]) - 512000  # Micro Volts
    msg.diff_pot_CH2 = int(data[9]) - 512000  # Micro Volts
    # Plant conditions
    msg.transpiration = int(data[11]) / 1000  # Percent
    # Soil conditions
    msg.soil_moist = int(data[13])  # UNKNOWN
    msg.soil_temp = int(data[14]) / 10  # Degrees Celsius

    return msg


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", type=str, default="../data/FER_4plants_office_noexternal_Jun25_Jul01",
                        help="relative path to the directory containing data")
    parser.add_argument("-e", "--extension", type=str, default="csv", help="extension of the files to read from")
    args = parser.parse_args()

    # Set up directories we'll be using.
    src_dir = pathlib.Path.cwd()  # Current directory from where the script was started.
    data_dir = src_dir / args.dir  # Directory with source csv files.
    file_extension = args.extension.strip('.')

    # Get available file names.
    file_handles = {filename.stem: open(filename, 'r') for filename in data_dir.glob(f"*.{file_extension}")}
    print(file_handles)

    # Set up ROS publisher.
    pubs = {name: rospy.Publisher(f'/{name}', SensorData, queue_size=1) for name in file_handles}

    # Skip first lines in files.
    for name, file in file_handles.items():
        next(file, None)

    # Read files line by line and publish data.
    line = None
    while True:
        for name, file in file_handles.items():
            line = next(file, None)
            if line is not None:
                msg = parse_data(line)
                pubs[name].publish(msg)
                rospy.sleep(0.001)
            else:
                file.close()
        if line is None:
            break


if __name__ == '__main__':
    rospy.init_node('csv_publisher')

    try:
        main()
    except rospy.ROSInterruptException:
        pass
    else:
        print("DONE")
