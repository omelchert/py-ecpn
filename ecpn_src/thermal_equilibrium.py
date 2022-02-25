"""
Data structures and functions for obtaining thermal equilibrium properties for
systems with weak nonlinearities.

author: OM
date: 2022-01-06
"""
import sys
import numpy as np
import scipy.optimize as so


def optical_temperature(N, A, E, e):
    r"""Determine optical temperature.

    Computes optical temperature using the method detailed in Ref. [P2019].

    Notes:
        - Notation used is that of Ref. [RFK2020].
        - Here (other than in [P2019]), the quantitites rho_i obey the order
          rho_0 >= rho_1 >= ... >= rho_N.
        - Here, root-finding is performed in the positive temperature domain,
          requiring E<0.

    References:
        [P2019] M. Parto, F.O. Wu, P.S. Jung, K. Makris, D.N. Christodouliedes,
        Thermodynamic conditions governing the optical temperature and chemical
        potential in nonlinear highly multimoded photonic systems, OL 22 (2019)
        3936, https://doi.org/10.1364/OL.44.003936

        [RFK2020] A. Ramos, L. Fernandez-Alcazar, T. Kottos, Optical Phase
        Transitions in Photonic Networks: a Spin-System Formulation, Phys. Rev.
        X, 10 (2020) 031024, https://doi.org/10.1103/PhysRevX.10.031024.

    Args:
        N (int): number of nodes (default: 8).
        A (float): total optical power.
        E (float): energy.
        e (np.ndarray, 1-dim): eigenfrequencies of linear part.

    Returns: (Tc)
        Tc (float): optial temperature.
    """

    if E>0:
      print("WARNING: E must be negative to determine optical temperature")
      print("Given E = %lf"%(E))
      sys.exit()

    # -- IMPLEMENTS VARIANT OF EQ. (2) OF REF. [P2019]
    rho = -(A*e - E)
    fun = lambda T:  np.sum(T/(N*T-rho)) - 1

    # -- RESTRICT ROOT-FINDING TO POSITIVE TEMPERATURE DOMAIN (OK FOR E<0) 
    T_min, T_max = rho[0]/N + 1e-1, 100.
    Tc = so.bisect(fun, T_min, T_max)

    return Tc


def chemical_potential(N,A,E,Tc):
    r"""Chemical potential.

    Computes chemical potential from equation of state, see Ref.  [P2019].

    References:
        [P2019] M. Parto, F.O. Wu, P.S. Jung, K. Makris, D.N. Christodouliedes,
        Thermodynamic conditions governing the optical temperature and chemical
        potential in nonlinear highly multimoded photonic systems, OL 22 (2019)
        3936, https://doi.org/10.1364/OL.44.003936

    Args:
        N (int): number of nodes (default: 8).
        A (float): total optical power.
        E (float): energy.
        Tc (float): optial temperature.

    Returns: (mu)
        mu (float): chemical potential.
    """
    return (E-N*Tc)/A


def average_optical_powers(e,Tc,mu):
    r"""Average optical powers in equilibrium.

    Calculates average modal occupancy from a Rayleigh-Jeans distribution for
    given optical temperature and chemical potential, see Ref. [P2009].

    References:
        [P2019] M. Parto, F.O. Wu, P.S. Jung, K. Makris, D.N. Christodouliedes,
        Thermodynamic conditions governing the optical temperature and chemical
        potential in nonlinear highly multimoded photonic systems, OL 22 (2019)
        3936, https://doi.org/10.1364/OL.44.003936

    Args:
        e (np.ndarray, 1-dim): eigenfrequencies of linear part.
        Tc (float): optial temperature.
        mu (float): chemical potential.

    Returns: (n_av)
        n_av (np.array, 1-dim): average model occupancy in thermal equilibrium.
    """
    return Tc/(e-mu)


def thermal_equilibrium_properties(N,A,E,e):
    Tc = optical_temperature(N,A,E,e)
    mu = chemical_potential(N,A,E,Tc)
    n_av = average_optical_powers(e,Tc,mu)
    return Tc, mu, n_av
