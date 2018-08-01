#!/usr/bin/python3
import psutil
import tkinter as tk
import gc

import matplotlib
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg

length = 60  # in s
update_freq = 1000  # in ms
list_len = int(length / (update_freq/1000))
loops = 0  # used to forcefully trigger the gc
LARGE_FONT = ("Verdana", 12)
style.use("ggplot")
f = Figure(figsize=(5, 5), dpi=100)
subplot = f.add_subplot(111)

# preparing lists
frameY = [0, 0, 100]
frameX = [length, 0, 0]
memyList = []
cpuyList = []
xList = []


class Lists:
    def re_set(self):
        for i in range(list_len + 1):
            memyList.append(None)
            cpuyList.append(None)
            xList.append(i * (length / list_len))

    def update(self):
        memyList.append(psutil.virtual_memory().percent)
        memyList.pop(0)
        cpuyList.append(psutil.cpu_percent(update_freq/1000/2))
        cpuyList.pop(0)


# Actually drawing stuff
def animate(for_some_reason_it_wants_a_variable):
    global loops
    Lists.update(Lists)
    subplot.clear()
    if loops >= list_len:
        loops = 1
        gc.collect()
    else:
        loops += 1
    subplot.plot(xList, cpuyList, label="cpu " + str(cpuyList[len(cpuyList) - 1]) + "%")
    used_memory = round(psutil.virtual_memory().used / 1024 / 1024 / 1024, 3)      # conversion
    used_memory = "{:,}".format(used_memory) + "GB"  # formatting
    subplot.plot(xList, memyList, label=("memory " + used_memory))
    subplot.plot(frameX, frameY)
    subplot.legend(loc=9, framealpha=0)
    subplot.set_xlabel("time in s (approximately)")
    subplot.set_ylabel("percentage used")


# tkinter gui
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.wm_title(self, "Hallo")

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # toolbar for modifying/saving the plot
        # toolbar = NavigationToolbar2TkAgg(canvas, self)
        # toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


Lists.re_set(Lists)
app = App()
ani = animation.FuncAnimation(f, animate, interval=update_freq / 2)
app.mainloop()
