"""
Functions for analyzing raw data.

author: OM
date: 2022-01-XX
"""
import sys
import os
import numpy as np


def get_file_dict(path, ext='npz'):

    h0_val = lambda f: float(os.path.splitext(f)[0].split('_')[-1][2:])

    f_dict = {}
    for f in os.listdir(path):
        if f.endswith(ext):
            f_dict[h0_val(f)]=path+f

    return f_dict



def fetch_data_npz(f_name, key=None):
    """Read data from npz-file.

    Arguments:
        f_name (str): file name
        key (str): name of the entry to retrieve

    Returns: (x)
        x (object): data
    """
    data = np.load(f_name)
    return data[key]


def autocorrelation(t, m, dt):
    """autocorrelation function.

    Compute time-displaced autoforrelation function of a given model property
    using the definition given in Eq.~(3.21) of section "3.3.1 Autocorrelation
    functions" of Ref. [NB1999].

    Notes:
        -# Autocorrelation function is normalized so that C(dt=0) = 1
        -# time-displacement is adjusted to an integer multiple  of the time
        increment t[1]-t[0]

    References:
        [NB1999] M.E.J. Newma, G.T. Barkema, Monte Carlo Methods in Statistical
        Physics (Oxford University Press, 1999).

    Arguments:
        t (np.ndarray,1-dim): evenly-spaced measurememt times.
        m (np.ndarray,1-dim): model property.
        dt (float): displacement.

    Returns: (dt, C)
        dt (float): adjusted time displacement.
        C (float): normalized time-displaced autocorrelation.
    """
    dt_ = t[1]-t[0]
    n_t0 = int(dt/dt_)
    low_lim, up_lim = n_t0, (-n_t0+m.size)%(m.size+1)
    m_1_av = np.mean(m[:up_lim])
    m_2_av = np.mean(m[low_lim:])
    m_12_av = np.mean(m[low_lim:]*m[:up_lim])
    m_av = np.mean(m)
    m2_av = np.mean(m*m)
    C = m_12_av - m_1_av*m_2_av
    C0 = m2_av - m_av*m_av
    return n_t0*dt_, C/C0


def Binder_parameter(m):
    r"""Binder parameter.

    Computes the Binder parameter, i.e.\ the comulant ratio defined by Eq.
    (3.17) in Ref. [BH2010], that allows to estimate the transition point via
    finite-size-scaling.

    References:
        [BH2010]  K. Binder, D.W. Heermann, Monte Carlo Simulation in
        Statistical Physics (Springer, 2010).

    Arguments:
        m (np.ndarray, 1-dim): measured values of (scalar) magnetization.

    Returns: (b)
        b (float): Binder parameter.
    """
    s_4 = np.mean(np.abs(m)**4)
    s_22 = np.mean(np.abs(m)**2)**2
    return 1-s_4/s_22/3


def basic_stats(x):
    """Basic statistical summary measures.

    Compute mean value, standard deviation, and standard error of the mean
    for the supplied list of numerical values

    NOTE:
        -# so as to reduce roundoff errors, variance is computed via the
        corrected two-pass algorithm

    Arguments:
        x (np.ndarray, 1-dim): array data containing numerical values

    Returns: (av,sDev,sErr)
        av (float): mean value
        s_dev (float): standard deviation
        s_err (float): standard error of the mean
    """
    x = np.asarray(x)
    av=var=tiny=0.
    N=x.size
    for xi in x:
        av += xi
    av /= N
    for xi in x:
        dum   = xi - av
        tiny += dum
        var  += dum*dum
    var = (var - tiny*tiny/N)/(N-1)
    s_dev = np.sqrt(var)
    s_err = s_dev/np.sqrt(N)
    return av, s_dev, s_err


def bootstrap(x,fun,M=128):
    """Empirical bootstrap resampling of data.

    Estimates value of function 'fun' from original data
    stored in the list 'x'. Calculates corresponding error as
    standard deviation of the 'M' resampled bootstrap
    data sets.

    Arguments:
        x (np.ndarray, 1-dim): original data
        fun (object): estimator function for resampling procedure
        M (int): number of bootstrap samples (default: 128)

    Returns: (origEstim, resError)
        o_est (float): value of estimator function for original data
        res (float): corresponding error estimated via resampling
    """
    x = np.asarray(x)
    # -- ESTIMATE MEAN VALUE FROM ORIGINAL ARRAY
    o_est = fun(x)
    # -- RESAMPLE DATA FROM ORIGINAL ARRAY (WITH REPLACEMENT)
    h = np.asarray([fun(np.random.choice(x,x.size)) for m in range(M)])
    # -- ESTIMATE ERROR AS STD DEVIATION OF RESAMPLED VALUES
    err = basic_stats(h)[1]
    return o_est, err


