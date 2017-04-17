# import ROOT
import tweepyScraper
from mpi4py import MPI
import sys
import cPickle as pick

WORKTAG = 0
DIETAG = 1

class Work():
    def __init__(self, workItems):
        self.workItems = workItems[:]

    def getNextItem(self):
        if len(self.workItems) == 0:
            return None
        return self.workItems.pop()

def master(wi):
    dataList = []
    size = MPI.COMM_WORLD.Get_size()
    current_work = Work(wi)
    comm = MPI.COMM_WORLD
    status = MPI.Status()
    for i in range(1, size):
        anext = current_work.getNextItem()
        if not anext: break
        comm.send(obj=anext, dest=i, tag=WORKTAG)

    while 1:
        anext = current_work.getNextItem()
        if not anext: break
        data = comm.recv(obj=None, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        dataList.append(data)
        comm.send(obj=anext, dest=status.Get_source(), tag=WORKTAG)

    for i in range(1,size):
        data = comm.recv(obj=None, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        dataList.append(data)

    for i in range(1,size):
        comm.send(obj=None, dest=i, tag=DIETAG)

    return dataList


def slave(do_work):
    comm = MPI.COMM_WORLD
    status = MPI.Status()
    while 1:
        data = comm.recv(obj=None, source=0, tag=MPI.ANY_TAG, status=status)
        if status.Get_tag(): break
        comm.send(obj=do_work(data), dest=0)

def main(work_list, do_work):
    rank = MPI.COMM_WORLD.Get_rank()
    name = MPI.Get_processor_name()
    size = MPI.COMM_WORLD.Get_size()

    if rank == 0:
        dataList = master(work_list)
    else:
        slave(do_work)
