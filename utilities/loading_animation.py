import sys
import threading
import time

def loading_animation(loading_complete):
    animation = "|/-\\"
    idx = 0
    while not loading_complete.is_set():
        sys.stdout.write("\rFETCHING DATA " + animation[idx % len(animation)])
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1

