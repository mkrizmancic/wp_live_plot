# wp_live_plot
Live plotting of data on WatchPlant project.

Work in progress. This repository is a template for future package.

### How to use the template
1. Put testing data in `data` folder.
1. Put definitions of ROS messages in `msg` folder. Remember to make necessary adjustments in CMakeLists.txt.
1. Put various scripts (things that are run occasionally, like preprocessing and testing) in `scripts` folder.
1. If using **Python**, put the source files in `src/wp_live_plot`.
1. If using **C++**, put the header files in `include` and source files in `src`.

### Scripts
- `csv2bag.py` - Publishes data stored in CSV files as ROS messages which can then be recorded into a ROS bag. It is also useful to show data transformation equations.
    - `rosbag record -a`
    - `rosbag play <name_of_the_file> -r 0.001` (When there is a lot of data, publishing messages at their true rate would take to long, so the script publishes at a higher rate (1 kHz). If you want to read the data at its true rate, you need to change the playback speed of the bag.)
