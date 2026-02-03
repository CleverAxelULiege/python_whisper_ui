import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

x = threading.Thread(target=thread_function, daemon=True, args=(1,))
x.start()

print("finished")