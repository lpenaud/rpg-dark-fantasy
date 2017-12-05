#!/usr/bin/env python3
# coding: utf-8
import threading

class ThreadJob(threading.Thread):
    """
    Runs the callback function after interval seconds x times

    :param callback:  callback function to invoke
    :type callback: function
    :param interval: time in seconds after which are required to fire the callback
    :type interval: float
    :param time: number of times callback is invoke
    :type time: int
    """

    def __init__(self,callback,interval,times):
        self.callback = callback
        self.event = threading.Event()
        self.interval = interval
        self.times = times
        self.currentTimes = 0
        super(ThreadJob,self).__init__()

    def run(self):
        while not(self.event.wait(self.interval)) and self.currentTimes != self.times:
            self.callback()
            self.currentTimes += 1
