#!/usr/bin/env python3
"""Child process in signal example.
"""
#end_pymotw_header

import os
import signal
import time
import sys

pid = os.getpid()
received = False


def signal_usr1(signum, frame):
    "Callback invoked when a signal is received"
    global received
    received = True
    print('CHILD %6s: Received USR1' % pid)
    sys.stdout.flush()


print('CHILD %6s: Setting up signal handler' % pid)
sys.stdout.flush()
signal.signal(signal.SIGUSR1, signal_usr1)
print('CHILD %6s: Pausing to wait for signal' % pid)
sys.stdout.flush()
time.sleep(3)

if not received:
    print('CHILD %6s: Never received signal' % pid)
