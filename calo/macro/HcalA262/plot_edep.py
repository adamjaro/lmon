#!/usr/bin/python

from pandas import read_csv
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import norm
from scipy.optimize import curve_fit
import numpy as np

import os
from math import ceil

#_____________________________________________________________________________
def main():

    infile = "HCal.csv"

    iplot = 0
    funclist = []
    funclist.append( fit_err_sum ) # 0

    #open the input
    global inp
    inp = read_csv(infile)

    #call the plot function
    funclist[iplot]()

#main

#_____________________________________________________________________________
def fit_err_sum(infile=None, outfile=None, en=None):

    #fit with error

    #primary energy for legend, GeV
    prim_en = "12"

    #w = 0.94

    #separate input
    if infile is not None:
        global inp
        inp = read_csv(infile)
        prim_en = str(en)

    sum_edep = inp["hcal_edep_EM"] + inp["hcal_edep_HAD"]
    #sum_edep = inp["hcal_edep"]

    nbins = 20

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)

    #data plot
    hx = plt.hist(sum_edep, bins = nbins, color = "lime", density = True, label = "edep")
    #hx = plt.hist(sum_edep, bins = nbins, color = "blue", density = True, label = "edep")

    #Gaussian fit
    centers = (0.5*(hx[1][1:]+hx[1][:-1]))
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), centers, hx[0])

    print pars[0], pars[1], pars[1]/pars[0]

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    #fit function
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 300)
    y = norm.pdf(x, pars[0], pars[1])

    plt.plot(x, y, "k-", label="norm", color="red")

    #ax.set_xlabel("ECal + HCal (GeV)")
    ax.set_xlabel("HCal (GeV)")
    ax.set_ylabel("Counts / {0:.3f} GeV".format((xmax-xmin)/nbins))

    mean_str = "{0:.3f} \pm {1:.3f}".format(pars[0], np.sqrt(cov[0,0]))
    sigma_str = "{0:.3f} \pm {1:.3f}".format(pars[1], np.sqrt(cov[1,1]))
    res_str = "{0:.3f}".format(pars[1]/pars[0])
    fit_param = r"\begin{align*}\mu &= " + mean_str + r"\\ \sigma &= " + sigma_str + r"\\"
    fit_param += r"\sigma/\mu &= " + res_str + r"\end{align*}"

    #plot legend
    leg_items = [Line2D([0], [0], lw=0), Line2D([0], [0], lw=2, color="red"), Line2D([0], [0], lw=0)]
    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    ax.legend(leg_items, ["$E(\pi^+)$ = "+str(prim_en)+" GeV", "Gaussian fit", fit_param])

    #output log
    out = open("out.txt", "w")
    out.write( "{0:.4f} +/- {1:.4f} | ".format(pars[0], np.sqrt(cov[0,0])) )
    out.write( "{0:.4f} +/- {1:.4f} | ".format(pars[1], np.sqrt(cov[1,1])) )
    out.write( "{0:.4f}".format(pars[1]/pars[0]) )
    out.close()

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    if outfile is not None:
        fig.savefig(outfile, bbox_inches = "tight")

    return pars, cov

#fit_err_sum

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
def set_grid(px):

    px.grid(True, color = "lime", linewidth = 0.5, linestyle = "--")

#set_grid

#_____________________________________________________________________________
def make_hist(px, x, xbin, xmin, xmax):

    #bins for a given bin size and range
    nbins = int( ceil( (xmax-xmin)/xbin ) ) #round-up value
    xmax = xmin + float(xbin*nbins) # move max up to pass the bins

    #print nbins, xmin, xmax

    hx = px.hist(x, bins = nbins, range = (xmin, xmax), color = "lime", density = True)

    return hx

#make_hist

#_____________________________________________________________________________
if __name__ == "__main__":

    main()

    os.system("mplayer computerbeep_1.mp3 > /dev/null 2>&1")



















