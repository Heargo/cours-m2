from threading import Thread

from time import sleep

# from geeteventbus.subscriber import subscriber
# from geeteventbus.eventbus import eventbus
# from geeteventbus.event import event

# from EventBus import EventBus
from Bidule import Bidule
from messages.Message import Message
from messages.BroadcastMessage import BroadcastMessage
from messages.TargetMessage import TargetMessage
from messages.Token import Token
from messages.Sync import Sync
from messages.Stop import Stop

from pyeventbus3.pyeventbus3 import *


class Process(Thread):
    nbProcess = 0

    def __init__(self, name):
        Thread.__init__(self)

        self.myId = Process.nbProcess
        Process.nbProcess += 1
        self.setName(name)
        PyBus.Instance().register(self, self)
        # Lamport clock
        self.clock = 0
        # synchronization. Choose to use two boolean to make the conditions easier to read and understand
        self.tokenPossessed = False
        self.needToken = False
        self.synchronizingProcesses = []
        self.stoppedProcesses = []

        # state. If alive, the process is running.
        # If dead, the process is stopped if not alive and not dead, the process is being killed (zombie)
        self.alive = True
        self.dead = False
        self.start()

    #############################
    ###### GENERAL METHODS ######
    #############################

    def incrementClock(self, externalClock=0):
        self.clock = max(self.clock, externalClock)+1

    def log(self, msg):
        print(
            f"[{'LIVE' if self.alive else 'ZOMB' if not self.dead else 'DEAD'}] [{self.clock}] node <{self.myId}>: {msg}", flush=True)

    #############################
    ###### SYNCHRONIZATION ######
    #############################

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Stop)
    def onStop(self, event: Stop):
        stoppedProc = event.getSender()
        if (stoppedProc == self.myId):
            self.log("I'm stopping")
            self.alive = False
            self.synchronizingProcesses = []
        else:
            self.log(
                f"Process {stoppedProc} has stopped. Let's verify if I can restart")

            # remove from synchronizing list
            if stoppedProc in self.synchronizingProcesses:
                self.synchronizingProcesses.remove(stoppedProc)

            # add to stopped list
            if (stoppedProc not in self.stoppedProcesses):
                self.stoppedProcesses.append(stoppedProc)

            # check if I can restart since a process is stopped
            if self.isAllProcessSynchonized():
                self.log(
                    "One process has stopped and all surviving processes have synchronized, I'm starting again")
                self.synchronizingProcesses = []
            else:
                self.log(
                    "One process has stopped but not all surviving processes have synchronized, I'm still waiting")

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Sync)
    def onSync(self, event: Sync):
        if event.getSender() not in self.synchronizingProcesses:
            self.synchronizingProcesses.append(event.getSender())

        if self.isAllProcessSynchonized() and self.alive:
            self.log("The last process has synchronized, I'm starting again")
            self.synchronizingProcesses = []

    def isAllProcessSynchonized(self):
        for i in range(Process.nbProcess):
            if i not in self.synchronizingProcesses and i not in self.stoppedProcesses:
                return False
        return True

    def synchronize(self):
        sync = Sync(self.myId)
        self.log(f"SYNCHRONIZING")
        self.synchronizingProcesses.append(self.myId)
        PyBus.Instance().post(sync)

    #############################
    ######     TOKEN      #######
    #############################

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
            if (not self.alive):
                raise Exception("I'm dying")

    def releaseToken(self):
        self.needToken = False
        self.sendToken()

    #############################
    ######  COMMUNICATION  ######
    #############################

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

    #############################
    ######      RUN       #######
    #############################

    def run(self):
        loop = 0
        while self.alive:

            # if we are synchronizing, we wait
            while (self.myId in self.synchronizingProcesses):
                sleep(0.5)
                self.log(f"Process {self.myId} is synchronizing")

            self.log(f"Loop: {loop}")
            sleep(1)

            if (self.myId == Process.nbProcess-1 and loop == 0):
                self.log("I'm the last process, I'm starting to send the token")
                self.sendToken()

            if self.getName() == "P1":
                b1 = Bidule("message normal")
                b2 = Bidule("message broadcast")
                b3 = Bidule("message target")

                # self.send(b1)
                # self.broadcast(b2)
                self.sendTo(2, b3)
                if (loop == 1):
                    self.synchronize()

            if self.getName() == "P2":
                self.log("I'm gonna sleep for 1 second")
                sleep(1)
                self.log("I'm done sleeping, I'm gonna synchronize")
                if (loop == 1):
                    self.synchronize()
                # self.synchronize()

            if (self.getName() == "P3"):
                try:
                    self.requestToken()
                    self.log("I have the token I'm gonna use it for a while")
                    sleep(2)
                    self.log("I'm done, I'll release the token")
                    self.releaseToken()
                except:
                    self.log("I'm can't use the token since I'm dying")

                if (loop == 1):
                    self.synchronize()

            loop += 1

        self.dead = True

    def stop(self):
        self.alive = False
        self.synchronizingProcesses = []
        self.log(f"Process {self.myId} is stopping")
        stop = Stop(self.myId)
        PyBus.Instance().post(stop)
        self.join()
        self.log("TERMINATED")
