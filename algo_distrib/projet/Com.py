from threading import Thread, Semaphore
from pyeventbus3.pyeventbus3 import *
from time import sleep
import uuid

from messages.Message import Message
from messages.BroadcastMessage import BroadcastMessage
from messages.TargetMessage import TargetMessage
from messages.Token import Token
from messages.Sync import Sync
from messages.Stop import Stop
from messages.Acknowledge import Acknowledge
from messages.Connect import Connect
from messages.ConnectConfirmation import ConnectConfirmation


class Com(Thread):

    def __init__(self, nbProcess):
        Thread.__init__(self)
        PyBus.Instance().register(self, self)

        self.nbProcess = nbProcess

        # dynamic id
        self.uniqueUUID = uuid.uuid4()
        self.lastAttributedId = 0
        self.myId = None
        self.confirmedId = False
        self.pendingConnect = []
        self.idDict = {}  # key: uuid, value: {id:int,leader:bool}

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
        self._connect()

    #############################
    ######  DYNAMIC ID    #######
    #############################

    @subscribe(threadMode=Mode.PARALLEL, onEvent=ConnectConfirmation)
    def onConnectConfirmation(self, event: ConnectConfirmation):
        # remove from pending connect
        for pc in self.pendingConnect:
            if pc.getSender() == event.getTarget():
                self.pendingConnect.remove(pc)
                break

        if (event.isForMe(self.uniqueUUID) and not self.confirmedId):
            self.log(
                f"Process {event.getSender()} has confirmed my id {event.getContent()}")
            self.myId = int(event.getContent())
            self.confirmedId = True

        # add to id dict
        self.idDict[event.getTarget()] = {
            "id": event.getContent(), "leader": event.getContent() == 0}
        self.log(f"DICT {self.idDict}")

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Connect)
    def onConnect(self, event: Connect):
        # only take care of this if I'm the process 0
        self.pendingConnect.append(event)
        if (self._getLeader() != self.uniqueUUID):
            self.log(
                f"CANNOT take care of {event} because I'm not the leader ({self._getLeader()}!={self.uniqueUUID})")
            return

        # as I'm the first process I can attribute a new one

        self.lastAttributedId += 1
        self.log(
            f"Process {event.getSender()} want id {event.getContent()}. I don't care, I'm gonna give him a new one ({self.lastAttributedId})")
        connConfirm = ConnectConfirmation(
            self.uniqueUUID, event.getSender(), self.lastAttributedId)
        PyBus.Instance().post(connConfirm)
        self.log(f"SEND {connConfirm} to {event.getSender()}")

    def _connect(self):
        self.log(
            f"I'm connecting to the network with unique id {self.uniqueUUID}. I want id 0")
        conn = Connect(self.uniqueUUID, 0)
        PyBus.Instance().post(conn)

    def _getLeader(self):
        # self.log(f"Getting leader{self.idDict}")
        for uuid, idDict in self.idDict.items():
            if idDict["leader"]:
                return uuid
        return None

    def getId(self):
        # wait 1 sec or until someone corrected the id
        t = 0
        while (not self.confirmedId and (t < 10 or self._getLeader() != None)):
            sleep(0.1)
            t += 1
        # if no one corrected the id, we consider that I'm the first process and confirm it
        if (not self.confirmedId):
            connConfirm = ConnectConfirmation(
                self.uniqueUUID, self.uniqueUUID, self.lastAttributedId)
            PyBus.Instance().post(connConfirm)
            self.log(f"SEND {connConfirm} to {self.uniqueUUID}")

            # take care of pending connect
            self.log(
                f"Taking care of pending connect ({len(self.pendingConnect)})")
            for connect in self.pendingConnect:
                self.onConnect(connect)

        return self.myId

    #############################
    ###### GENERAL METHODS ######
    #############################

    def inc_clock(self, externalClock=0):
        self.clockSem.acquire()
        self.clock = max(self.clock, externalClock)+1
        self.clockSem.release()

    def log(self, msg):
        print(
            f"\tCOM<{self.myId}> {'OFFICIAL'if self.confirmedId else ''} [{'LIVE' if self.alive else 'ZOMB' if not self.dead else 'DEAD'}] [{self.clock}] : {msg}", flush=True)

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
