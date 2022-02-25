import sys; sys.path.append("../../")
import numpy as np
import numpy.fft as nfft
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec


# -- FFT ABREVIATIONS
FT = nfft.ifft
IFT = nfft.fft
FTFREQ = nfft.fftfreq
SHIFT  = nfft.fftshift


def save_fig(fig_name='test', fig_format='png'):
    if fig_format == 'png':
        plt.savefig(fig_name+'.png', format='png', dpi=600)
    elif fig_format == 'pdf':
        plt.savefig(fig_name+'.pdf', format='pdf', dpi=600)
    elif fig_format == 'svg':
        plt.savefig(fig_name+'.svg', format='svg', dpi=600)
    else:
        plt.show()


def set_style(fig_width=3.25, aspect_ratio = 0.6):

    fig_height = aspect_ratio*fig_width

    params = {
        'figure.figsize': (fig_width,fig_height),
        'legend.fontsize': 5,
        'legend.frameon': False,
        'axes.labelsize': 6,
        'axes.linewidth': 0.75,
        'xtick.labelsize' :6,
        'ytick.labelsize': 6,
        'lines.linewidth': 0.75,
        'lines.markersize': 1.,
        'mathtext.fontset': 'stixsans',
        'mathtext.rm': 'serif',
        'mathtext.bf': 'serif:bold',
        'mathtext.it': 'serif:italic',
        'mathtext.sf': 'sans\\-serif',
        'font.size':  6,
        'font.family': 'serif',
        'font.serif': "Helvetica",
    }
    mpl.rcParams.update(params)

def set_style_PR(fig_width=3.25, aspect_ratio = 0.6):
    fig_height = aspect_ratio*fig_width
    params = {
        'figure.figsize': (fig_width,fig_height),
        'legend.fontsize': 6,
        'legend.frameon': False,
        'axes.labelsize': 7,
        'axes.linewidth': 1.,
        'axes.linewidth': 0.8,
        'lines.linewidth': 0.75,
        'lines.markersize': 1.5,
        'xtick.labelsize' :7,
        'ytick.labelsize': 7,
        'mathtext.fontset': 'stixsans',
        'mathtext.rm': 'serif',
        'mathtext.bf': 'serif:bold',
        'mathtext.it': 'serif:italic',
        'mathtext.sf': 'sans\\-serif',
        'font.size':  7,
        'font.family': 'serif',
        'font.serif': "Helvetica",
    }
    mpl.rcParams.update(params)



