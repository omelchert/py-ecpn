"""
Contains functions mplementing different numerical integration schemes.

AUTHOR: O. Melchert
DATE: 2020-01-17
"""
import sys
import numpy as np
from scipy.integrate import complex_ode


def evolve_DOP853(J, chi, psi, t_min, t_max, Nt, callback_fun):
    t, dt = np.linspace(t_min, t_max, Nt, endpoint=True, retstep=True)

    #J0 = J[1,2]
    #def _NMPN_RHS(dt, x):
    #    M = np.sum(x)
    #    return -1j*(-J0*(M-x) + chi*np.abs(x)**2*x)

    # -- EQUATIONS OF MOTION FOR NONLINEAR MULTIMODE PHOTONIC NETWORK (NMPN) 
    _NMPN_RHS = lambda dt, x: -1j*(-np.dot(J,x) + chi*np.abs(x)**2*x)

    solver = complex_ode(_NMPN_RHS)
    solver.set_integrator('dop853', rtol=1e-10)
    solver.set_initial_value(psi, t.min())

    it=0
    while solver.successful() and solver.t < t.max():
        solver.integrate(solver.t+dt)
        callback_fun(it, solver.t, solver.y)
        it += 1

    return solver.t, solver.y

