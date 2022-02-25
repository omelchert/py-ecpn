import sys
import numpy as np
from helper_ECPN import helper_sim


def single_run(N_val, h0_val):

    sim_pars = {
        'J0': 1.2,
        'chi': 1.0,
        'sigma': 0.0,
        'dh': 0.001,
        't_min': 0,
        't_max': 1e6,
        'Nt': 100001,
        'log_every_n': 100
    }

    helper_sim(N=N_val, h0=h0_val, **sim_pars)


if __name__=='__main__':
    N_val = int(sys.argv[1])
    h0_val = float(sys.argv[2])
    single_run(N_val, h0_val)
