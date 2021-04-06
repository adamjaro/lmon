#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.lines import Line2D
from pandas import DataFrame

from math import sqrt
import os

#_____________________________________________________________________________
def main():

    iplot = 0
    funclist = []
    funclist.append( linear ) # 0
    funclist.append( logx_sqrtE ) # 1
    funclist.append( individual_par ) # 2


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
    #res = [0.2316, 0.2089, 0.1959, 0.1913, 0.1728, 0.1653, 0.1636, 0.1589] # hcal2ax3
    #res = [0.2161, 0.2231, 0.1966, 0.1826, 0.1552, 0.1442, 0.1344, 0.1212] # hcal2ax2 EM > 0.1
    #res = [0.2306, 0.2077, 0.1970, 0.1853, 0.1801, 0.1774, 0.1667, 0.1632] # hcal2ax4
    #res = [0.3410, 0.2630, 0.2184, 0.1670, 0.1219, 0.1050, 0.0929, 0.0826] # hcal2b
    #res = [0.1408, 0.1090, 0.0899, 0.0770, 0.0546, 0.0442, 0.0344, 0.0282] # hcal2bx1 (e-)
    #res = [0.3153, 0.2468, 0.2013, 0.1581, 0.1175, 0.1042, 0.0908, 0.0825] # hcal2bx2
    #res = [0.2310, 0.1890, 0.1601, 0.1266, 0.0875, 0.0741, 0.0599, 0.0530] # hcal2bx3
    #res = [0.1395, 0.1073, 0.0894, 0.0758, 0.0524, 0.0432, 0.0342, 0.0281] # hcal2bx4 (e-)
    res = [0.2288, 0.1870, 0.1594, 0.1248, 0.0873, 0.0731, 0.0591, 0.0518] # hcal2c, pass2
    #res = [0.2179, 0.1795, 0.1532, 0.1239, 0.0892, 0.0758, 0.0629, 0.0557] # hcal2cx1
    #res = [0.2714, 0.2278, 0.1958, 0.1533, 0.1090, 0.0947, 0.0810, 0.0725] # hcal2cx2
    #res = [0.2136, 0.1918, 0.1729, 0.1559, 0.1300, 0.1213, 0.1123, 0.1040] # hcal2cx3
    #res = [0.2131, 0.1778, 0.1531, 0.1262, 0.0932, 0.0808, 0.0686, 0.0615] # hcal2cx4
    #res = [0.2290, 0.1872, 0.1591, 0.1252, 0.0873, 0.0731, 0.0591, 0.0518] # hcal2c2

    #en = [5, 7, 10, 20, 30, 50, 75]
    #res = [0.2231, 0.1966, 0.1826, 0.1552, 0.1442, 0.1344, 0.1212] # hcal2ax2 EM > 0.1
    #en = [10, 20, 30, 50, 75]
    #res = [0.1835, 0.1554, 0.1438, 0.1357, 0.1223] # hcal2ax2 EM > 0.2

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    #resolution data
    plt.plot(en, res, marker="o", linestyle="", color="blue")

    #fit the resolution
    #pars, cov = curve_fit(resf, en, res)  #  , [0.004, 0.026, 1.9]
    pars, cov = curve_fit(resf2, en, res)  #  , [0.004, 0.026]
    #pars, cov = curve_fit(resf3, en, res)

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
    #y = resf3(x, pars[0])

    plt.plot(x, y, "k-", label="resf", color="blue")

    #ZEUS resolution
    yZEUS = resf2(x, 0.442, 0) # 44% for hadrons
    #yZEUS = resf2(x, 0.235, 0.012) # electrons
    plt.plot(x, yZEUS, "k--", label="ZEUS", color="red")

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    #ax.set_title("Hadron resolution for HcalA262")
    #ax.set_title("Hadron resolution for HcalA262, FTFP$\_$BERT$\_$HP")
    #ax.set_title("Electron resolution for HcalA262")
    #ax.set_xlabel("Incident energy $E(\pi^+)$ (GeV)")
    #ax.set_xlabel("Incident energy $E(e^-)$ (GeV)")
    #ax.set_ylabel("Resolution $\sigma/\mu$")
    ax.set_title("Lead - scintillator (HcalA262)")
    ax.set_xlabel("Incident energy $E$ (GeV)")
    ax.set_ylabel(r"Resolution $\sigma/\langle E\rangle$")

    ax.set_xscale("log")

    xlabels = [str(i) for i in en]
    plt.xticks(en, xlabels)

    #fit parameters on the plot
    fit_param = ""
    fit_param += r"\begin{align*}"
    fit_param += r"a &= {0:.4f} \pm {1:.4f}\\".format(pars[0], np.sqrt(cov[0,0]))
    fit_param += r"b &= {0:.4f} \pm {1:.4f}".format(pars[1], np.sqrt(cov[1,1]))
    fit_param += r"\end{align*}"

    leg_items = [leg_lin("red", "--"), leg_txt(), leg_dot(fig, "blue"), leg_lin("blue")]
    res_form = r"$\frac{\sigma(E)}{\langle E\rangle} = \frac{a}{\sqrt{E}} \oplus\ b$"
    ax.legend(leg_items, [r"44.2\%$\sqrt{E}$, NIM A262 (1987) 229-242", res_form, "FTFP\_BERT\_HP", fit_param])

    plt.savefig("01fig.pdf", bbox_inches = "tight")

