import sys; sys.path.append("../../")
import os
import datetime
import numpy as np
import scipy
import scipy.stats
import scipy.optimize
from ecpn_src.data_analysis import basic_stats, bootstrap, fetch_data_npz, get_file_dict, Binder_parameter


def main_postprocessing(f_name, t_eq=0):

    # -- READ IN RAW DATA
    N = fetch_data_npz(f_name, "N")
    J = fetch_data_npz(f_name, "J")
    chi = fetch_data_npz(f_name, "par_chi")
    t = fetch_data_npz(f_name, "t")
    h = fetch_data_npz(f_name, "h")
    m_cplx = fetch_data_npz(f_name, "m_cplx")
    cfg = fetch_data_npz(f_name, "cfgs")

    # -- IGNORE EQUILIBRATION PHASE
    m_cplx = m_cplx[t>t_eq]
    m = np.abs(m_cplx)
    cfg = cfg[t > t_eq]
    t_ = t[t > t_eq]

    # -- RATE OF CHANGE OF SPINS
    _NMPN_RHS = lambda dt, x: -1j * (-np.dot(J, x) + chi * np.abs(x) ** 2 * x)

    # -- ANALYZE SPIN CONFIGURATIONS
    theta_list = []
    msd_list = []
    for i in range(t_.size):
        y = cfg[i]
        a_k = np.angle(y)

        # -- RATE OF CHANGE OF SPIN POSITION
        ds = _NMPN_RHS(0, y)
        ds_x, ds_y = np.real(ds), np.imag(ds)
        # -- COMPONENT IN ANGULAR DIRECTION
        ds_phi = -ds_x * np.sin(a_k) + ds_y * np.cos(a_k)
        # -- COMPONENT IN RADIAL DIRECTION
        ds_r = ds_x * np.cos(a_k) + ds_y * np.sin(a_k)

        # -- TOTAL ANGULAR VELOCITY
        dphi = np.sum(ds_phi) / N
        # -- MEAN SQUARED DEVIATION OF INDIVIDUAL SPIN ANGULAR VELOCITIES
        msd_phi = np.sum((ds_phi - dphi) ** 2) / N

        theta_list.append((a_k - np.angle(m_cplx[i]) + np.pi) % (2 * np.pi) - np.pi)
        msd_list.append(msd_phi)

    # -- TIME-AVERAGED MAGNETIZATION
    m_av, m_sDev, m_sErr = basic_stats(m)
    # -- FINITE SIZE SUSCEPTIBILITY
    chi, chi_err = bootstrap(m, lambda x: N * np.var(x), M=32)

    # -- TIME AVERAGED MSE OF ANGULAR VELOCITIES
    mse_av, mse_sDev, mse_sErr = basic_stats(msd_list)

    # -- SUMMARY OF ANGULAR DISTRIBUTION
    theta = np.concatenate(np.asarray(theta_list), axis=-1)
    theta_av = np.mean(theta)
    theta_var, theta_var_err = bootstrap(theta, lambda x: np.var(x), M=32)

    print( h[0], mse_av, mse_sErr, m_av, m_sErr, chi, chi_err, theta_av, theta_var, theta_var_err)


def main_wrapper():
    path = sys.argv[1]
    t_eq = float(sys.argv[2])
    f_dict = get_file_dict(path)

    print("# ANALYSIS SCRIPT: %s" % (sys.argv[0]))
    print("# PATH TO RAW DATA: %s" % (path))
    print("# EQUILIBRATION TIME: t_eq = %lf" % (t_eq))
    print("# TIMESTAMP: %s" % (datetime.datetime.now()))
    print("# (h) (Ts) (Ts_err) (m_av) (m_serr) (chi) (chi_err) (theta_av) (theta_var) (theta_var_err)")
    for h0, f_name in sorted(f_dict.items()):
        main_postprocessing(f_name, t_eq=t_eq)


if __name__ == "__main__":
    main_wrapper()
