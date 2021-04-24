#!/usr/bin/python

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

    iplot = 2
    funclist = []
    funclist.append( run_alpha ) # 0
    funclist.append( run_eh ) # 1
    funclist.append( run_res ) # 2

    funclist[iplot]()

#_____________________________________________________________________________
def run_res():

    #energy resolution as a function of energy

    #GeV
    #en = [3, 5, 7, 10, 20, 30, 50, 75]
    #en = [10]
    en = [6, 8, 12, 16, 25, 32, 64]

    #inp = ["/home/jaroslav/sim/hcal/data/hcal3a/HCal_en", ".h5"]
    inp = ["/home/jaroslav/sim/hcal/data/hcal3b/HCal_en", ".h5"]
    #inp = ["/home/jaroslav/sim/hcal/data/hcal3ax1/HCal_en", ".h5"]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    res = []
    for i in en:
        mean, sigma = gfit(inp[0]+str(i)+inp[1], 1.2)
        res.append( sigma/mean )

    #print res

    #res = [0.26083651824598386, 0.20830177294832528, 0.1719577008925196, 0.15239249536493935, 0.13622102149109735, 0.12226436738270607, 0.12239779598312915, 0.1220989616622746]

    #fit the resolution
    pars, cov = curve_fit(resf2, en, res)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    #resolution data
    plt.plot(en, res, marker="o", linestyle="", color="blue")

    #plot the fit function
    x = np.linspace(en[0], en[-1], 300)
    y = resf2(x, pars[0], pars[1])

    plt.plot(x, y, "k-", label="resf", color="blue")

    ax.set_xscale("log")
    plt.xticks(en, [str(i) for i in en])

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    ax.set_xlabel("Incident energy $E$ (GeV)")
    ax.set_ylabel(r"Resolution $\sigma/\langle E\rangle$")

    #fit parameters for legend
    fit_param = ""
    fit_param += r"\begin{align*}"
    fit_param += r"a &= {0:.4f} \pm {1:.4f}\\".format(pars[0], np.sqrt(cov[0,0]))
    fit_param += r"b &= {0:.4f} \pm {1:.4f}".format(pars[1], np.sqrt(cov[1,1]))
    fit_param += r"\end{align*}"

    leg = legend()
    leg.add_entry(leg_dot(fig, "blue"), "FTFP\_BERT\_HP, 10.7.p01")
    leg.add_entry(leg_lin("blue"), r"$\frac{\sigma(E)}{\langle E\rangle} = \frac{a}{\sqrt{E}} \oplus\ b$")
    leg.add_entry(leg_txt(), fit_param)
    leg.draw(plt, col)

    plt.savefig("01fig.pdf", bbox_inches = "tight")

#run_res

#_____________________________________________________________________________
def resf2(E, a, b):

    #resolution function  sigma/E = sqrt( a^2/E + b^2 )
    return np.sqrt( (a**2)/E + b**2 )

#resf2

#_____________________________________________________________________________
def run_eh():

    #e/h ratio
    beam = [3, 5, 7, 10, 20, 30, 50, 75]

    inp_h = ["/home/jaroslav/sim/hcal/data/hcal3a/HCal_en", ".h5"]
    inp_e = ["/home/jaroslav/sim/hcal/data/hcal3ax1/HCal_en", ".h5"]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    #eh = []
    #for i in beam:
    #    mean_h, sigma_h = gfit(inp_h[0]+str(i)+inp_h[1], 1.)
    #    mean_e, sigma_e = gfit(inp_e[0]+str(i)+inp_e[1], 1.)
    #    eh.append(mean_e/mean_h)
    #print eh

    #hcal2c2, hcal2cx5, alpha_fix = 1
    #eh = [0.9794002736470295, 1.0047705480458915, 0.9993314733476454, 0.9915415124811879, 0.9927651323442229, 0.9971136899733369, 0.9975166634190157, 1.000640450250562]

    eh = [1.2043151051440364, 1.1608734893714028, 1.1389287513817081, 1.143370959029314, 1.151118138852424, 1.1522250055361773, 1.162840657742684, 1.1702070246063314]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_ylim([0.9, 1.3])

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    ax.set_xlabel("Incident energy $E$ (GeV)")
    ax.set_ylabel("e/h")

    set_axes_color(ax, col)
    set_grid(plt, col)

    ax.set_xscale("log")
    plt.xticks(beam, [str(i) for i in beam])

    #line at e/h = 1
    x = np.linspace(beam[0], beam[-1], 300)
    plt.plot(x, [1. for i in x], "k--", color="red", lw=2)

    plt.plot(beam, eh, "o", color="blue")

    leg = legend()
    leg.add_entry(leg_lin("red", "--"), "e/h = 1")
    leg.add_entry(leg_dot(fig, "blue"), "FTFP\_BERT\_HP, 10.7.p01")
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#run_eh

#_____________________________________________________________________________
def run_alpha():

    #Gaussian fit for a given alpha

    #alpha = [0.8, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15]
    #alpha = [1]
    alpha = [0.8, 1., 1.2, 1.4, 1.6, 1.8]

    infile = "/home/jaroslav/sim/hcal/data/hcal3b/HCal_en6.h5"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    res = []
    for a in alpha:
        mean, sigma = gfit(infile, a)
        res.append( sigma/mean )

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

    inp = read_hdf(infile)

    #sum_edep = inp["hcal_edep_EM"] + alpha*inp["hcal_edep_HAD"]
    sum_edep = inp["ecal_edep"] + alpha*inp["hcal_edep_HAD"]

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

    leg = legend()
    leg.add_entry(leg_txt(), "alpha: "+str(alpha))
    leg.add_entry(leg_txt(), "mu: {0:.4f}".format(pars[0]))
    leg.add_entry(leg_txt(), "sig: {0:.4f}".format(pars[1]))
    leg.add_entry(leg_txt(), "r: {0:.4f}".format(pars[1]/pars[0]))
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

    return pars[0], pars[1]

#gfit

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
            if col is not "black":
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
if __name__ == "__main__":

    main()

    os.system("mplayer computerbeep_1.mp3 > /dev/null 2>&1")





