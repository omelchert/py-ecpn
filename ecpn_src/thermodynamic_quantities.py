"""
Functions for analyzing field configurations.

author: OM
date: 2022-01-04
"""
import numpy as np
import numpy.linalg as nlin


def energy(J, chi, psi):
    r"""Extensive energy of mode configuration.

    Evaluates energy functional for a given mode condfiguration according to
    Eq. (4) of Ref. [RFK2020].

    References:
        [RFK2020] A. Ramos, L. Fernandez-Alcazar, T. Kottos, Optical Phase
        Transitions in Photonic Networks: a Spin-System Formulation, Phys. Rev.
        X, 10 (2020) 031024, https://doi.org/10.1103/PhysRevX.10.031024.

    Args:
        J (np.ndarray, 2-dim): coupling matrix.
        chi (float): nonlinear parameter.
        psi (np.ndarray, 1-dim): mode configuration.

    Returns: (E)
        E (float): energy of the mode configuration.
    """
    h = np.dot(J,np.conj(psi))
    E_L = -np.sum(h*psi)
    E_N = 0.5*chi*np.sum(np.abs(psi)**4)
    return np.real(E_L + E_N)


def power(psi):
    r"""Extensive power of mode configuration.

    Evaluates optical power functional for a given mode condfiguration
    according to Eq. (5) of Ref. [RFK2020].

    References:
        [RFK2020] A. Ramos, L. Fernandez-Alcazar, T. Kottos, Optical Phase
        Transitions in Photonic Networks: a Spin-System Formulation, Phys. Rev.
        X, 10 (2020) 031024, https://doi.org/10.1103/PhysRevX.10.031024.

    Args:
        psi (np.ndarray, 1-dim): mode configuration.

    Returns: (A)
        A (float): optical power of the mode configuration.
    """
    return np.sum(np.abs(psi)**2)


def amplitudes_from_field(psi, sm):
    r"""Convert modes to supermode amplitudes.

    Note:
    -  supermodes are computed by function analyze_spectral_properties in
       module coupling_matrix.

    Args:
        psi (np.ndarray, 1-dim): mode field configuration.
        sm (np.ndarray, 2-dim): data structure holding the supermodes.

    Returns: (C)
        C (np.ndarray, 1-dim): complex-valued amplitudes of supermodes.
    """
    return np.dot(psi, sm)


def field_from_amplitudes(C, sm):
    r"""Recunstruct modes from supermode amplitudes.

    Note:
    -  supermodes are computed by function analyze_spectral_properties in
       module coupling_matrix.

    Args:
        C (np.ndarray, 1-dim):  complex-valued supermode amplitudes.
        sm (np.ndarray, 2-dim): data structure holding the supermodes.

    Returns: (psi)
        psi (np.ndarray, 1-dim): mode field.
    """
    return np.dot(sm,C)


def magnetization_cplx(psi):
    r"""Complex-valued magnetization.

    Energy dependent complex-valued reduced soft-spin magnetization, analogous
    to the (canonical ensemble) temperature-dependent reduced magnetization of
    classical multi-component spins [N2007].

    References:
        [N2007] U. Nowak, Classical Spin Models, Micromagnetism, Wiley (2007)

    Args:
        psi (np.ndarray, 1-dim): configuration of photonic soft-spins.

    Returns: (m_cplx)
        m_cplx (complex): complex-valued reduced magnetization.
    """
    return np.sum(psi)/psi.size


def magnetization(psi):
    r"""Real-valued magnetization.

    Energy dependent real-valued reduced soft-spin magnetization,
    given by the magnitude of the complex-valued magnetization.

    Notes:
        - In classical spin models is is not uncommon to also use this absolute
          value for finite-size scaling. This will overestimate the value of
          the magnetization in the disordered phase and close to the critical
          point in the ordered phase. The associated suszeptibilities do not
          suffer from this. See Ref. [NB1999]

    References:
        [NB1999] M.E.J. Newman, G.T. Barkema, Monte Carlo Methods in
        Statistical Physics (Oxford University Press, 1999).

    Args:
        psi (np.ndarray, 1-dim): configuration of photonic soft-spins.

    Returns: (m)
        m (float): real-valued reduced magnetization.
    """
    return np.abs(np.sum(psi))/psi.size

