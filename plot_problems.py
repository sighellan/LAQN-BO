import datetime
import matplotlib.pyplot as plt
import numpy as np
import pickle

plt.rcParams["font.family"] = "Times New Roman"

def plot_problem(prob, ax, vmin, vmax, set_xlabel, set_ylabel, set_colorbar, ylims, xlims, col_bar_label):
    """
    Plot a single problem
    """
    _, poll, year, day_id = prob.identifier.split('-')
    prob_str = (datetime.datetime(int(year)-1, 12, 31) + datetime.timedelta(days=int(day_id))).strftime('%d %B %Y')
    print(prob_str)
    ax.set_title(prob_str)
    cb = ax.scatter(prob.domain[:,1], prob.domain[:,0], c=prob.labels, 
                    cmap=plt.get_cmap('Reds'), edgecolor='grey',
                    vmin=vmin, vmax=vmax) 
    if set_xlabel:
        ax.set_xlabel('East (km)')
    if set_ylabel:
        ax.set_ylabel('North (km)')
    if set_colorbar:
        colbar = plt.colorbar(cb, ax=ax, fraction=0.022, pad=0.02)
        colbar.set_label(col_bar_label, size=12)
        colbar.ax.tick_params(labelsize=12)
        
    # Align plots
    ax.set_aspect('equal')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylim(ylims)
    ax.set_xlim(xlims)
    
    # Adjust font labels
    ax.xaxis.label.set_fontsize(14)
    ax.yaxis.label.set_fontsize(14)
    ax.title.set_fontsize(14)
    [ii.set_fontsize(12) for ii in ax.get_xticklabels() ]
    [ii.set_fontsize(12) for ii in ax.get_yticklabels() ]

def load_problems(problem_choices):
    # Load problems and determine extrema of domains and labels chosen
    problems = []
    vmin = np.inf
    vmax = -np.inf
    south = np.inf
    north = -np.inf
    east = -np.inf
    west = np.inf
    for (year, prob_id) in problem_choices:
        problem_dir = 'data_sorted/%s_problems/not_preprocessed/' %year
        problem_file = 'laqn-al_notpre_NO2_Roadside_msfp_40_day-%s.p' %prob_id
        prob = pickle.load(open(problem_dir+problem_file, 'rb'))
        problems.append(prob)
        vmin = min(vmin, prob.minimum)
        vmax = max(vmax, prob.maximum)
        south = min(south, np.min(prob.domain[:,0]))
        north = max(north, np.max(prob.domain[:,0]))
        west = min(west, np.min(prob.domain[:,1]))
        east = max(east, np.max(prob.domain[:,1]))
    ylims = [south-3, north+3]
    xlims = [west-3, east+3]
    return problems, vmin, vmax, ylims, xlims

def generate_figure(problems, vmin, vmax, ylims, xlims, col_bar_label):
    # Plot problems
    aa = 0
    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    for prob in problems:
        plot_problem(prob, axes[aa//2, aa%2], vmin, vmax, 
                     set_xlabel=aa//2==1, set_ylabel=aa%2==0, 
                     set_colorbar=aa%2==1, ylims=ylims, xlims=xlims,
                     col_bar_label=col_bar_label)
        aa += 1

    figure_name = 'Paper_figure'
    figure_types = ['.svg', '.png']
    print('Producing figures:')
    for fig_type in figure_types:
        plt.savefig(figure_name+fig_type, bbox_inches='tight')
        print(figure_name+fig_type)
    
#############################################################################
# Choose problems to plot                                                   #
problem_choices = [(2015, '174'), (2015, '305'), (2016, '13'), (2016, '223')]
#############################################################################
problems, vmin, vmax, ylims, xlims = load_problems(problem_choices)

try:
    plt.rcParams["text.usetex"] = True
    col_bar_label = r'$\mathrm{NO}_2$ (ppb)'
    generate_figure(problems, vmin, vmax, ylims, xlims, col_bar_label)
except:
    plt.rcParams["text.usetex"] = False
    print('Trying without LaTeX')
    col_bar_label = r'$\mathrm{NO}_2$ (ppb)'
    generate_figure(problems, vmin, vmax, ylims, xlims, col_bar_label)
