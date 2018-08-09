'''
Copyright 2018 Yi-Fan Shyu. Some rights reserved.
CC BY-NC-SA
'''
import os, threading, Queue

rd_path, wr_path = "\\\\.\\pipe\\pokerbridge_wr", "\\\\.\\pipe\\pokerbridge_rd"
inbuf = Queue.Queue()
outbuf = Queue.Queue()

rd = os.open(rd_path, os.O_RDONLY)
wr = os.open(wr_path, os.O_WRONLY)

def readfunc(inbuf, rd):
    while True:
        if inbuf.qsize() < 10:
            inbuf.put(os.read(rd, 50))
    
def writefunc(outbuf, wr):
    while True:
        try:
            mess = outbuf.get()
            os.write(wr, mess)
        except Queue.Empty:
            pass
        
def connect():
    thr_rd = threading.Thread(target = readfunc, args = (inbuf, rd))
    thr_rd.daemon = True
    thr_rd.start()
    thr_wr = threading.Thread(target = writefunc, args = (outbuf, wr))
    thr_wr.daemon = True
    thr_wr.start()

def read():
    while True:
        try:
            mess = inbuf.get(False)
            return mess
        except Queue.Empty:
            continue

def write(mess):
    if mess != "":
        outbuf.put(mess)



