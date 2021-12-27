#!/usr/bin/python3

from pandas import read_csv, DataFrame, read_hdf
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

    iplot = 1
    funclist = []
    funclist.append( plot_signal ) # 0
    funclist.append( plot_res ) # 1

    funclist[iplot]()

#main

#_____________________________________________________________________________
def plot_signal():

    #signal for a set of energies

    en = [1, 2, 3, 4, 5, 6]

    inp = ["/home/jaroslav//sim/lmon/data/bpc/bpc1a/bpc_en", ".csv"]

    nbins = 60

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)

    ax.set_xlabel("Deposited energy (GeV)")
    ax.set_ylabel("Normalized counts")

    for i in range(len(en)):

        edep, x, y = gfit(inp[0]+str(en[i])+inp[1], True)

        #signal
        plt.hist(edep, bins=nbins, color="blue", density=True, histtype="step", lw=1.5)

        #Gaussian fit to the signal
        plt.plot(x, y, "k-", color="red", lw=1)

    set_grid(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#plot_signal

#_____________________________________________________________________________
def plot_res():

    #energy resolution

    en = [1, 2, 3, 4, 5, 6]

    inp = ["/home/jaroslav//sim/lmon/data/bpc/bpc1a/bpc_en", ".csv"]

    #resolution as sigma/mean
    res = [ms[1]/ms[0] for ms in [gfit(inp[0]+str(en[i])+inp[1]) for i in range(len(en))]]

    #print(res)

    #fit the resolution
    pars, cov = curve_fit(resf3, en, res)

    #print(pars[0], pars[1], pars[2])

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    #print(fig.get_size_inches())
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble=r"\usepackage{amsmath}")
    ax.set_xlabel("Incident energy (GeV)")
    ax.set_ylabel(r"Resolution $\sigma/\langle E\rangle$")

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    #resolution data
    plt.plot(en, res, marker="o", linestyle="", color="blue")

    #plot the fit function
    x = np.linspace(en[0], en[-1], 300)
    y = resf3(x, pars[0], pars[1], pars[2])
    yZEUS = resf3(x, 0.13, 0.17, 0.02) # Nuclear Instruments and Methods in Physics Research A 565 (2006) 572–588

    plt.plot(x, y, "-", label="resf", color="red")
    plt.plot(x, yZEUS, "--", label="resf", color="red")

    #fit parameters for legend
    fit_param = r""
    fit_param += r"\begin{align*}"
    fit_param += r"a &= {0:.4f} \pm {1:.4f}\\".format(pars[0], np.sqrt(cov[0,0]))
    fit_param += r"b &= {0:.4f} \pm {1:.4f}\\".format(pars[1], np.sqrt(cov[1,1]))
    fit_param += r"c &= {0:.4f} \pm {1:.4f}".format(pars[2], np.sqrt(cov[2,2]))
    fit_param += r"\end{align*}"

    leg = legend()
    leg.add_entry(leg_txt(), "BPC")
    leg.add_entry(leg_dot(fig, "blue"), "FTFP\_BERT, 10.7.p01")
    leg.add_entry(leg_lin("red"), r"$\frac{\sigma(E)}{\langle E\rangle} = \frac{a^2}{E} \oplus \frac{b}{\sqrt{E}} \oplus\ c$")
    leg.add_entry(leg_txt(), fit_param)
    leg.add_entry(leg_lin("red", "--"), "NIMA 565 (2006) 572–588")
    leg.draw(plt, col)

    plt.savefig("01fig.pdf", bbox_inches = "tight")

#_____________________________________________________________________________
def gfit(infile, put_hx=False):

    inp = read_csv(infile)

    nbins = 60

    edep = inp["bpc_edep"]

    #data plot
    hx = plt.hist(edep, bins=nbins, color="blue", density=True, histtype="step", lw=1.5)

    #Gaussian fit, bin centers and values
    centers = (0.5*(hx[1][1:]+hx[1][:-1]))
    fit_data = DataFrame({"E": centers, "density": hx[0]})
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), fit_data["E"], fit_data["density"])

    #fit function
    x = np.linspace(plt.xlim()[0], plt.xlim()[1], 300)
    y = norm.pdf(x, pars[0], pars[1])

    if put_hx is True:
        return edep, x, y

    return pars[0], pars[1]

#gfit

#_____________________________________________________________________________
def resf2(E, a, b):

    #resolution function  sigma/E = sqrt( a^2/E + b^2 )
    return np.sqrt( (a**2)/E + b**2 )

#resf2

#_____________________________________________________________________________
def resf3(E, a, b, c):

    #resolution function  sigma/E = sqrt( a^2/E^2 + b^2/E + c^2 )
    return np.sqrt( (a**2)/(E**2) + (b**2)/E + c**2 )

#resf3

#_____________________________________________________________________________
def set_axes_color(ax, col):

    #[t.set_color('red') for t in ax.xaxis.get_ticklines()]
    #[t.set_color('red') for t in ax.xaxis.get_ticklabels()]

    ax.xaxis.label.set_color(col)
    ax.yaxis.label.set_color(col)
    ax.tick_params(which = "both", colors = col)
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
class legend:
    def __init__(self):
        self.items = []
        self.data = []
    def add_entry(self, i, d):
        self.items.append(i)
        self.data.append(d)
    def draw(self, px, col=None, **kw):
        leg = px.legend(self.items, self.data, **kw)
        if col is not None:
            px.setp(leg.get_texts(), color=col)
            if col != "black":
                leg.get_frame().set_edgecolor("orange")
        return leg

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
if __name__ == "__main__":

    main()

















