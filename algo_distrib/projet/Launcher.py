from time import sleep
from Process import Process

if __name__ == '__main__':

    # bus = EventBus.getInstance()
    nbProcess = 3

    procs = []
    for i in range(nbProcess):
        procs.append(Process(f"P{i}", nbProcess))
        print("process", i, "created")

    sleep(15)

    for p in procs:
        p.stop()

    # bus.stop()
