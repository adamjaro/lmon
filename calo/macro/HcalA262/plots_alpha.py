#!/usr/bin/python

from pandas import read_csv, DataFrame
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
    funclist.append( run_alpha ) # 0

    funclist[iplot]()

#_____________________________________________________________________________
def run_alpha():

    #Gaussian fit for a given alpha

    alpha = [0.8, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15]
    #alpha = [1]

    infile = "/home/jaroslav/sim/hcal/data/hcal2c/HCal_en10.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2c/HCal_en50.csv"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    res = []
    for a in alpha:
        res.append( gfit(infile, a) )

        #print a, res

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(alpha, res, "o", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#run_alpha

#_____________________________________________________________________________
def gfit(infile, alpha):

    #Gaussian fit for energy resolution at a given momentum

    inp = read_csv(infile)

    sum_edep = inp["hcal_edep_EM"] + alpha*inp["hcal_edep_HAD"]

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

    set_grid(plt, col)

    mean_str = "{0:.4f} \pm {1:.4f}".format(pars[0], np.sqrt(cov[0,0]))
    sigma_str = "{0:.4f} \pm {1:.4f}".format(pars[1], np.sqrt(cov[1,1]))
    res = pars[1]/pars[0]
    res_str = "{0:.4f}".format(res)
    fit_param = r"\begin{align*}\mu &= " + mean_str + r"\\ \sigma &= " + sigma_str + r"\\"
    fit_param += r"\sigma/\mu &= " + res_str + r"\end{align*}"

    #plot legend
    leg_items = [Line2D([0], [0], lw=2, color="red"), Line2D([0], [0], lw=0)]
    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    ax.legend(leg_items, ["Gaussian fit", fit_param])

    #output log
    out = open("out.txt", "w")
    out.write( "{0:.4f} +/- {1:.4f} | ".format(pars[0], np.sqrt(cov[0,0])) )
    out.write( "{0:.4f} +/- {1:.4f} | ".format(pars[1], np.sqrt(cov[1,1])) )
    out.write( "{0:.4f}".format(pars[1]/pars[0]) )
    out.close()

    fig.savefig("01fig.pdf", bbox_inches = "tight")

    #return pars, cov
    return res

#gfit


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





