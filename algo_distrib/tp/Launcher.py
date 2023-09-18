from time import sleep
from Process import Process

if __name__ == '__main__':

    # bus = EventBus.getInstance()

    p1 = Process("P1")
    p2 = Process("P2")
    p3 = Process("P3")

    sleep(15)

    p1.stop()
    p2.stop()
    p3.stop()

    # bus.stop()
