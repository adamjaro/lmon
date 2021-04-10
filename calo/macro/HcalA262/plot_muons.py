#!/usr/bin/python

from pandas import DataFrame, read_hdf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import norm
from scipy.optimize import curve_fit
import numpy as np
import collections

import os
from math import ceil, log10

#_____________________________________________________________________________
def main():

    iplot = 0
    funclist = []
    funclist.append( run_signal ) # 0

    funclist[iplot]()

#_____________________________________________________________________________
def run_signal():

    beam = [3, 5, 7, 10, 20, 30, 50, 75]
    #beam = [10]

    #81./16 = 5.0625

    infile = ["/home/jaroslav/sim/hcal/data/hcal2cx6/HCal_en", ".h5"]

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    had_em = []
    for i in beam:

        inp = read_hdf(infile[0]+str(i)+infile[1])

        mean_em = inp["hcal_edep_EM"].mean()
        mean_had = inp["hcal_edep_HAD"].mean()

        #print i, mean_em, mean_had, mean_had/mean_em

        #mean_em, sigma_em = gfit(inp, "hcal_edep_EM")
        #mean_had, sigma_had = gfit(inp, "hcal_edep_HAD")

        had_em.append(mean_had/mean_em)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_ylim([4.5, 6])

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    ax.set_xlabel("Incident energy $E$ (GeV)")
    #ax.set_ylabel("$\mu_{\mathrm{HAD}}/\mu_{\mathrm{EM}}$")
    ax.set_ylabel(r"$\frac{\mu_{\mathrm{HAD}}}{\mu_{\mathrm{EM}}}$", rotation=0)

    ax.set_xscale("log")
    plt.xticks(beam, [str(i) for i in beam])

    set_axes_color(ax, col)
    set_grid(plt, col)

    x = np.linspace(beam[0], beam[-1], 300)
    plt.plot(x, [5.06 for i in x], "k--", color="red")

    plt.plot(beam, had_em, "o", color="blue")

    leg = legend()
    leg.add_entry(leg_lin("red", "--"), "81/16 = 5.06")
    leg.add_entry(leg_dot(fig, "blue"), "FTFP\_BERT\_HP, 10.5.p01")
    leg.draw(ax)

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#run_signal

#_____________________________________________________________________________
def gfit(inp, sec_name):

    #Gaussian fit at a given energy

    sum_edep = inp[sec_name]

    nbins = 60

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)

    #data plot
    hx = plt.hist(sum_edep, bins = nbins, color = "lime", density = True, label = "edep")

    #bin centers for the fit
    centers = (0.5*(hx[1][1:]+hx[1][:-1]))

    #pass1, fit over the full range
    fit_data = DataFrame({"E": centers, "density": hx[0]})
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), fit_data["E"], fit_data["density"])

    #print "pass1:", pars[0], pars[1]

    #pass2, fit in +/- 2*sigma range
    fitran = [pars[0] - 2.*pars[1], pars[0] + 2.*pars[1]] # fit range at 2*sigma
    fit_data = fit_data[ fit_data["E"].between(fitran[0], fitran[1], inclusive=False) ] # select the data to the range
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), fit_data["E"], fit_data["density"])

    #print "pass2:", pars[0], pars[1]

    #fit function
    x = np.linspace(fitran[0], fitran[1], 300)
    y = norm.pdf(x, pars[0], pars[1])

    plt.plot(x, y, "k-", label="norm", color="red")

    ax.set_xlabel("Calorimeter signal (GeV)")
    ax.set_ylabel("Counts / {0:.3f} GeV".format((plt.xlim()[1]-plt.xlim()[0])/nbins))

    #ax.set_title(r"$\text{"+infile+"}$")
    #print infile

    set_grid(plt, col)

    #mean_str = "{0:.4f} \pm {1:.4f}".format(pars[0], np.sqrt(cov[0,0]))
    #sigma_str = "{0:.4f} \pm {1:.4f}".format(pars[1], np.sqrt(cov[1,1]))
    #res = pars[1]/pars[0]
    #res_str = "{0:.4f}".format(res)
    #fit_param = r"\begin{align*}\mu &= " + mean_str + r"\\ \sigma &= " + sigma_str + r"\\"
    #fit_param += r"\sigma/\mu &= " + res_str + r"\end{align*}"

    #plot legend
    #leg_items = [Line2D([0], [0], lw=2, color="red"), Line2D([0], [0], lw=0)]
    leg_items = [Line2D([0], [0], lw=0)]
    #plt.rc("text", usetex = True)
    #plt.rc('text.latex', preamble='\usepackage{amsmath}')
    #ax.legend(leg_items, ["Gaussian fit", fit_param])
    ax.legend(leg_items, ["{0:.4f}, {1:.4f}, {2:.4f}".format(pars[0], pars[1], pars[1]/pars[0])])

    #output log
    #out = open("out.txt", "w")
    #out.write( "{0:.4f} +/- {1:.4f} | ".format(pars[0], np.sqrt(cov[0,0])) )
    #out.write( "{0:.4f} +/- {1:.4f} | ".format(pars[1], np.sqrt(cov[1,1])) )
    #out.write( "{0:.4f}".format(pars[1]/pars[0]) )
    #out.close()

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

    return pars[0], pars[1]
    #return res

#gfit

#_____________________________________________________________________________
class legend:
    def __init__(self):
        self.items = []
        self.data = []
    def add_entry(self, i, d):
        self.items.append(i)
        self.data.append(d)
    def draw(self, px, **kw):
        return px.legend(self.items, self.data, **kw)

#_____________________________________________________________________________
def leg_lin(col, sty="-"):
    return Line2D([0], [0], lw=2, ls=sty, color=col)

#_____________________________________________________________________________
def leg_txt():
    return Line2D([0], [0], lw=0)

#_____________________________________________________________________________
def leg_dot(fig, col, siz=8):
    return Line2D([0], [0], marker="o", color=fig.get_facecolor(), markerfacecolor=col, markersize=siz)

#_____________________________________________________________________________
def set_axes_color(ax, col):

    ax.xaxis.label.set_color(col)
    ax.yaxis.label.set_color(col)
    ax.tick_params(axis = "x", colors = col)
    ax.tick_params(axis = "y", colors = col)
    ax.spines["bottom"].set_color(col)
    ax.spines["left"].set_color(col)
    ax.spines["top"].set_color(col)
    ax.spines["right"].set_color(col)

#set_axes_color

#_____________________________________________________________________________
def set_grid(px, col="lime"):

    px.grid(True, color = col, linewidth = 0.5, linestyle = "--")

#set_grid

#_____________________________________________________________________________
if __name__ == "__main__":

    main()

    os.system("mplayer computerbeep_1.mp3 > /dev/null 2>&1")





