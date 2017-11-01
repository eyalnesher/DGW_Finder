#!/usr/bin/python

from Tkinter import *
from multiprocessing import Process
import active_DGW_determinate as dgw
from time import time


def time_parsing(inp_time):
    """
    Turning time from time units format to seconds
    :param inp_time: The time in time units format
    :type inp_time: str
    :return: The time in seconds
    :rtype: Union[float, int]
    """
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


def start():
    """
    Calling to the actual code.
    :return: None
    :rtype: None
    """
    dgw.main()


def starting_process():
    """
    The actions that happen when the start button is clicked
    :return: None
    :rtype: None
    """
    global time_entry
    global log

    # Clear the log
    clear_log = open("result.log", "w")
    clear_log.close()
    try:
        log.delete(0, END)
    except:
        pass

    running_time = time_parsing(time_entry.get())   # The running time

    pstart = Process(target=start)

    starting_time = time()   # The starting time
    pstart.start()

    # Time checking
    while True:
        current_time = time()
        if (current_time - starting_time > running_time) or (len(open("result.log", "r").read().split("\n")) > 1):
            pstart.terminate()
            break
        elif not pstart.is_alive():
            break

    result = open("result.log", "r").read()

    # Detales checking
    if len(result) == 0:
        open("result.log", "w").write("The Default Gateway could not be found")
    elif len(result.split("\n")) == 1:
        open("result.log", "w").write(result + "The IP address of the Default Gateway could not be found")

    updated_result = open("result.log", "r").read()

    log.insert(INSERT, updated_result)


def main():
    """
    The GUI of the DGW finder.
    :return: None
    :rtype: None
    """
    global log

    root = Tk()

    # The entry of the running time
    time_frame = Frame(root)
    time_frame.pack(side=TOP)

    time_label = Label(time_frame, text="The program duration time:")
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
