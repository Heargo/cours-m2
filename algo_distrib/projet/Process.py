from threading import Thread

from time import sleep

# from geeteventbus.subscriber import subscriber
# from geeteventbus.eventbus import eventbus
# from geeteventbus.event import event

# from EventBus import EventBus
from Com import Com

from pyeventbus3.pyeventbus3 import *


class Process(Thread):

    def __init__(self, name, nbProcess):
        Thread.__init__(self)

        self.setName(name)
        self.nbProcess = nbProcess
        self.alive = True
        self.dead = False

        self.com = Com(nbProcess)
        self.myId = None
        self.start()

    def log(self, msg):

        print(
            f"PRO<{self.myId}> [{'LIVE' if self.alive else 'ZOMB' if not self.dead else 'DEAD'}] {msg}", flush=True)

    #############################
    ######      RUN       #######
    #############################

    def stop(self):
        self.alive = False
        self.synchronizingProcesses = []
        self.log(f"Let's STOP")
        self.com.stop()
        self.join()
        self.log("TERMINATED")

    def run(self):
        loop = 0
        self.myId = self.com.getId()
        while self.alive:
            self.log(f"Loop: {loop}")
            sleep(1)

            if (self.myId == self.nbProcess-1 and loop == 0):
                self.log("I'm the last process, I'm starting to send the token")
                self.com.sendToken()

            # self.test_async_messages_and_synchro(loop)
            # self.test_section_critique(loop)
            # self.test_sync_messages(loop)
            self.test_all(loop)

            loop += 1

        self.dead = True

    def test_async_messages_and_synchro(self, loop):

        if (loop == 1):
            self.com.broadcastSync(0, "message broadcast")

        if self.getName() == "P0":

            if (loop == 1):
                self.com.broadcast("broadcast info to all")
                self.com.sendTo(2, "dm to id 2")
                self.com.synchronize()

        if self.getName() == "P1":
            self.log("I'm gonna sleep for 1 second")
            sleep(1)
            self.log("I'm done sleeping")
            if (loop == 1):
                self.com.synchronize()

        if (self.getName() == "P2"):
            if (loop == 1):
                self.com.synchronize()

            self.log("I'm doing something for 2 seconds")
            sleep(2)
            self.log("I'm done doing something")

    def test_section_critique(self, loop):

        if self.getName() == "P0":
            if (loop == 2):
                try:
                    self.com.requestSC()
                    self.log("using the token")
                    sleep(2)
                    self.log("I'm done, I'll release the token")
                    self.com.releaseSC()
                except:
                    self.log(
                        "I'm can't access the critical section since I'm dying")

        if (self.getName() == "P2"):
            try:
                self.com.requestSC()
                self.log("using the token")
                sleep(2)
                self.log("I'm done, I'll release the token")
                self.com.releaseSC()
            except:
                self.log(
                    "I'm can't access the critical section since I'm dying")

    def test_sync_messages(self, loop):
        if (loop == 1):
            self.com.broadcastSync(0, "message broadcast")

        if self.getName() == "P0":
            if (loop == 1):
                # sleep is here to avoid the message to be sent before the receiver is ready
                sleep(1)
                self.com.sendToSync(1, "sending sync dm to 1")

        if self.getName() == "P1":
            if (loop == 1):
                self.com.recevFromSync(0)

            self.log("I'm gonna sleep for 1 second")
            sleep(1)
            self.log("I'm done sleeping")

    def test_all(self, loop):
        if (loop == 1):
            self.com.broadcastSync(0, "message broadcast")

        if self.getName() == "P0":

            if (loop == 1):
                self.com.broadcast("broadcast info to all")
                # sleep is here to avoid the message to be sent before the receiver is ready
                sleep(1)
                self.com.sendToSync(1, "sending sync dm to P1")
                self.com.sendTo(2, "dm async to P2")
                self.com.synchronize()

            if (loop == 2):
                try:
                    self.com.requestSC()
                    self.log("using the token")
                    sleep(2)
                    self.log("I'm done, I'll release the token")
                    self.com.releaseSC()
                except:
                    self.log(
                        "I'm can't access the critical section since I'm dying")

        if self.getName() == "P1":
            if (loop == 1):
                self.com.recevFromSync(0)
            self.log("I'm gonna sleep for 1 second")
            sleep(1)
            self.log("I'm done sleeping")

            if (loop == 1):
                self.com.synchronize()

        if (self.getName() == "P2"):
            try:
                self.com.requestSC()
                self.log("using the token")
                sleep(2)
                self.log("I'm done, I'll release the token")
                self.com.releaseSC()
            except:
                self.log(
                    "I'm can't access the critical section since I'm dying")

            if (loop == 1):
                self.com.synchronize()
