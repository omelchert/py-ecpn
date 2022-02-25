import sys
import os
import numpy as np
import multiprocessing as mp
from main_single_run import single_run


def main_MP(n_proc, N_val, h0_list):

    def worker(queue):
        while True:
            h0_curr = queue.get(block=True)
            if h0_curr is None:
               break
            single_run(N_val, h0_curr)

    queue = mp.Queue()
    pool = mp.Pool(n_proc, worker, (queue,))

    for i in range(h0_list.size):
        queue.put(h0_list[i])

    for i in range(n_proc):
        queue.put(None)

    queue.close()
    queue.join_thread()

    pool.close()
    pool.join()



if __name__=='__main__':
    n_proc = 13
    N = int(sys.argv[1])
    h0_list = np.linspace(0.6,0.9,13,endpoint=True)
    main_MP(n_proc, N, h0_list)
