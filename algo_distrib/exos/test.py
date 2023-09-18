from mpi4py import MPI
comm = MPI.COMM_WORLD
me = comm.Get_rank()
size = comm.Get_size()
print("Hi from <"+str(me)+">")