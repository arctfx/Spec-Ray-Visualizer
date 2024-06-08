import time
import sys
import win32pipe, win32file, pywintypes
import io
import multiprocessing as mp
from multiprocessing import shared_memory
import re
import numpy as np


# Defining image width and height
img_w, img_h = 1200, 700


class Client:
    def __init__(self):
        self.img_h = img_h
        self.img_w = img_w
        # Creating a NumPy array 'arr' filled with zeros of shape (img_h, img_w, 3) representing RGB channels
        arr = np.zeros((img_h, img_w, 3), dtype=np.uint8)
        self.data_shm = shared_memory.SharedMemory(create=True, size=arr.nbytes, name='data')
        self.data = np.ndarray((img_h, img_w, 3), dtype=np.uint8, buffer=self.data_shm.buf)  # image data

    @staticmethod
    def pipe_client():
        # global data
        data_shm = shared_memory.SharedMemory(name='data')
        data = np.ndarray((img_h, img_w, 3), dtype=np.uint8, buffer=data_shm.buf)
        print("pipe client")
        terminate = False

        while not terminate:
            try:
                handle = win32file.CreateFile(r'\\.\pipe\specray', win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0,
                                              None, win32file.OPEN_EXISTING, 0, None)
                # res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, 2, 2)
                # if res == 0:
                #     print(f"SetNamedPipeHandleState return code: {res}")
                # data = pack[0]
                # data2 = pack[1]
                while True:
                    result, dt = win32file.ReadFile(handle, 64*1024)
                    pixel = re.findall(r"-?\d+(?:\.\d+)?", f"{dt}")

                    if pixel[0] == pixel[1] == '-1':
                        print(f"{pixel[0]} {pixel[1]}")
                        break
                    # print(f"{dt}")
                    print(f"{pixel[0]} {pixel[1]}")

                    # Note: image coordinates in tkinter start from top left,
                    # while in our raytracer coordinates start from bottom left;
                    # data[height-y][x]
                    data[img_h-int(pixel[1])-1][int(pixel[0])] = [int(pixel[2]), int(pixel[3]), int(pixel[4])]
                    # data[val // img_h, val % img_w] = pixels[val]

                    r, g, b = data[img_h-int(pixel[1])-1][int(pixel[0])]
                    # print(result)
                    print(f"message: {r} {g} {b}")
                    # win32file.WriteFile(handle, b"HELLO\n", None)
            except pywintypes.error as e:
                if e.args[0] == 2:
                    io.StringIO().seek(0)
                    io.StringIO().truncate(0)
                    # print("no pipe, trying again in a sec")

    def start(self):
        # self.pipe_client()
        mp.set_start_method('spawn')
        q = mp.Queue()
        p = mp.Process(target=self.pipe_client, args=())
        p.start()
        print('print')
        # print(q.get())
        # p.join()
