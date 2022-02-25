"""
Optimization heuristic for preparing mode configurations for specified optical
power per mode and energy density.

author: OM
date: 2022-01-XX
"""
import numpy as np


# --  NORMAL DISTRIBUTED RANDOM VARIABLES
_N = lambda mu, sigma: np.random.normal(mu, sigma)
# -- COMPLEX NORMAL DISTRIBUTED RANDOM VARIABLES
_CN = lambda mu, sigma: (_N(mu, sigma) + 1j * _N(mu, sigma)) / np.sqrt(2)
# -- UNIFORMLY RANDOM INTEGERS IN RANGE 0 ... N-1 
_U = lambda N: np.random.randint(N)


def get_initial_state_ecpn(N, h_fun, h0, a=1, dh=1e-4, seed=0, m_max=1000000):
    """prepare initial mode configuration

    Arguments:
        N (int): number of modes.
        h_fun (object): function returning the energy density.
        h0 (float): goal energy density.
        a (float): optica power per mode (default: 1).
        dh (float): control parameter (default: 1e-4).
        seed (int): seed for random number generators (default: 0).
        m_max (int): maximum number of iterations (default:1e6).

    Returns: (Psi)
        Psi (np.ndarray, 1-dim): mode configuration.
    """
    np.random.seed(seed)
    cost_fun = lambda x: np.abs(h_fun(x) - h0)
    h_curr_list = []

    psi0 = sample_random_state(N, a=a, seed=seed)
    fit_curr = cost_fun(psi0)

    m = 0
    while m < m_max and fit_curr > dh:

        tmp = modify_locally(np.copy(psi0), N)
        fit_tmp = cost_fun(tmp)

        if fit_tmp < fit_curr:
            psi0 = tmp
            fit_curr = fit_tmp

        h_curr = h_fun(psi0)
        h_curr_list.append(h_curr)
        m += 1

    return psi0, np.asarray(h_curr_list)


def modify_locally(tmp, N):
    """propose local modification

    Arguments:
        N (int): number of modes.
        tmp (np.ndarray, 1-dim): current mode configuration.

    Returns: (tmp)
        tmp (np.ndarray, 1-dim): modified mode configuration.
    """
    j = k = _U(N)
    while k == j:
        k = _U(N)
    chi_1 = _CN(0, 1)
    chi_2 = _CN(0, 1)
    xi = (np.abs(tmp[j]) ** 2 + np.abs(tmp[k]) ** 2) / (
        np.abs(chi_1) ** 2 + np.abs(chi_2) ** 2
    )
    tmp[j] = np.sqrt(xi) * chi_1
    tmp[k] = np.sqrt(xi) * chi_2
    return tmp


def sample_random_state(N, a=1, seed=0):
    """sample random mode configuration

    Arguments:
        N (int): number of modes.
        a (float): optica power per mode (default: 1).
        seed (int): seed for random number generators (default: 0).

    Returns: (Psi)
        Psi (np.ndarray, 1-dim): random mode configuration.
    """
    np.random.seed(seed)
    psi = np.random.normal(size=N) + 1j * np.random.normal(size=N)
    return np.sqrt(N) * psi / np.sqrt(np.sum(np.abs(psi) ** 2))


# EOF: initial_state_heuristic.py
