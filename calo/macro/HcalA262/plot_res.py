#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.lines import Line2D

import os

#_____________________________________________________________________________
def main():

    iplot = 0
    funclist = []
    funclist.append( linear ) # 0
    funclist.append( logx_sqrtE ) # 1

    funclist[iplot]()

#main

#_____________________________________________________________________________
def linear():

    #direct fit in linear horizontal scale

    #hcal2a, e-
    en = [3, 5, 7, 10, 20, 30, 50, 75]
    #res = [0.1398, 0.1082, 0.0922, 0.0776, 0.0546, 0.0446, 0.0345, 0.0284]
    #res = [0.1392, 0.1084, 0.0911, 0.0746, 0.0542, 0.0444, 0.0349, 0.0289] # hcal2ax1
    #res = [0.2306, 0.2118, 0.1959, 0.1820, 0.1596, 0.1534, 0.1459, 0.1369] # hcal2ax2
    res = [0.2316, 0.2089, 0.1959, 0.1913, 0.1728, 0.1653, 0.1636, 0.1589] # hcal2ax3
    #res = [0.2161, 0.2231, 0.1966, 0.1826, 0.1552, 0.1442, 0.1344, 0.1212] # hcal2ax2 EM > 0.1

    #en = [5, 7, 10, 20, 30, 50, 75]
    #res = [0.2231, 0.1966, 0.1826, 0.1552, 0.1442, 0.1344, 0.1212] # hcal2ax2 EM > 0.1
    #en = [10, 20, 30, 50, 75]
    #res = [0.1835, 0.1554, 0.1438, 0.1357, 0.1223] # hcal2ax2 EM > 0.2

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    #resolution data
    plt.plot(en, res, marker="o", linestyle="")

    #fit the resolution
    #pars, cov = curve_fit(resf, en, res)  #  , [0.004, 0.026, 1.9]
    pars, cov = curve_fit(resf2, en, res)  #  , [0.004, 0.026]

    print pars

    #output log
    out = open("out.txt", "w")
    out.write( "a = {0:.4f} +/- {1:.4f}\n".format(pars[0], np.sqrt(cov[0,0])) )
    out.write( "b = {0:.4f} +/- {1:.4f}".format(pars[1], np.sqrt(cov[1,1])) )
    out.close()

    #plot the fit function
    x = np.linspace(en[0], en[-1], 300)
    #y = resf(x, 0.004, 0.026, 1.9)
    #y = resf(x, pars[0], pars[1], pars[2])
    y = resf2(x, pars[0], pars[1])

    plt.plot(x, y, "k-", label="resf", color="blue")

    #ZEUS resolution
    yZEUS = resf2(x, 0.44, 0) # 44% for hadrons
    #yZEUS = resf2(x, 0.235, 0.012) # electrons
    plt.plot(x, yZEUS, "k--", label="ZEUS", color="red")

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    #ax.set_title("Hadron resolution for HcalA262")
    ax.set_title("Hadron resolution for HcalA262, Geant 4.10.02.p02")
    #ax.set_title("Electron resolution for HcalA262")
    ax.set_xlabel("Incident energy $E(\pi^+)$ (GeV)")
    #ax.set_xlabel("Incident energy $E(e^-)$ (GeV)")
    ax.set_ylabel("Resolution $\sigma/\mu$")

    #fit parameters on the plot
    fit_param = ""
    fit_param += r"\begin{align*}"
    fit_param += r"a &= {0:.4f} \pm {1:.4f}\\".format(pars[0], np.sqrt(cov[0,0]))
    fit_param += r"b &= {0:.4f} \pm {1:.4f}".format(pars[1], np.sqrt(cov[1,1]))
    fit_param += r"\end{align*}"

    leg_items = [Line2D([0], [0], lw=2, ls="--", color="red"), Line2D([0], [0], lw=2, color="blue"), Line2D([0], [0], lw=0)]
    ax.legend(leg_items, [r"NIM A262 (1987) 229-242", r"$\frac{\sigma(E)}{E} = \frac{a}{\sqrt{E}} \oplus\ b$", fit_param])

    plt.savefig("01fig.pdf", bbox_inches = "tight")

#linear

#_____________________________________________________________________________
def logx_sqrtE():

    #logarithmic horizontal axis and values of (sigma/mu)*sqrt(E)

    en = [6, 8, 12, 16, 25, 38, 52, 64]
    res = [0.1982, 0.1841, 0.1712, 0.1608, 0.1499, 0.1418, 0.1315, 0.1280]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    #transform to (sigma/mu)*sqrt(E)
    resE = []
    for i in range(len(res)):
        resE.append(res[i]*np.sqrt(en[i]))

    #resolution data
    plt.plot(en, resE, marker="o", linestyle="")

    plt.savefig("01fig.pdf", bbox_inches = "tight")

#logx_sqrtE

#_____________________________________________________________________________
def resf(E, a, b, c):

    #resolution function  sigma/E = sqrt( a^2 + b^2/E + c^2/E^2 )

    r = np.sqrt( a**2 + (b**2)/E + (c**2)/(E**2) )

    return r

#_____________________________________________________________________________
def resf2(E, a, b):

    #resolution function  sigma/E = sqrt( a^2/E + b^2 )

    r = np.sqrt( (a**2)/E + b**2 )

    return r



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
if __name__ == "__main__":

    main()

    os.system("mplayer ../../../macro/computerbeep_1.mp3 > /dev/null 2>&1")






