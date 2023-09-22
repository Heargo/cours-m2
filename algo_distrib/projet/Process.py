from threading import Thread

from time import sleep

# from geeteventbus.subscriber import subscriber
# from geeteventbus.eventbus import eventbus
# from geeteventbus.event import event

# from EventBus import EventBus
from Com import Com

from pyeventbus3.pyeventbus3 import *

from demoEntities.Drink import Drink


class Process(Thread):

    def __init__(self, name, nbProcess):
        Thread.__init__(self)

        self.setName(name)
        self.nbProcess = nbProcess
        self.alive = True
        self.dead = False

        self.com = Com(nbProcess, showLogs=False)
        self.myId = None
        self.start()

        # demo infos
        self.drinkedBeers = []

    def log(self, msg):

        print(
            f"PRO<{self.name} | {self.myId}> [{'LIVE' if self.alive else 'ZOMB' if not self.dead else 'DEAD'}] {msg}", flush=True)

    #############################
    ######      RUN       #######
    #############################

    def stop(self):
        self.alive = False
        self.synchronizingProcesses = []
        self.log(f"I'm tired, I'm leaving the party, bye bye")
        self.com.stop()
        self.join()
        self.log("left the party")

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
            # self.test_all(loop)
            self.test_demo(loop)

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

    def serveDrink(self, drink: Drink, to):
        self.log(f"preparing {drink} for {to}")
        sleep(.5)
        self.log(f"serving {drink} to {to}")
        self.com.sendToSync(to, drink)

    def serveRound(self, drinks: Drink):
        self.log(f"preparing round")
        sleep(3)
        self.log(f"serving round")
        self.com.broadcast(drinks)

    def drink(self):
        # if there is a drink not drunked yet, drink it

        for msg in self.com.inbox:
            drink = msg.getContent()
            if (isinstance(drink, Drink) and msg.getId() not in self.drinkedBeers):
                self.log(f"drinking {drink}")
                if (self.name == "Flo"):
                    sleep(3)
                elif (self.name == "Simon"):
                    sleep(1)
                self.drinkedBeers.append(msg.getId())
                self.log(
                    f"finished drinking {drink} it was my {len(self.drinkedBeers)}th beer")

    def go_to_toilet(self):
        self.log("I'm wanna go to the toilet")
        self.com.requestSC()
        self.log("I'm going to the toilet")
        sleep(3)
        self.com.releaseSC()
        self.log("I'm back from the toilet")

    def test_demo(self, loop):
        # Barman is 0, Flo is 1, Simon is 2
        # Simon is a heavy drinker and take only 1 second to drink a beer
        # Flo is a moderate drinker and take 3 seconds to drink a beer
        # Barman takes .5 second to serve a beer and 3 seconds to prepare a round
        # Barman is the only one who can serve a beer
        # Simon and Flo can only drink when they have a beer.
        # at loop 0 Simon and Flo ordering a beer
        # at loop 2 Barman prepare a round
        # at loop 4 they wait each other (synchronize) then both want to go to the toilet

        if (self.name == "Barman"):
            if (loop == 0):
                self.serveDrink(Drink("beer"), 1)
                self.serveDrink(Drink("beer"), 2)
            if (loop == 3):
                self.serveRound(Drink("beer"))
            if (loop == 4):
                self.log("I'm waiting (synchronize)")
                self.com.synchronize()
                self.log("Everyone is back !")

        if (self.name == "Flo"):
            if (loop == 0):
                self.com.recevFromSync(0)
            if (loop == 4):
                self.log("I'm waiting (synchronize)")
                self.com.synchronize()
                self.log("Everyone is back !")
                self.go_to_toilet()

        if (self.name == "Simon"):
            if (loop == 0):
                self.com.recevFromSync(0)
                self.drink()
            if (loop == 4):
                self.log("I'm waiting (synchronize)")
                self.com.synchronize()
                self.log("Everyone is back !")
                self.go_to_toilet()

        if (self.name in ["Flo", "Simon"]):
            self.drink()
