from threading import Lock, Thread

from time import sleep, time

# from geeteventbus.subscriber import subscriber
# from geeteventbus.eventbus import eventbus
# from geeteventbus.event import event

# from EventBus import EventBus
from Bidule import Bidule
from messages.Message import Message
from messages.BroadcastMessage import BroadcastMessage
from messages.TargetMessage import TargetMessage
from messages.Token import Token

from pyeventbus3.pyeventbus3 import *


class Process(Thread):
    nbProcess = 0

    def __init__(self, name):
        Thread.__init__(self)

        self.myId = Process.nbProcess
        Process.nbProcess += 1
        self.setName(name)
        self.clock = 0
        PyBus.Instance().register(self, self)
        self.tokenPossessed = False
        self.needToken = False
        self.synchronizingProcesses = []

        self.alive = True
        self.start()

    def incrementClock(self, externalClock=0):
        self.clock = max(self.clock, externalClock)+1

    def log(self, msg):
        print(f"[{self.clock}] node <{self.myId}>: {msg}", flush=True)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Message)
    def onMessage(self, event: Message):
        self.incrementClock(event.getClock())
        self.log(f"RECEIVED {event}")

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def onBroadcast(self, event: BroadcastMessage):
        if event.isFromMe(self.myId):
            return

        self.incrementClock(event.getClock())
        self.log(f"RECEIVED {event}")

    @subscribe(threadMode=Mode.PARALLEL, onEvent=TargetMessage)
    def onTarget(self, event: TargetMessage):
        if not event.isForMe(self.myId):
            return

        self.incrementClock(event.getClock())
        self.log(f"RECEIVED {event}")

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Token)
    def onToken(self, event: Token):
        if not event.isForMe(self.myId):
            return

        self.log(f"RECEIVED token from {event.sender}")
        self.tokenPossessed = True

        if not self.needToken:
            sleep(0.1)
            self.sendToken()

    def sendToken(self):
        if not self.alive:
            return

        nextProcess = (self.myId+1) % Process.nbProcess
        token = Token(self.myId, nextProcess)
        self.log(f"SEND {token}")
        self.tokenPossessed = False
        PyBus.Instance().post(token)

    def requestToken(self):
        self.needToken = True

        while not self.tokenPossessed:
            sleep(0.1)

    def releaseToken(self):
        self.needToken = False
        self.sendToken()

    def send(self, data):
        self.incrementClock()
        msg = Message(self.myId, data)

        msg.setClock(self.clock)
        self.log(f"SEND {msg}")
        PyBus.Instance().post(msg)

    def broadcast(self, data):
        self.incrementClock()
        msg = BroadcastMessage(self.myId, data)

        msg.setClock(self.clock)
        self.log(f"BROADCAST {msg}")
        PyBus.Instance().post(msg)

    def sendTo(self, target, data):
        self.incrementClock()
        msg = TargetMessage(self.myId, target, data)

        msg.setClock(self.clock)
        self.log(f"SEND {msg}")
        PyBus.Instance().post(msg)

    def run(self):
        loop = 0
        while self.alive:
            self.log(f"Loop: {loop}")
            sleep(1)

            if self.getName() == "P1":
                self.sendToken()  # P1 starts with the token
                b1 = Bidule("message normal")
                b2 = Bidule("message broadcast")
                b3 = Bidule("message target")

                self.send(b1)
                self.broadcast(b2)
                self.sendTo(2, b3)

            if (self.getName() == "P3"):
                self.requestToken()
                self.log("I have the token I'm gonna use it for a while")
                sleep(2)
                self.log("I'm done, I'll release the token")
                self.releaseToken()

            loop += 1

        self.log("stopped")

    def stop(self):
        self.alive = False
        self.join()
