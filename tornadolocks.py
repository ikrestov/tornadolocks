#! /usr/bin/python

__author__="Igor Krestov"
__date__ ="$04-Jul-2012 16:08:49$"

from threading import Lock as TLock, BoundedSemaphore as TBoundedSemaphore
from tornado import gen
from Queue import Queue, Empty

class Lock(object):
    def __init__(self, io_loop=None):
        self._lock = TLock()
        self._queue = Queue()
        self.io_loop = io_loop
        
    @gen.engine
    def run(self, callback, *args, **kwargs):
        yield gen.Task(self.acquire)
        callback(*args, **kwargs)
        self.release()
    
    @gen.engine
    def run_async(self, callback, *args, **kwargs):
        yield gen.Task(self.acquire)
        yield gen.Task(callback, *args, **kwargs)
        self.release()
    
    def acquire(self, callback, *args, **kwargs):
        if self._lock.acquire(False):
            callback(*args, **kwargs)
        else:
            self._queue.put_nowait((callback, args, kwargs))
            
    def release(self):
        self._lock.release()
        try:
            callback, args, kwargs = self._queue.get_nowait()
            if self.io_loop:
                self.io_loop.add_callback(lambda: self.acquire(callback, *args, **kwargs))
            else:
                self.acquire(callback, *args, **kwargs)
        except Empty:
            pass

class Semaphore(object):
    def __init__(self, value=1, io_loop=None):
        self._lock = TBoundedSemaphore(value)
        self._queue = Queue()
        self.io_loop = io_loop