#linear

#_____________________________________________________________________________
def logx_sqrtE():

    #logarithmic horizontal axis and values of (sigma/mu)*sqrt(E)

    en = [3, 5, 7, 10, 20, 30, 50, 75]
    res = [0.2288, 0.1870, 0.1594, 0.1248, 0.0873, 0.0731, 0.0591, 0.0518] # hcal2c, pass2

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    #transform to (sigma/mu)*sqrt(E)
    res = [1e2*sqrt(en[i])*res[i] for i in range(len(res))]

    ax.set_ylim([20, 60])
    ax.set_xlim([1, 100])

    ax.set_xscale("log")

    #resolution data
    plt.plot(en, res, marker="o", linestyle="")

    plt.savefig("01fig.pdf", bbox_inches = "tight")

#logx_sqrtE

#_____________________________________________________________________________
def individual_par():

    #individual resolution parametrizations

    #energy range
    emin = 3
    emax = 75

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    #input data
    inp = {
        "label": ["c",    "cx1",    "cx2",    "cx3",    "cx4"],
        "kB":    [0.126,  0.08,     0.5,      0.01,     0.06],
        "a":     [0.4035, 0.3827,   0.4792,   0.3446,   0.3727],
        "b":     [0.0157, 0.0324,   0.0428,   0.1033,   0.0447],
        "col":   ["blue", "gold",   "violet", "orange", "lime"]
    }
    df = DataFrame(inp).sort_values(by="kB")

    #make the plot
    x = np.linspace(emin, emax, 300)
    leg_items = [Line2D([0], [0], lw=0)]
    leg_val = [r"$k_B$ in mm/MeV, $\frac{\sigma(E)}{E} = \frac{a}{\sqrt{E}} \oplus\ b$"]
    for index, i in df.iterrows():

        plt.plot(x, resf2(x, i["a"], i["b"]), "k-", color=i["col"])
        leg_items.append(Line2D([0], [0], lw=2, color=i["col"]))
        leg_val.append(r"$k_B$: {0:.3f}, $a$ = {1:.3f}, $b$ = {2:.3f}".format(i["kB"], i["a"], i["b"]))

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')

    ax.set_title("Hadron resolution for HcalA262")
    ax.set_xlabel("Incident energy $E(\pi^+)$ (GeV)")
    ax.set_ylabel("Resolution $\sigma/\mu$")

    ax.legend(leg_items, leg_val)

    plt.savefig("01fig.pdf", bbox_inches = "tight")

#individual_par

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
def resf3(E, a):

    #resolution function  sigma/E = sqrt( a^2/E )

    r = np.sqrt( (a**2)/E )

    return r

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
if __name__ == "__main__":

    main()

    os.system("mplayer ../../../macro/computerbeep_1.mp3 > /dev/null 2>&1")






