# traffic_counter

PROBLEM WITH MOTORCYCLES CURRENTLY :(

This program is a traffic counter. It counts objects that cross the line_point specified in the main.py.

All parameters that need to be specified by the user are at the top of the main.py file (below the imports).

They are currently:

video_source (The source input, f.e. live webcams or videos)
output_dir (if an Object was tracked, the frame when it crosses the specified line is saved)
line_point (said line that you need to specify, were the objects are counted based on crossing the line)
classes_to_track (here you can specify the classes you wanna track based on the classes in YOLOv8)

The classes are tracked class wise and combined.