def figure_vid(o_name='fig', o_format='png'):

    def subfig_label(ax, label):
        pos = ax.get_position()
        fig.text(
            pos.x0,
            pos.y1,
            label,
            fontsize=7,
            color="white",
            backgroundcolor="k",
            bbox=dict(facecolor="k", edgecolor="none", boxstyle="square,pad=0.1"),
            verticalalignment="top",
            horizontalalignment="left",
        )

    def properties_label(ax, a, h, m):
        pos = ax.get_position()
        fig.text(
            pos.x0+0.02,
            pos.y0+0.02,
            "Average power: $a=%4.3lf$\nEnergy density: $h=%4.3lf$\nMagnetization: $m=%lf$"%(a,h,m),
            color="k",
            fontsize=9,
            backgroundcolor="white",
            verticalalignment="bottom",
            horizontalalignment="left",
        )

    aspect_ratio = 0.45
    set_style_PR(3.4, aspect_ratio)
    fig = plt.figure()
    plt.subplots_adjust(left = 0.01, bottom = 0.07, right = 1., top = 0.98)
    gs00 = GridSpec(nrows = 1, ncols = 1)

    gsA = GridSpecFromSubplotSpec(1, 2, subplot_spec=gs00[0,0], wspace=0.4, hspace=0.)
    ax1 = fig.add_subplot(gsA[0, 0])
    ax2 = fig.add_subplot(gsA[0, 1])
    sf2 = [ax1, ax2]


    def properties_label(ax, h, m, loc='left'):
        pos = ax.get_position()

        if loc=='left':
            fig.text(
                pos.x1-0.5*(pos.x1-pos.x0),
                pos.y0-0.01,
                "$h=%3.2lf$, $m=%3.2lf$"%(h,m),
                color="k",
                fontsize=6,
                backgroundcolor="white",
                verticalalignment="top",
                horizontalalignment="center",
                zorder=10
            )

        if loc=='right':
            fig.text(
                pos.x1-0.5*(pos.x1-pos.x0),
                pos.y0-0.01,
                "$h=%3.2lf$, $m=%3.2lf$"%(h,m),
                color="k",
                fontsize=6,
                backgroundcolor="white",
                verticalalignment="top",
                horizontalalignment="center",
                zorder=10
            )


    def fetch_cfg(f_name):
        data = np.load(f_name)
        N = data['N']
        h = data['h']
        m = data['m']
        cfg = data['cfg_fin']
        return N, h, m, cfg

    cols = ['k', 'gray', '#3776ab', '#ab7f37', '#ab4537']

    mv = 1.2
    x_lim = (-mv,mv)
    x_ticks = (-mv,0,mv)
    y_lim = (-mv,mv)
    y_ticks = (-mv,0,mv)


    # ... EXAMPLE FERROMAGNETIC DOMAIN

    ax = sf2[0]
    # ... RESCALE Y-AXIS
    pos = ax.get_position()
    dx = (pos.x1 - pos.x0)
    dy = dx/aspect_ratio
    ax.set_position( [pos.x0, pos.y0, dx, dy]  )

    #N, h, m, psi = fetch_cfg('./obs_DOP853_ECPN_J01.200_chi1.000_N16_tmax500000.000000_Nt100000_h0-0.500000.npz')
    #N, h, m, psi = fetch_cfg('./obs_DOP853_ECPN_J01.200_chi1.000_N16_tmax500000.000000_Nt100000_h0-0.421053.npz')
    N, h, m, psi = fetch_cfg('cfg_01.npz')

    psi=-psi

    phi = np.linspace(0,2*np.pi, N, endpoint=False)
    x, y = np.cos(phi), np.sin(phi)

    for i in range(N-1):
       for j in range(i+1,N):
         s=0.8
         ax.plot([s*x[i],s*x[j]], [s*y[i],s*y[j]] , color='#3776ab', lw=0.7  , zorder=0)

    r0 = 0.66*np.pi/N
    for sId in range(N):
       dx, dy = np.real(psi[sId])*r0, np.imag(psi[sId])*r0
       ax.arrow( x[sId], y[sId], dx, dy , length_includes_head=True, lw=1., head_width=0.02, color='k')
       ax.add_patch(plt.Circle((x[sId], y[sId]), r0, color=cols[1], alpha=0.2, linewidth=0))


    ax.tick_params(axis="x", direction='out', length=2.5, pad=1, top=False, bottom=False, labelbottom=False)

    ax.tick_params(axis="y", direction='out', length=2.5, pad=1,left=False, labelleft=False)

    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    properties_label(ax, h, m, loc='left')

    subfig_label(ax, '(a)')



    # -- LEGEND FOR SPINS


    ax_l = ax.inset_axes([1.12,0.05,0.2,0.2], zorder=15)

    ax_l.set_xlim((-1.,1.))
    ax_l.set_ylim((-1.,1.))

    ax_l.add_patch(plt.Circle((0, 0), 1, color=cols[1], alpha=0.2, linewidth=0))

    dx, dy = 0.9,0.9
    ax_l.arrow( 0,0, dx, dy , length_includes_head=True, lw=1., head_width=0.1, color='k')

    ax_l.tick_params(axis="y", direction='out', length=2.5, pad=1, labelsize=6)
    ax_l.tick_params(axis="x", direction='out', length=2.5, pad=1, labelsize=6)


    ax_l.spines['bottom'].set_position(('outward', 4))
    ax_l.spines['left'].set_position(('outward', 4))
    ax_l.spines['top'].set_color('none')
    ax_l.spines['right'].set_color('none')

    pos = ax_l.get_position()
    fig.text(
        pos.x0-0.01,
        pos.y1+0.10,
        "Soft-spin:",
        color="k",
        fontsize=5,
        verticalalignment="bottom",
        horizontalalignment="left",
        zorder=10
    )
    fig.text(
        pos.x0-0.0,
        pos.y1+0.03,
        "$\mathsf{Im}[\psi]$",
        color="k",
        fontsize=6,
        verticalalignment="bottom",
        horizontalalignment="right",
        zorder=10
    )
    fig.text(
        pos.x1+0.01,
        pos.y0-0.03,
        "$\mathsf{Re}[\psi]$",
        color="k",
        fontsize=6,
        verticalalignment="top",
        horizontalalignment="left",
        zorder=10
    )

    #


    ax = sf2[1]
    # ... RESCALE Y-AXIS
    pos = ax.get_position()
    dx = (pos.x1 - pos.x0)
    dy = dx/aspect_ratio
    ax.set_position( [pos.x0, pos.y0, dx, dy]  )

    #N, h, m, psi = fetch_cfg('./obs_DOP853_ECPN_J01.200_chi1.000_N16_tmax500000.000000_Nt100000_h00.900000.npz')
    N, h, m, psi = fetch_cfg('cfg_02.npz')

    phi = np.linspace(0,2*np.pi, N, endpoint=False)
    x, y = np.cos(phi), np.sin(phi)

    for i in range(N-1):
       for j in range(i+1,N):
         s=0.8
         ax.plot([s*x[i],s*x[j]], [s*y[i],s*y[j]] , color='#3776ab', lw=0.7  , zorder=0)

    r0 = 0.66*np.pi/N
    for sId in range(N):
       dx, dy = np.real(psi[sId])*r0, np.imag(psi[sId])*r0
       ax.arrow( x[sId], y[sId], dx, dy , length_includes_head=True, lw=1., head_width=0.02, color='k')
       ax.add_patch(plt.Circle((x[sId], y[sId]), r0, color=cols[1], alpha=0.2, linewidth=0))


    ax.tick_params(axis="x", direction='out', length=2.5, pad=1, top=False, bottom=False, labelbottom=False)

    ax.tick_params(axis="y", direction='out', length=2.5, pad=1,left=False, labelleft=False)

    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    properties_label(ax, h, m, loc='right')

    subfig_label(ax, '(b)')

    save_fig(fig_name=o_name, fig_format=o_format )


def main():

    figure_vid(o_name='fig_01', o_format='png')

main()




