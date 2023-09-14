from mpi4py import MPI

comm = MPI.COMM_WORLD
me = comm.Get_rank()
size = comm.Get_size()
print("Hi from <"+str(me)+">")
if me == 0:
    buf = ["coucou"]
    print("I'm <"+str(me)+">: send " + buf[0])
    for i in range(1, size):
	    comm.send(buf, dest=i, tag=99)
else:
    buf = comm.recv(source=0, tag=99)
    print("I'm <"+str(me)+">: receive " + buf[0])
