# Author: Arun Mathew
# Created: 10-11-2022

# Fx_Plotter: plot f(x)'s with a common x-axis.
# MultiFx_Plotter: plots f(x) with seperated x-axis.

# comments:

#############################################################
# Required libraries
import matplotlib.pyplot as plt
#from labellines import labelLines
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

class Plot_Function:

    #############################################################
    # plot multiple functions with common x-axis
    def Single_Xaxis_Plotter(self, fig, x_datapoints, functions, axislabels, axislimit):

        ax = fig.add_subplot()
        for func in functions:
            ax.plot(x_datapoints, func, label=func[1], linewidth=0.6)
        ax.set(xlabel = axislabels[0], ylabel = axislabels[1])
        if(axislimit == []):
            pass
        else:
            ax.set_xlim([axislimit[0][0], axislimit[0][1]])
            ax.set_ylim([axislimit[1][0], axislimit[1][1]])

        plt.tight_layout()
        #plt.legend()
        #xvals = [0.8, 0.55, 0.22, 0.104, 0.045]
        #labelLines(ax.get_lines(), align=False, xvals=xvals, color="k")
        #labelLines(ax.get_lines(), align=True, fontsize=8, color="k")
        #labelLines(plt.gca().get_lines(), drop_label=True, zorder=2.0, ha='left')
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(axis="both", direction="in", which="both", bottom=True, top=True,
                       left=True, right=True, length=3)

        return fig

    #############################################################
    # plot multiple functions with respect to the associated x points
    def Fx_Plotter(self, fig, functions, axis_labels, axis_limit):

        ax = fig.add_subplot()
        for func in functions:
            ax.plot(func[0], func[1], label=func[2], linewidth=1.0)
            ax.legend()
        ax.set(xlabel = axis_labels[0], ylabel = axis_labels[1])
        ax.set_xlim([axis_limit[0][0], axis_limit[0][1]])
        ax.set_ylim([axis_limit[1][0], axis_limit[1][1]])
        plt.tight_layout()
        ax.legend(bbox_to_anchor =(1.0, 0.95), prop = {'size' : 8})

        return fig
