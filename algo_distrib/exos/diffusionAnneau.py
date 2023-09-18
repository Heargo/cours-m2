from mpi4py import MPI

comm = MPI.COMM_WORLD
me = comm.Get_rank()
size = comm.Get_size()
prev = (me-1+size) % size
next = (me+1) % size
clock = 0


def log(msg):
    print(f"[{clock}] node <{me}>: {msg}", flush=True)


def incrementClock(buff=None):
    global clock
    if (buff == None):
        clock += 1
    else:
        clock = max(clock, buff["clock"])+1
        buff["clock"] = clock
    return buff


def send(buff, dest):
    buff = incrementClock(buff)
    log(f"SEND [pending] {buff['data']} to {dest}")
    comm.send(buff, dest=dest, tag=99)
    log(f"SEND [ok] {buff['data']} to {dest}")


def receive(source):
    log(f"GET [pending] from {source}")
    buff = comm.recv(source=source, tag=99)
    incrementClock(buff)
    log(f"GET [ok] {buff['data']} from {source}")
    return buff


def mirrorPosFromStart(start):
    return (start+(size//2)) % size


def receiveFromNext(start):
    log(f"me <{me}> start <{start}> do i receive from next ? <{(me - start)%size > (size//2)}> ( {me} - {start} ) % {size} > {size//2})")
    return (me - start) % size > (size//2)


def isLastNodeToReceive(start):
    last_1 = mirrorPosFromStart(start)
    last_2 = (last_1+1) % size
    return (me == last_1) or (me == last_2)


def main(start=0, buff={"data": "Hello", "clock": 0}):
    if me == start:
        log(f"I start the diffusion of {buff['data']}")
        log(f"Last node to receive is <{mirrorPosFromStart(start)}> and <{(mirrorPosFromStart(start)+1)%size}>")
        send(buff, next)
        send(buff, prev)
    else:
        if (receiveFromNext(start)):
            # si on est le dernier noeud qui recoit par le suivant
            if (isLastNodeToReceive(start)):
                buff = receive(next)
            else:
                buff = receive(next)
                send(buff, prev)
        else:
            # si on est le dernier noeud qui recoit par le précédent
            if (isLastNodeToReceive(start)):
                buff = receive(prev)
            else:
                buff = receive(prev)
                send(buff, next)


log("start")
main(0)
