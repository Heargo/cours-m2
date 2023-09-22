from threading import Thread, Semaphore
from pyeventbus3.pyeventbus3 import *
from time import sleep
import uuid
from random import randint

from messages.Message import Message
from messages.BroadcastMessage import BroadcastMessage
from messages.TargetMessage import TargetMessage
from messages.Token import Token
from messages.Sync import Sync
from messages.Stop import Stop
from messages.Acknowledge import Acknowledge
from messages.Connect import Connect
from messages.ConnectConfirmation import ConnectConfirmation
from messages.Heartbit import Heartbit


class Com(Thread):

    def __init__(self, nbProcess, showLogs=False):
        Thread.__init__(self)
        PyBus.Instance().register(self, self)

        self.nbProcess = nbProcess
        self.showLogs = showLogs

        # dynamic id
        # this id is only used during the connection phase. Once the myId is confirmed, this id is not used anymore except for heartbit
        self.uniqueUUID = uuid.uuid4()
        self.myId = None
        self.confirmedId = False
        self.idDict = {}  # key: uuid, value: int

        # heartbit
        self.lastHeartbit = {}  # key: uuid, value: timestamp
        self.heartbitThread = Thread(target=self._hearbit)
        self.verifHeartBitThread = Thread(target=self._verifyHearbit)

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

        # list of aknowledgements messages received. This is used for the synchronous communication
        self.syncAknowledgement = []
        # keep track of already acknowledged messages to avoid sending multiple aknowledgements for the same message
        self.alreadyAcknowledged = []

        # state. If alive, the process is running.
        # If dead, the process is stopped if not alive and not dead, the process is being killed (zombie)
        self.alive = True
        self.dead = False

        self.start()
        self._connect()  # connect to the network and get an id

    def _initBackgroundTasks(self):
        """
        The function initializes the background tasks that are running in parallel to the main thread. 
        The background tasks are the heartbit and the verification of the heartbit.
        """
        self.heartbitThread.start()
        self.verifHeartBitThread.start()

    #############################
    ######  DYNAMIC ID    #######
    #############################

    @subscribe(threadMode=Mode.PARALLEL, onEvent=ConnectConfirmation)
    def _onConnectConfirmation(self, event: ConnectConfirmation):
        """
        Handles the confirmation of the list of IDs by updating the idDict and the id of the current process.

        :param event: The parameter "event" is of type ConnectConfirmation. It represents an event that
        confirms a successful connection
        :type event: ConnectConfirmation
        """
        self.idDict = event.getContent()
        self.myId = self.idDict[self.uniqueUUID]
        self.confirmedId = True
        self.log(f"Confirmed id: {self.myId}")

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Connect)
    def _onConnect(self, event: Connect):
        """
        Handles connection events and assigns a new ID to the connecting
        process if the current process is the leader. This method is called when a Connect event is posted on the bus.

        :param event: The parameter "event" is of type "Connect"
        :type event: Connect
        :return: If the process is not the leader, then the function will return without performing any further actions.
        """
        # add info to idDict
        self.idDict[event.getSender()] = event.getContent()

        # if everyone sent a connect message, I update the idDict and send a confirmation
        if (len(self.idDict) == self.nbProcess):
            self.log(f"Everyone sent a connect message")
            idIncrement = 0
            for uuid in self.idDict.keys():
                self.log(
                    f"Process {uuid} has now id {idIncrement}")
                self.idDict[uuid] = idIncrement
                idIncrement += 1

            # send confirmation
            connConfirm = ConnectConfirmation(self.uniqueUUID, self.idDict)
            PyBus.Instance().post(connConfirm)
            self.log(f"SEND {connConfirm}")

    def _connect(self):
        """
        Send a connection message to the bus with a unique uuid and requests an ID.
        """
        randomID = randint(0, self.nbProcess-1)
        self.log(
            f"I'm connecting to the network with unique id {self.uniqueUUID}. I want the id {randomID}")
        conn = Connect(self.uniqueUUID, randomID)
        PyBus.Instance().post(conn)

    def getId(self):
        """
        Waits for a confirmed ID. Waits for every process to have an ID. This function is blocking.
        :return: The method is returning the id from 0 to (n-1) where n is the number of processes in total.
        """
        # wait until id is confirmed
        while (not self.confirmedId):
            sleep(0.1)

        self._initBackgroundTasks()

        return self.myId

    #############################
    ###### GENERAL METHODS ######
    #############################

    def inc_clock(self, externalClock=0):
        """
        The function increments a clock value, taking into account an external clock value.

        :param externalClock: The externalClock parameter is an optional parameter that represents the
        value of an external clock. If provided, it will be used as a base to update the internal clock value 
        if it's value is greater than the internal clock. If not provided, the internal clock value will be 
        incremented by 1.
        defaults value is 0 (optional)
        """
        self.clockSem.acquire()
        self.clock = max(self.clock, externalClock)+1
        self.clockSem.release()

    def log(self, msg):
        """
        The log function prints a formatted message with information about the object's state and a
        given message.
        The format is as follows:
        `COM<id> [OFFICIAL] [LIVE|ZOMB|DEAD] [clock] : message`
        where `id` is the id of the process or the uuid if the process don't have a confirmed id yet, `OFFICIAL` is a string that indicates if the process has a confirmed id,
        `LIVE|ZOMB|DEAD` is a string that indicates the state of the process, `clock` is the value of the clock
        and `message` is the message to be logged.

        :param msg: The `msg` parameter is a string that represents the message to be logged
        """
        if (not self.showLogs):
            return

        print(
            f"\tCOM<{self.myId if self.confirmedId else self.uniqueUUID}> {'OFFICIAL'if self.confirmedId else ''} [{'LIVE' if self.alive else 'ZOMB' if not self.dead else 'DEAD'}] [{self.clock}] : {msg}", flush=True)

    #############################
    ###### SYNCHRONIZATION ######
    #############################

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Stop)
    def _onStop(self, event: Stop):
        """
        Handles the event when a process stops by managing the list of stopped and synchronizing processes.

        :param event: The event parameter is an message sent by a process that has stopped.
        :type event: Stop
        """
        stoppedProc = event.getSender()
        if (stoppedProc == self.uniqueUUID):
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
    def _onSync(self, event: Sync):
        """
        Handles the synchronization event by managing the list of synchronizing processes.

        :param event: The event parameter is an instance of the Sync class. It represents a
        synchronization event that has occurred
        :type event: Sync
        """
        # get uuid from str
        senderUUID = event.getSender()
        if senderUUID not in self.synchronizingProcesses:
            self.synchronizingProcesses.append(senderUUID)
            # update clock
            self.inc_clock(event.getClock())

        if self._isAllProcessSynchonized() and self.alive:
            self.log("The last process has synchronized, I'm starting again")
            self.synchronizingProcesses = []

    def _isAllProcessSynchonized(self):
        """
        The function checks if all processes are synchronized. It does not take into account the stopped processes.

        :return: a boolean value. True if all processes are synchronized, False otherwise.
        """
        # to avoid wrong logs return true if the list is empty
        if len(self.synchronizingProcesses) == 0:
            return True

        for uuidProc in self.idDict.keys():
            if uuidProc not in self.synchronizingProcesses and uuidProc not in self.stoppedProcesses:
                return False
        return True

    def synchronize(self):
        """
        When called, the function sends a synchronization message to all processes and waits until all processes have synchronized.
        This function is blocking.
        """
        self.log(f"SYNCHRONIZING")
        sync = Sync(self.uniqueUUID)
        sync.setClock(self.clock)
        self.synchronizingProcesses.append(self.uniqueUUID)
        PyBus.Instance().post(sync)

        # we wait until the synchronization is done
        while (self.uniqueUUID in self.synchronizingProcesses):
            sleep(0.5)
            self.log(
                f"Process {self.myId}| {self.uniqueUUID} is synchronizing ")

    def stop(self):
        """
        Stop the com thread and perform some cleanup tasks.
        """
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
    def _onToken(self, event: Token):
        """
        Handle token reception. If meant for the current instance, sets a flag to indicate
        possession of the token, and sends the token if it is not needed after 300ms.

        :param event: The token message received from the bus
        :type event: Token
        :return: If the token is not meant for the current instance, the function returns without performing any further actions.
        """
        if not event.isForMe(self.myId):
            return

        self.log(f"RECEIVED token from {event.sender}")
        self.tokenPossessed = True
        sleep(0.3)
        if not self.needToken:
            self.log("I don't need the token, I'm gonna send it")
            self.sendToken()

    def sendToken(self):
        """
        Sends a token to the next process if the current process is alive. The token is sent to the next process in loop and 
        give access to the critical section when possessed by a process.
        :return: If the current process is not alive, the function returns without performing any further actions.
        """
        if not self.alive:
            return

        nextProcess = (self.myId+1) % self.nbProcess
        token = Token(self.myId, nextProcess)
        self.log(f"SEND {token}")
        self.tokenPossessed = False
        PyBus.Instance().post(token)

    def requestSC(self):
        """
        Requests access the the critical section and waits until access is granted. This function is blocking.
        Must be called before entering the critical section.
        """
        self.needToken = True

        while not self.tokenPossessed:
            sleep(0.1)
            if (not self.alive):
                raise Exception("I'm dying")
        self.log("I have the token now, I'm gonna use it for a while")

    def releaseSC(self):
        """
        Release the access to the critical section. Must be called after leaving the critical section.
        """
        self.needToken = False
        self.sendToken()

    #############################
    ##  COMMUNICATION - ASYNC  ##
    #############################

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Message)
    def _onMessage(self, event: Message):
        """
        Handles the reception of a message by incrementing the clock and adding the message to the inbox.

        :param event: The parameter "event" is of type Message
        :type event: Message
        """
        self.inc_clock(event.getClock())
        self.log(f"RECEIVED {event}")
        self.inbox.append(event)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=BroadcastMessage)
    def _onBroadcast(self, event: BroadcastMessage):
        """
        Handles the reception of a broadcast message by incrementing the clock and adding the message to the inbox.

        :param event: A Message that is being broadcasted
        :type event: BroadcastMessage
        :return: If the message is emitted by the current process, the function returns without performing any further actions.
        """
        if event.isFromMe(self.myId):
            return

        self.inc_clock(event.getClock())
        self.log(f"RECEIVED {event}")
        self.inbox.append(event)

    @subscribe(threadMode=Mode.PARALLEL, onEvent=TargetMessage)
    def _onTarget(self, event: TargetMessage):
        """
        Handles the reception of a message by incrementing the clock and adding the message to the inbox.

        :param event: The parameter "event" is an instance of the class "TargetMessage"
        :type event: TargetMessage
        :return: If the message is not for the current instance, the function returns without performing any further actions.
        """
        if not event.isForMe(self.myId):
            return

        self.inc_clock(event.getClock())
        self.log(f"RECEIVED {event}")
        self.inbox.append(event)

    def send(self, data):
        """
        Sends a message with data and increments the clock.

        :param data: The `data` parameter is the message that you want to send. It can be any data that
        you want to transmit to another component or system
        :return: The method is returning the ID of the message that was sent.
        """
        self.inc_clock()
        msg = Message(self.myId, data)

        msg.setClock(self.clock)
        self.log(f"SEND {msg}")
        PyBus.Instance().post(msg)
        return msg.getId()

    def broadcast(self, data, type="ASYNC"):
        """
        The function broadcasts a message with the given data and type, and returns the ID of the
        message.

        :param data: The `data` parameter is the information that you want to broadcast.
        :param type: DO NOT USE OUTSIDE OF COM CLASS. optional parameter that specifies the type of broadcast.
        If you want to use a synchronous broadcast, use the  `broadcastSync()` method.
        :return: The method is returning the ID of the broadcast message.
        """
        self.inc_clock()
        msg = BroadcastMessage(self.myId, data, type)

        msg.setClock(self.clock)
        self.log(f"BROADCAST {msg}")
        PyBus.Instance().post(msg)
        return msg.getId()

    def sendTo(self, target, data, type="ASYNC"):
        """
        Sends a message to a target with the specified data and type, and returns the
        message ID.

        :param target: The `target` parameter represents the id of the target process that you want to send the message to.
        :param data: The `data` parameter is the information that you want to send to the target. 
        :param type: DO NOT USE OUTSIDE OF COM CLASS. optional parameter and specifies the type of message being sent. If you 
        want to use a synchronous message, use the `sendToSync()` method.
        :return: The method `sendTo` returns the ID of the message that was sent.
        """
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
    def _onAcknowledge(self, event: Acknowledge):
        """
        Handles the reception of an acknowledgement message by incrementing the clock and adding the message to the list of
        acknowledged messages.

        :param event: The parameter `event` represents an acknowledgement message.
        :type event: Acknowledge
        :return: If the acknowledgement message is not for the current instance, the function returns without performing any further actions.
        """
        if not event.isForMe(self.myId):
            return

        self.log(f"RECEIVED {event}")
        self.inc_clock(event.getClock())
        self.syncAknowledgement.append(event)

    def _sendAcknowledge(self, target, id):
        """
        The function sends an acknowledgment message relative to a specific message to a target processus.

        :param target: The `target` parameter is the id of the target process that you want to send the acknowledgment to.
        :param id: The `id` parameter is the id of the message that is being acknowledged.
        """
        ack = Acknowledge(self.myId, target, id)
        ack.setClock(self.clock)
        self.log(f"SEND {ack}")
        PyBus.Instance().post(ack)
        self.alreadyAcknowledged.append(id)

    def _hasNAknowledgementForId(self, id, n=1):
        """
        The function checks if the number of acknowledgements relative to a specific message ID is greater than or
        equal to a given threshold.

        :param id: The `id` parameter is the id of the message that is being acknowledged.
        :param n: The parameter "n" represents the minimum number of acknowledgements required for the
        given "id" in order to return True, defaults to 1 (optional)
        :return: The method returns a boolean value. True if the number of acknowledgements is greater than or equal to the threshold, False otherwise.
        """
        count = 0
        for ackMsg in self.syncAknowledgement:
            if ackMsg.getContent() == id:
                count += 1
        # self.log(f"_hasNAknowledgementForId <id={id},n={n}> ? {count >= n}")
        return count >= n

    def broadcastSync(self, fromId, data):
        """
        Broadcast data to all processes and wait until all processes have received the message. This function is blocking.

        :param fromId: The `fromId` parameter represents the ID of the process that is sending the
        broadcast message
        :param data: The "data" parameter is the information that you want to broadcast.
        """
        if (self.myId == fromId):
            msgId = self.broadcast(data, "SYNC")
            # we wait until everyone has received the message
            while not self._hasNAknowledgementForId(msgId, self.nbProcess-1):
                sleep(0.1)
                # self.log(
                #     f"Waiting for aknowledgements for message {msgId}")

            self.syncAknowledgement = []
            self.log("Everyone received the broadcast")
        else:
            self.recevFromSync(fromId)

    def sendToSync(self, target, data):
        """
        The function sends a message to a target and waits until the target has received the message. This function is blocking.

        :param target: The "target" parameter parameter represents the ID of the process that is receiving the message.
        :param data: The `data` parameter is the message or data that you want to send to the target.
        """
        msgId = self.sendTo(target, data, "SYNC")

        # we wait until the target has received the message
        while not self._hasNAknowledgementForId(msgId, 1):
            sleep(0.1)
            self.log(
                f"Waiting for <{target}> aknowledgements")

        self.syncAknowledgement = []
        self.log(f"Target <{target}> received the message")

    def getLastPendingSyncMessage(self):
        """
        Returns the last synchronous message from the inbox that hasn't been acknowledged yet.
        :return: A message or None if no message is found.
        """
        # return last message that has type "SYNC" in the inbox and that has not been acknowledged yet
        for i in range(len(self.inbox)-1, -1, -1):
            msg = self.inbox[i]
            if (msg.type == "SYNC" and msg.getId() not in self.alreadyAcknowledged):
                return msg
        return None

    def recevFromSync(self, fromId):
        """
        Waits until a message is received from a specific process. This function is blocking.

        :param fromId: The `fromId` parameter represents the ID of the sender from whom the message is
        expected to be received
        :return: The method returns the message that was received from the specified process.
        """
        lastSyncMessage = self.getLastPendingSyncMessage()
        while lastSyncMessage == None or lastSyncMessage.sender != fromId:
            sleep(0.2)
            self.log(f"Waiting for a message from {fromId}")
            lastSyncMessage = self.getLastPendingSyncMessage()

        self.log(f"Received message {lastSyncMessage} from {fromId}")
        self._sendAcknowledge(fromId, lastSyncMessage.getId())

        return lastSyncMessage

    #############################
    ######    HEARTBIT    #######
    #############################

    @subscribe(threadMode=Mode.PARALLEL, onEvent=Heartbit)
    def _onHearbit(self, event: Heartbit):
        """
        Handles the reception of a heartbit message by updating the last heartbit timestamp.

        :param event: The parameter "event" is of type Heartbit
        :type event: Heartbit
        """
        self.lastHeartbit[event.getSender()] = time.time()
        pass

    def _hearbit(self):
        """
        The function sends a hearbit message to all processes. This function is called every 1 seconds.
        """
        while self.alive:
            # self.log("Sending hearbit: I'm please don't forget me ")
            heartbit = Heartbit(self.uniqueUUID)
            PyBus.Instance().post(heartbit)
            sleep(1)

    def _verifyHearbit(self):
        """
        The function verifies a process stopped to live. This function is called every 1 seconds.
        """
        while self.alive:
            for uuid in self.lastHeartbit.keys():
                if (time.time() - self.lastHeartbit[uuid] > 5 and uuid not in self.stoppedProcesses):
                    self.log(
                        f"Process {uuid} is probably dead and didn't warned")
                    self._onStop(Stop(uuid))
            sleep(1)
