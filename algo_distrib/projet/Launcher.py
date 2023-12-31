from time import sleep
from Process import Process

if __name__ == '__main__':

    # bus = EventBus.getInstance()
    nbProcess = 3

    # customNames = ["Barman", "Flo", "Simon"] # for demo

    customNames = [f"P{i}" for i in range(nbProcess)]  # for other tests
    procs = []
    for i in range(nbProcess):
        procs.append(Process(customNames[i], nbProcess))
        print("process", i, "created")
    sleep(20)

    for p in procs:
        p.stop()

    # bus.stop()
