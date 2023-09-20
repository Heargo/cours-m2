from threading import Thread, Semaphore
from pyeventbus3.pyeventbus3 import *
from time import sleep

from messages.Message import Message
from messages.BroadcastMessage import BroadcastMessage
from messages.TargetMessage import TargetMessage
from messages.Token import Token
from messages.Sync import Sync
from messages.Stop import Stop
from messages.Acknowledge import Acknowledge


class Com(Thread):

    def __init__(self, myId, nbProcess):
        Thread.__init__(self)
        PyBus.Instance().register(self, self)

        self.myId = myId
        self.nbProcess = nbProcess

        # Lamport clock
        self.clockSem = Semaphore()
        self.clock = 0
        # synchronization. Choose to use two boolean to make the conditions easier to read and understand
        self.tokenPossessed = False
        self.needToken = False
        self.synchronizingProcesses = []
        self.stoppedProcesses = []
        # inbox
        self.inbox = []
        # sync aknowledgement list
        self.syncAknowledgement = []
        # keep track of already acknowledged messages to avoid sending multiple aknowledgements for the same message
        self.alreadyAcknowledged = []

        # state. If alive, the process is running.
        # If dead, the process is stopped if not alive and not dead, the process is being killed (zombie)
        self.alive = True
        self.dead = False
        self.start()

    #############################
    ######  DYNAMIC ID    #######
    #############################

    # TODO

    #############################
    ###### GENERAL METHODS ######
    #############################

    def inc_clock(self, externalClock=0):
        self.clockSem.acquire()
        self.clock = max(self.clock, externalClock)+1
        self.clockSem.release()

    def log(self, msg):
        print(
            f"\tCOM<{self.myId}> [{'LIVE' if self.alive else 'ZOMB' if not self.dead else 'DEAD'}] [{self.clock}] : {msg}", flush=True)

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

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Sync)
    def onSync(self, event: Sync):
        if event.getSender() not in self.synchronizingProcesses:
            self.synchronizingProcesses.append(event.getSender())

        if self.isAllProcessSynchonized() and self.alive:
            self.log("The last process has synchronized, I'm starting again")
            self.synchronizingProcesses = []

    def isAllProcessSynchonized(self):
        # to avoid wrong logs return true if the list is empty
        if len(self.synchronizingProcesses) == 0:
            return True

        for i in range(self.nbProcess):
            if i not in self.synchronizingProcesses and i not in self.stoppedProcesses:
                return False
        return True

    def synchronize(self):
        self.log(f"SYNCHRONIZING")
        sync = Sync(self.myId)
        self.synchronizingProcesses.append(self.myId)
        PyBus.Instance().post(sync)

        # we wait until the synchronization is done
        while (self.myId in self.synchronizingProcesses):
            sleep(0.5)
            self.log(f"Process {self.myId} is synchronizing")

    def stop(self):
        self.alive = False
        self.synchronizingProcesses = []
        self.log(f"Process {self.myId} is stopping")
        stop = Stop(self.myId)
        PyBus.Instance().post(stop)
        self.join()
        self.log("coms are dead")

    #############################
    ######     TOKEN      #######
    #############################

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Token)
    def onToken(self, event: Token):
        if not event.isForMe(self.myId):
            return

        # self.log(f"RECEIVED token from {event.sender}")
        self.tokenPossessed = True

        if not self.needToken:
            sleep(0.1)
            # self.log("I don't need the token, I'm gonna send it")
            self.sendToken()

    def sendToken(self):
        if not self.alive:
            return

        nextProcess = (self.myId+1) % self.nbProcess
        token = Token(self.myId, nextProcess)
        # self.log(f"SEND {token}")
        self.tokenPossessed = False
        PyBus.Instance().post(token)

    def requestSC(self):
        self.needToken = True

        while not self.tokenPossessed:
            sleep(0.1)
            if (not self.alive):
                raise Exception("I'm dying")
        self.log("I have the token now, I'm gonna use it for a while")

    def releaseSC(self):
        self.needToken = False
        self.sendToken()

    #############################
    ##  COMMUNICATION - ASYNC  ##
    #############################

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Message)
    def onMessage(self, event: Message):
        self.inc_clock(event.getClock())
        self.log(f"RECEIVED {event}")
        self.inbox.append(event)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def onBroadcast(self, event: BroadcastMessage):
        if event.isFromMe(self.myId):
            return

        self.inc_clock(event.getClock())
        self.log(f"RECEIVED {event}")
        self.inbox.append(event)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=TargetMessage)
    def onTarget(self, event: TargetMessage):
        if not event.isForMe(self.myId):
            return

        self.inc_clock(event.getClock())
        self.log(f"RECEIVED {event}")
        self.inbox.append(event)

    def send(self, data):
        self.inc_clock()
        msg = Message(self.myId, data)

        msg.setClock(self.clock)
        self.log(f"SEND {msg}")
        PyBus.Instance().post(msg)
        return msg.getId()

    def broadcast(self, data, type="ASYNC"):
        self.inc_clock()
        msg = BroadcastMessage(self.myId, data, type)

        msg.setClock(self.clock)
        self.log(f"BROADCAST {msg}")
        PyBus.Instance().post(msg)
        return msg.getId()

    def sendTo(self, target, data, type="ASYNC"):
        self.inc_clock()
        msg = TargetMessage(self.myId, target, data, type)

        msg.setClock(self.clock)
        self.log(f"SEND {msg}")
        PyBus.Instance().post(msg)
        return msg.getId()

    #############################
    ##   COMMUNICATION - SYNC  ##
    #############################

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Acknowledge)
    def onAcknowledge(self, event: Acknowledge):
        if not event.isForMe(self.myId):
            return

        self.log(f"RECEIVED {event}")
        self.inc_clock(event.getClock())
        self.syncAknowledgement.append(event)

    def sendAcknowledge(self, target, id):
        ack = Acknowledge(self.myId, target, id)
        ack.setClock(self.clock)
        self.log(f"SEND {ack}")
        PyBus.Instance().post(ack)
        self.alreadyAcknowledged.append(id)

    def hasNAknowledgementForId(self, id, n=1):
        count = 0
        for ackMsg in self.syncAknowledgement:
            if ackMsg.getContent() == id:
                count += 1
        # self.log(f"hasNAknowledgementForId <id={id},n={n}> ? {count >= n}")
        return count >= n

    def broadcastSync(self, fromId, data):
        if (self.myId == fromId):
            msgId = self.broadcast(data, "SYNC")
            # we wait until everyone has received the message
            while not self.hasNAknowledgementForId(msgId, self.nbProcess-1):
                sleep(0.1)
                # self.log(
                #     f"Waiting for aknowledgements for message {msgId}")

            self.syncAknowledgement = []
            self.log("Everyone received the broadcast")
        else:
            self.recevFromSync(fromId)

    def sendToSync(self, target, data):
        msgId = self.sendTo(target, data, "SYNC")

        # we wait until the target has received the message
        while not self.hasNAknowledgementForId(msgId, 1):
            sleep(0.1)
            self.log(
                f"Waiting for <{target}> aknowledgements")

        self.syncAknowledgement = []
        self.log(f"Target <{target}> received the message")

    def getLastPendingSyncMessage(self):
        # return last message that has type "SYNC" in the inbox and that has not been acknowledged yet
        for i in range(len(self.inbox)-1, -1, -1):
            msg = self.inbox[i]
            if (msg.type == "SYNC" and msg.getId() not in self.alreadyAcknowledged):
                return msg
        return None

    def recevFromSync(self, fromId):
        lastSyncMessage = self.getLastPendingSyncMessage()
        while lastSyncMessage == None or lastSyncMessage.sender != fromId:
            sleep(0.2)
            self.log(f"Waiting for a message from {fromId}")
            lastSyncMessage = self.getLastPendingSyncMessage()

        self.log(f"Received message {lastSyncMessage} from {fromId}")
        self.sendAcknowledge(fromId, lastSyncMessage.getId())
