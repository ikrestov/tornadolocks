tornadolocks
============

Async primitives for tornado non-blocking server (as in Twisted's DefferredSemaphore)

Usage
-----

```python
from tornadolocks import Lock
lock = Lock()

#----
lock.run(callback) # For simple blocking callback/ task

#----
lock.run_async(callback) # For async task, your task should accept `callback` as first argument
```

### More advanced examples ###
```python
from tornado import gen
from tornadolocks import Lock
lock = Lock()

yield gen.Task(lock.acquire)
# Do your thingy
lock.release()
```

TESTS
=====

No proper testsuite, rather testing example:
```python
python -m tornado.testing tests
```

TODO
----

1. Code documentation
2. Readme/ examples
3. Proper tests
