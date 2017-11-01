#!/usr/bin/python

from Tkinter import *
from multiprocessing import Process
import active_DGW_determinate as dgw
import sys
from scapy.all import *


def time_parsing(inp_time):
    if inp_time == "":
        return float("inf")
    time_units = inp_time.split(":")
    if len(time_units) < 3:
        time_in_seconds = 0
        for unit, t in enumerate(time_units[::-1]):
            time_in_seconds += float(t) * (60 ** unit)
        return time_in_seconds
    else:
        raise ValueError("Must be at most 3 time units ({} given)".format(len(time_units)))


def start(run_time):
    """
    The actions that happend when the start button is clicked
    :return:
    """
    
    running_time = time_parsing(run_time)
    print "starting sniffing"
    dgw.main(running_time)


def starting_process():
    global time_entry
    global log

    pstart = Process(target=start, args=(time_entry.get(),))
    pstart.start()
    result = open("result.log", "r").read()
    log.insert(INSERT, result)


def main():
    """

    :return:
    """
    global log

    root = Tk()

    # The entry of the running time
    time_frame = Frame(root)
    time_frame.pack(side=TOP)

    time_label = Label(time_frame, text="time for program to run for:")
    time_label.pack(side=LEFT)

    global time_entry
    time_entry = Entry(time_frame, width=3)
    time_entry.pack(side=LEFT)

    # The log
    log = Text(root, height=4)
    log.pack(side=BOTTOM)

    # The start button
    start_button = Button(root, command=starting_process, text="start")
    start_button.pack(side=BOTTOM)

    root.mainloop()

if __name__ == '__main__':
    main()
