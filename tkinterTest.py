from threading import Thread
from Tkinter import *
import random
import time

import Queue

q = Queue.Queue()
root = Tk()
canvas = Canvas(root, width=500, height=500)
canvas.pack()

def spin(i):
    time.sleep(random.randint(3,10))
    print "hello?"
    q.put("hello world %d" % i)

def update():
    ret = None
    try:
        ret = q.get_nowait()
    except:
        pass
    canvas.create_rectangle(0,0,random.randint(10, 50),50)
    canvas.create_text(50, random.randint(100, 300), text=ret)
    root.after(100, update)

def main():

    for i in range(10):
        Thread(target=spin, args=(i,)).start()

    root.after(100, update)
    root.mainloop()

main()
