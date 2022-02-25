"""
Simulate equal coupling photonic network (ECPN)

author: OM
date: 2022-01-08
"""
import sys; sys.path.append("../../")
import time
from ecpn_src.coupling_matrix import *
from ecpn_src.thermodynamic_quantities import *
from ecpn_src.solver import *
from ecpn_src.initial_state_heuristic import get_initial_state_ecpn
from ecpn_src.measurement import OBSERVER


def helper_sim(N=12, h0=0.5, J0=1.2, sigma=0., chi=1., dh=0.001,
t_min=0, t_max=1e6, Nt=10001, log_every_n = 10):

    seed= int(time.time())

    # -- PREPARE MODE-MODE COUPLING MATRIX
    J = set_connectivity_matrix(J0=J0, sigma=sigma, N=N, seed=seed)

    # -- PREPARE INITIAL MODE CONFIGURATION
    h_fun = lambda x: energy(J,chi,x)/N
    psi0, _ = get_initial_state_ecpn(N, h_fun, h0, dh=dh, seed=seed)

    # -- RUN SIMULATION AND MEAURE QUANTITIES OF INTEREST 
    obs = OBSERVER(N, J, chi, Nt, h0, every=log_every_n)
    _, cfg = evolve_DOP853(J, chi, psi0, t_min, t_max, Nt, obs.callback)

    # -- ADDITIONAL QUANTITIES OF INTEREST TO KEEP 
    res_dict = {
        'par_J0': J0,
        'par_chi': chi,
        'par_sigma': sigma,
        'par_dh': dh,
        'par_t_min' : t_min,
        'par_t_max' : t_max,
        'par_Nt': Nt,
        'log_every_n': log_every_n,
        'seed':seed,
        'cfg_ini': psi0,
        'cfg_fin': cfg
        }

    # -- SAVE RESULTS
    obs.save(path = './data_N%d/'%(N), f_name = 'obs_DOP853_ECPN_CONT_N%d_tmax%lf_Nt%d_h0%lf'%(N,t_max,Nt-1,h0), **res_dict)


if __name__=='__main__':

    sim_pars = {
        'J0': 1.2,
        'chi': 1.0,
        'sigma': 0.0,
        'dh': 0.001,
        't_min' : 0,
        't_max' : 5e3,
        'Nt': 201,
        'log_every_n': 10
    }

    N_val = int(sys.argv[1])
    h0_val = float(sys.argv[2])
    helper(N=N_val, h0=h0_val, **sim_pars)

