import sys; sys.path.append("../../")
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec


def save_fig(fig_name='test', fig_format='png'):
    if fig_format == 'png':
        plt.savefig(fig_name+'.png', format='png', dpi=600)
    elif fig_format == 'pdf':
        plt.savefig(fig_name+'.pdf', format='pdf', dpi=600)
    elif fig_format == 'svg':
        plt.savefig(fig_name+'.svg', format='svg', dpi=600)
    else:
        plt.show()


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


def figure_02(o_name='fig', o_format='png'):

    # -- FIGURE LAYOUT --------------------------------------------------------

    set_style_PR(3.4, 0.45)
    fig = plt.figure()
    plt.subplots_adjust(left = 0.1, bottom = 0.18, right = 0.98, top = 0.97)
    gs00 = GridSpec(nrows = 1, ncols = 1)

    gsA = GridSpecFromSubplotSpec(1, 2, subplot_spec=gs00[0,0], wspace=0.35, hspace=0.1)
    ax1 = fig.add_subplot(gsA[0, 0])
    ax2 = fig.add_subplot(gsA[0, 1])


    # -- CONVENTIENT FUNCTIONS AND OTHER DEFINITIONS --------------------------

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

    def fetch_data(f_name, col=0):
        dat = np.loadtxt(f_name)
        return dat[:,col]

    markers = ['o', 's', '>', '<', 'D']
    n_cols = len(markers)
    cols = plt.cm.Blues(np.linspace(0.5,1.,n_cols))


    # -- DATA CURVES FOR SUBFIGURES (A,B) -------------------------------------

    h = fetch_data('../pp_data_analysis/res_N8.dat',col=0)
    m = fetch_data('../pp_data_analysis/res_N8.dat',col=3)
    chi = fetch_data('../pp_data_analysis/res_N8.dat',col=5)
    ax1.plot(h, m, color=cols[0], marker=markers[0], label=r'$N=8$')
    ax2.plot(h, chi, color=cols[0], marker=markers[0], label=r'$N=8$')

    h = fetch_data('../pp_data_analysis/res_N16.dat',col=0)
    m = fetch_data('../pp_data_analysis/res_N16.dat',col=3)
    chi = fetch_data('../pp_data_analysis/res_N16.dat',col=5)
    ax1.plot(h, m, color=cols[1], marker=markers[1], label=r'$N=16$')
    ax2.plot(h, chi, color=cols[1], marker=markers[1], label=r'$N=16$')

    h = fetch_data('../pp_data_analysis/res_N32.dat',col=0)
    m = fetch_data('../pp_data_analysis/res_N32.dat',col=3)
    chi = fetch_data('../pp_data_analysis/res_N32.dat',col=5)
    ax1.plot(h, m, color=cols[2], marker=markers[2], label=r'$N=32$')
    ax2.plot(h, chi, color=cols[2], marker=markers[2], label=r'$N=32$')

    h = fetch_data('../pp_data_analysis/res_N64.dat',col=0)
    m = fetch_data('../pp_data_analysis/res_N64.dat',col=3)
    chi = fetch_data('../pp_data_analysis/res_N64.dat',col=5)
    ax1.plot(h, m, color=cols[3], marker=markers[3], label=r'$N=64$')
    ax2.plot(h, chi, color=cols[3], marker=markers[3], label=r'$N=64$')


    # -- AXES DETAILS SUBFIGURE (A) -------------------------------------------

    x_lim = (0.6,0.9)
    x_ticks = (0.6,0.7,0.8,0.9)
    ax1.set_xlim(x_lim)
    ax1.set_xticks(x_ticks)
    ax1.tick_params(axis="x", length=2.5, pad=1, top=False)
    ax1.set_xlabel(r"Energy density $h$",labelpad=1)

    y_lim = (0,0.5)
    y_ticks = (0,0.1,0.2,0.3,0.4,0.5)
    ax1.set_ylim(y_lim)
    ax1.set_yticks(y_ticks)
    ax1.tick_params(axis="y", length=2.0, pad=1)
    ax1.set_ylabel(r"Order parameter $\langle m \rangle$")

    legend = ax1.legend(
        ncol=1,
        handlelength=1.,
        borderpad=0.1,
        handletextpad=0.25,
        columnspacing=1.0,
        labelspacing=0.2,
        fontsize=6.0,
        title_fontsize=5.0,
        labelcolor="k",
        loc="upper right",
    )

    subfig_label(ax1, '(c)')


    # -- AXES DETAILS SUBFIGURE (B) -------------------------------------------

    ax2.set_xlim(x_lim)
    ax2.set_xticks(x_ticks)
    ax2.tick_params(axis="x", length=2.5, pad=1, top=False)
    ax2.set_xlabel(r"Energy density $h$",labelpad=1)

    y_lim = (0,0.35)
    y_ticks = (0,0.1,0.2,0.3)
    ax2.set_ylim(y_lim)
    ax2.set_yticks(y_ticks)
    ax2.tick_params(axis="y", length=2.0, pad=1)
    ax2.set_ylabel(r"Fluctuations $N \left( \langle m^2\rangle - \langle m\rangle^2 \right)$")

    legend = ax2.legend(
        ncol=1,
        handlelength=1.,
        borderpad=0.1,
        handletextpad=0.25,
        columnspacing=1.0,
        labelspacing=0.2,
        fontsize=6.0,
        title_fontsize=5.0,
        labelcolor="k",
        loc="lower right",
    )

    subfig_label(ax2, '(d)')


    # -- SAVE FIGURE ---------------------------------------------------------- 
    save_fig(fig_name=o_name, fig_format=o_format )


def main():
    figure_02(o_name='fig_02')


main()
