# pyPerfMeter
This is a python based CPU/RAM usage display

## FYI
This program has a "light memory leak".\
The memory usage might go up to ~500MB(Win10).\
Thanks matplotlib for saving previous frames of an animation 👍.


## Dependencies
* python3 (python3.7 tested)
* tkinter
* psutil
* matplotlib

## Questions that might arise
##### Q: How high is the resource usage?
A: It uses:\
1core at ~1GHz\
50MB at the beginning

##### Q: Why?
A: To improve my programming abilities.
##### Q: Why does the window stutter, when I move it?
A: tkinter uses a event based loop, as such, whenever you are computing something, or waiting for something it cannot update the window. This this does not happen in Linux.
