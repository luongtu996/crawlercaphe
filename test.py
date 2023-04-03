import re
import CrUtil

import threading


def my_func():
    print("Hello, world!")


# Create a Timer object that will call my_func after 5 seconds
t = threading.Timer(5.0, my_func)

# Start the timer
t.start()

# Wait for the timer to complete or to be cancelled
t.join()

# If the timer did not complete in 5 seconds, cancel it
if t.is_alive():
    print("Timeout!")
    t.cancel()
