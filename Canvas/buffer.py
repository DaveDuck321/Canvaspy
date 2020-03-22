import ctypes


class Buffer():
    def __init__(self, item_type, row_len):
        self.__type = item_type
        self.__row_len = row_len

        self.__index = 0
        self.__capacity = 8 * self.__row_len

        self.__buffer = (self.__type*self.__capacity)()

    def push_row(self, row):
        self.__buffer[self.__index: self.__index+self.__row_len] = row
        self.__index += self.__row_len
        if self.__index == self.__capacity:
            self.resize(2 * self.__capacity)

    def resize(self, capacity):
        self.__capacity = capacity
        self.__buffer = (self.__type*capacity)(*self.__buffer)

    def get_buffer(self):
        return (self.__index*ctypes.sizeof(self.__type), self.__buffer)

    def row_count(self):
        return self.__index//self.__row_len

    def clear(self):
        self.__index = 0


"""Numpy slow
import numpy as np

class BufferList():
    def __init__(self, item_type, row_len):
        self.__row_len = row_len

        self.__capacity = 8*row_len
        self.__index = 0

        self.__buffer = np.empty(self.__capacity, dtype=np.float32)

    def push_row(self, row):
        self.__buffer[self.__index:self.__index+self.__row_len] = row
        self.__index += self.__row_len
        if self.__index == self.__capacity:
            self.resize(self.__capacity * 2)

    def resize(self, capacity):
        new_buffer = np.empty(capacity, dtype=np.float32)
        new_buffer[:self.__capacity] = self.__buffer
        self.__capacity = capacity
        self.__buffer = new_buffer

    def get_buffer(self):
        return (self.__index*ctypes.sizeof(ctypes.c_float), self.__buffer)

    def clear(self):
        self.__index = 0

    def row_count(self):
        return self.__index//self.__row_len
"""
