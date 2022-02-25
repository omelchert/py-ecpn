import numpy as np


def main(f_in, f_out):

    def fetch_cfg(f_name):
        data = np.load(f_name)
        N = data['N']
        h = data['h']
        m = data['m']
        cfg = data['cfg_fin']
        return N, h, m, cfg

    N, h_, m_, psi = fetch_cfg(f_in)
    np.savez_compressed(f_out, N=N, h=h_[-1], m=m_[-1], cfg_fin=psi)


main('./obs_DOP853_ECPN_J01.200_chi1.000_N16_tmax500000.000000_Nt100000_h0-0.500000.npz', 'cfg_01.npz')
main('./obs_DOP853_ECPN_J01.200_chi1.000_N16_tmax500000.000000_Nt100000_h00.900000.npz', 'cfg_02.npz')
