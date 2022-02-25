import sys
import os
import time
import datetime
import numpy as np
from .thermodynamic_quantities import *


class OBSERVER():
    def __init__(self, N, J, chi, Nt, h0, every=10):
        # -- INITIALIZE CONTAINERS FOR QUANTITIES OF INTEREST
        self.start = datetime.datetime.now()
        self.Nt = Nt
        self.N = N
        self.J = J
        self.chi = chi
        self.t = []
        self.a = []
        self.h = []
        self.m_cplx = []
        self.cfgs = []
        self.every = every

        # -- PREPARE LOGFILE
        path = './logs_N%d/'%(N)
        os.makedirs(path,exist_ok=True)
        self.f = open(path+'N%d_h0%lf.log'%(N,h0),'w')
        print('# PID: %d'%(os.getpid()), file=self.f, flush=True)
        print('# (%) (t) (h) (m)', file=self.f, flush=True)


    def callback(self, it, t, y):
        N, J, chi, Nt, every = self.N, self.J, self.chi, self.Nt, self.every

        if it%every==0:

            # -- CURRENT VALUES OF QUANTITIES OF INTEREST
            a_curr = power(y)/N
            h_curr = energy(J,chi,y)/N
            m_cplx_curr = magnetization_cplx(y)

            # -- KEEP QUANTITITES OF INTEREST
            self.t.append(t)
            self.a.append(a_curr)
            self.h.append(h_curr)
            self.m_cplx.append(m_cplx_curr)
            self.cfgs.append(y)

            # -- WRITE DATA TO LOG-FILE
            print('%4.3lf %5.2lf %10.9lf %4.3lf'%(it/Nt, t, h_curr, np.abs(m_cplx_curr)), file=self.f, flush=True)


    def save(self, f_name='test', path='./data/',**kwargs):

        try:
            os.makedirs(path)
        except OSError:
            pass

        np.savez_compressed(path + f_name,
           N=self.N,
           chi=self.chi,
           J=self.J,
           t=np.asarray( self.t),
           a=np.asarray( self.a),
           h=np.asarray( self.h),
           m_cplx=np.asarray(self.m_cplx),
           cfgs=np.asarray(self.cfgs),
           proc_start=self.start,
           proc_end=datetime.datetime.now(),
           **kwargs
           )


