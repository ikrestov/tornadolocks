#! /usr/bin/python

from tornadolocks import Lock, Semaphore
from tornado.testing import AsyncTestCase

class LockTest(AsyncTestCase):
    def test_lock(self):
        self.lock = Lock()
        #print('[] First lock')
        self.lock.acquire(lambda: self.io_loop.add_callback(self._test_lock_acquired))
        #print('[] Second lock')
        self.lock.acquire(lambda: self.io_loop.add_callback(lambda: self._test_lock_acquired(123)))
        #print('[] Third lock')
        self.lock.run(self._test_lock_acquired2)
        #print('[] Fourth lock')
        self.lock.run_async(self._test_lock_async)
        self.wait()
        self.wait()
        self.wait()
        self.wait()
        #self.assertIn(2, (2,2))

    def _test_lock_async(self, callback):
        #print('* Async lock work')
        def _cb():
            #print('* Async task CB YETY')
            callback()
            self.stop()
        self.io_loop.add_callback(_cb)
 
    def _test_lock_acquired(self, *args, **kwargs):
        #print('Releasing')
        self.io_loop.add_callback(lambda: self.lock.release())
        self.stop()

    def _test_lock_acquired2(self, *args, **kwargs):
        #print('Running')
        self.stop()

    def test_lock_ioloop(self):
        self.lock = Lock(self.io_loop)
        #print('First lock')
        self.lock.acquire(lambda: self.io_loop.add_callback(self._test_lock_release))
        #print('Second lock')
        self.lock.acquire(lambda: self.io_loop.add_callback(lambda: self._test_lock_release(123)))
        self.wait()
        self.wait()

    def _test_lock_release(self, *args, **kwargs):
        #print('Lockkkk.......')
        self.lock.release()
        self.stop()
        #print('Stopping')
