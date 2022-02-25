"""
Data structures and functions for setting up and analyzing connectivity matrix

author: OM
date: 2022-01-04
"""
import numpy as np
import numpy.linalg as nlin


def set_connectivity_matrix_ECPN_1DLR(J0=1., N=12, r=0.2):
    r"""connectivity matrix for 1DLR ECPN.

    Sets up connectivity matrix for equal-coupling photonic networks with
    one-dimensional long-range couplings.

    Args:
        J0 (float): uniform coupling strength (default: 1.0).
        N (int): number of nodes (default: 8).
        r (float): relative interaction range (default: 0.2).

    Returns: (J)
        J (np.ndarray, 2-dim): symmetric connectivity matrix.
    """
    L = int(r*N)
    J = np.zeros((N,N))
    for i in range(N):
      for j in range(N):
          if j!=i:
             if np.abs(i-j)<=L or np.abs(j-i)<=L:
                 J[i,j] = 1.
             if np.abs(i+N-j)<=L or (j+N-i)<=L:
                 J[i,j] = 1.
    return J/2/L


def set_connectivity_matrix(J0=1., sigma=1., N=8, seed=0):
    r"""Set up connectivity matrix.

    Sets up connectivity matrix as specified in Eq. (15) of Ref. [RFK2020].
    The resulting matrix J is symmetric and has zeros along its main diagonal.

    Notes:
        - Special case sigma = 0: Equal coupling photonic network.
        - Special case J0 = 0: Extreme disorder case with frustration.

    References:
        [RFK2020] A. Ramos, L. Fernandez-Alcazar, T. Kottos, Optical Phase
        Transitions in Photonic Networks: a Spin-System Formulation, Phys. Rev.
        X, 10 (2020) 031024, https://doi.org/10.1103/PhysRevX.10.031024.

    Args:
        J0 (float): uniform coupling strength (default: 1.0).
        sigma (float): disorder strength parameter (default: 1.0).
        N (int): number of nodes (default: 8).
        seed (int): disorder seedd (default: 0).

    Returns: (J)
        J (np.ndarray, 2-dim): symmetric connectivity matrix.
    """
    np.random.seed(seed)
    # ... GET UPPER TRIANGULAR MATRIX (WITH ZEROS ALONG DIAGONAL) 
    tmp = np.triu(J0/N + sigma/np.sqrt(N)*np.random.normal(size=(N,N)), k=1)
    # ... COMPOSE SYMMETRIC CONNECTIVITY MATRIX WITH J_KL = J_LK, J_KK = 0
    J = tmp + tmp.T
    return J


def analyze_spectral_properties(J):
    r"""Analyze spectral properties of connectivity matrix.

    Computes eigenfrequencies and eigenvectors of a given connectivity matrix.

    Notes:
        - the eigenvectors are the supermodes, i.e. the eigenmodes of the
          entire system.
        - these supermodes form a complete basis, used to expand a given  field
          configuration.
        - eigenvalues of the connectivity matrix are the Hamiltonian
          eigenfrequencies times -1. If -J is provided insteadd of J, the
          eigenfrequencies of the hamiltonian are obtained directly.
        - OBEY THE INDEX ORDER:
            eigenfreuency "0" is given by e[0]
            eigenmode "0" is given by v[:,0]

    Args:
        J (np.ndarray, 2-dim): connectivity matrix.

    Returns: (e, v)
        e (np.ndarray, 1-dim): eigenvalues.
        v (np.ndarray, 2-dim): eigenvectors.
    """
    e,v = nlin.eigh(J)
    return e, v

