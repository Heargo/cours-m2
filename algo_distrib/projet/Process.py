from threading import Thread

from time import sleep

# from geeteventbus.subscriber import subscriber
# from geeteventbus.eventbus import eventbus
# from geeteventbus.event import event

# from EventBus import EventBus
from Bidule import Bidule
from Com import Com

from pyeventbus3.pyeventbus3 import *


class Process(Thread):

    def __init__(self, name, id, nbProcess):
        Thread.__init__(self)

        self.myId = id
        self.setName(name)
        self.nbProcess = nbProcess
        self.alive = True
        self.dead = False

        self.com = Com(self.myId, nbProcess)
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
        while self.alive:
            self.log(f"Loop: {loop}")
            sleep(1)

            if (self.myId == self.nbProcess-1 and loop == 0):
                self.log("I'm the last process, I'm starting to send the token")
                self.com.sendToken()

            if (loop == 1):
                b2 = Bidule("message broadcast")
                self.com.broadcastSync(0, b2)

            if self.getName() == "P0":

                if (loop == 1):
                    b1 = Bidule("message normal")
                    b3 = Bidule("message target")

                    self.com.broadcast(b1)
                    # sleep is here to avoid the message to be sent before the receiver is ready
                    # TODO: fix negative aknowledgements when having sendtosync and broadcast sync
                    # sleep(1)
                    # self.com.sendToSync(1, b3)
                    # self.com.sendTo(2, b3)
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
                # self.com.recevFromSync(0)
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

            loop += 1

        self.dead = True
