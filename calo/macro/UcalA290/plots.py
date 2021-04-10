#!/usr/bin/python

from pandas import read_csv, DataFrame, read_hdf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import norm
from scipy.optimize import curve_fit
import numpy as np
import collections

import os
from math import ceil, log10, sqrt

#_____________________________________________________________________________
def main():

    iplot = 9
    funclist = []
    funclist.append( run_alpha ) # 0
    funclist.append( run_sec_fraction ) # 1
    funclist.append( fit_alpha ) # 2
    funclist.append( momentum_alpha ) # 3
    funclist.append( momentum_res ) # 4
    funclist.append( res_fit ) # 5
    funclist.append( run_eh ) # 6
    funclist.append( res_fit_sqrtE ) # 7
    funclist.append( res_plot_sqrtE ) # 8
    funclist.append( compare_res ) # 9

    funclist[iplot]()

#_____________________________________________________________________________
def compare_res():

    #compare sets of resolution results

    momentum = [1, 1.5, 2, 3, 5, 7, 10, 20, 30, 50, 75, 100]
    momentum_red = [1, 2, 5, 10, 30, 75]

    #HP new, ucal1a1x16, alpha_fix = 1, fit: [0.23203715 0.05850512]
    res_hp = [0.2193080489595701, 0.1984711156277112, 0.18078266572034335, 0.15840828399379805, 0.13009282933727834, 0.11610975519973563, 0.10168621535705112, 0.07801513106465013, 0.0695711734912218, 0.06249469721217424, 0.05816156074296834, 0.05588241276047411]

    #HP old, ucal1a1x7, alpha_fix = 1, fit: [0.24785106 0.1011364 ]
    res_hp_old = [0.25937785564433274, 0.20522201016800912, 0.16532176438059826, 0.13628672072508746, 0.1056887100970676, 0.0941791116750464]

    #LHEP, ucal1a1x13, alpha by fits, fit: [0.39724115 0.03498337]
    res_lhep = [0.39953239509912547, 0.2733814887982889, 0.198492847444043, 0.1265011811951121, 0.0781079458675066, 0.05745226370685749]


    fit_lhep = curve_fit(resf2, momentum_red, res_lhep)
    fit_hp_old = curve_fit(resf2, momentum_red, res_hp_old)
    fit_hp = curve_fit(resf2, momentum, res_hp)

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    #plot the fit function
    x = np.linspace(momentum[0], momentum[-1], 300)
    plt.plot(x, resf2(x, fit_lhep[0][0], fit_lhep[0][1]), "k-", color="lime")
    plt.plot(x, resf2(x, fit_hp_old[0][0], fit_hp_old[0][1]), "k-", color="orange")
    plt.plot(x, resf2(x, fit_hp[0][0], fit_hp[0][1]), "k-", color="blue")

    #plot the data
    plt.plot(momentum, res_hp, "o", color="blue", markersize=5)
    plt.plot(momentum_red, res_hp_old, "o", color="orange", markersize=5)
    plt.plot(momentum_red, res_lhep, "o", color="lime", markersize=5)

    #Reference from beam data
    plt.plot(x, resf2(x, 0.35, 0), "k--", color="red")

    ax.set_xscale("log")

    #ax.set_title("Depleted uranium - scintillator (UcalA290)") #  UcalA290
    ax.set_xlabel("Incident momentum $E_{\mathrm{beam}}$ (GeV/c)")
    ax.set_ylabel(r"Resolution $\sigma/\langle E\rangle$")

    plt.xticks(momentum, [str(i) for i in momentum])

    #fit parameters on the plot
    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    #plt.rcParams["text.latex.preamble"] = [r"\usepackage{amsmath}", r"\usepackage{graphicx}"]

    leg = legend()
    leg.add_entry(leg_lin("red", "--"), r"35\%$\sqrt{E_b},$ DESY 89-128 (1989)")
    leg.add_entry(leg_txt(), r"$\frac{\sigma(E)}{\langle E\rangle} = \frac{a}{\sqrt{E}} \oplus\ b$")
    leg.add_entry(leg_dot(fig, "blue"), "FTFP\_BERT\_HP, 10.7.p01")
    leg.add_entry(leg_lin("blue"), r"$a$ = {0:.4f}, $b$ = {1:.4f}".format(fit_hp[0][0], fit_hp[0][1]))
    leg.add_entry(leg_dot(fig, "orange"), "FTFP\_BERT\_HP, 10.5.p01")
    leg.add_entry(leg_lin("orange"), r"$a$ = {0:.4f}, $b$ = {1:.4f}".format(fit_hp_old[0][0], fit_hp_old[0][1]))
    leg.add_entry(leg_dot(fig, "lime"), "LHEP, 9.4.p03")
    leg.add_entry(leg_lin("lime"), r"$a$ = {0:.4f}, $b$ = {1:.4f}".format(fit_lhep[0][0], fit_lhep[0][1]))
    leg.draw(ax)

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#compare_res

#_____________________________________________________________________________
def res_plot_sqrtE():

    #plot to energy resolution as (sigma/E)*sqrt(momentum) hadrons at lower energies

    #momentum = [0.5, 1, 2, 5, 10, 30, 75]
    #momentum = [0.5, 1, 2, 5, 10]
    momentum = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10]

    #NIM A290 (1990) 95-108, Table 8, Pions +
    data =     [25.9, 27.7, 30.5, 33.3, 33.9, 32.8, 34.5, 34.6, 33.2]
    data_err = [0.4,  0.4,  0.3,  0.3,  0.3,  0.5,  0.5,  0.5,  0.5]

    infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x16/HCal_p", ".h5"]
    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x19/HCal_p", ".h5"]

    #res = momentum_res(momentum, infile, 1)

    #ucal1a1x16, alpha_fix = 1
    #res = [0.26320004184019585, 0.233560061823574, 0.2193080489595701, 0.1984711156277112, 0.18078266572034335, 0.15840828399379805, 0.13009282933727834, 0.11610975519973563, 0.10168621535705112]

    #ucal1a1x19, alpha_fix = 1
    res = [0.3354936775470077, 0.32102372347325425, 0.31610800536324174, 0.28162160992154256, 0.2552691104509457, 0.22244311212670287, 0.17548157959587743, 0.14089615617777254, 0.11610713910553998]

    res = [1e2*sqrt(momentum[i])*res[i] for i in range(len(res))]

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    #ax.set_title("Hadron resolution for UcalA290")
    ax.set_xlabel("Incident momentum $E_{\mathrm{beam}}$ (GeV/c)")
    ax.set_ylabel(r"$\frac{\sigma}{\langle E\rangle}\sqrt{E_b}$ (%)")

    set_axes_color(ax, col)
    set_grid(plt, col)

    ax.set_ylim([15, 45])
    #ax.set_ylim([15, 50])

    ax.set_xscale("log")

    plt.xticks(momentum, [str(i) for i in momentum])

    #NIM A290 (1990) 95-108
    plt.errorbar(momentum, data, yerr=data_err, fmt="o", color="red", markersize=4)
    x = np.linspace(1.5, momentum[-1], 300)
    plt.plot(x, [34. for i in x], "k--", color="red")

    #plot Geant data
    plt.plot(momentum, res, "o", color="blue")

    leg = legend()
    leg.add_entry(leg_dot(fig, "red"), "Data, NIM A290 (1990) 95-108")
    leg.add_entry(leg_lin("red", "--"), r"34\%$\sqrt{E_b}$, NIM A290 (1990) 95-108")
    leg.add_entry(leg_dot(fig, "blue"), "FTFP\_BERT\_HP, 10.7.p01")
    #leg.add_entry(leg_dot(fig, "blue"), "10 mm Pb absorbers")
    leg.draw(ax)

    #leg_items = [Line2D([0], [0], lw=2, ls="--", color="red"),
    #    Line2D([0], [0], marker="o", color=fig.get_facecolor(), markerfacecolor="b", markersize=8)]
    #leg_data = [r"34\%$\sqrt{E_b}$, NIM A290 (1990) 95-108", "Geant4"]
    #ax.legend(leg_items, leg_data, loc="upper left", handletextpad=0.1)

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#res_plot_sqrtE

#_____________________________________________________________________________
def res_fit_sqrtE():

    #constant fit to energy resolution as (sigma/E)*sqrt(momentum)

    #momentum = [1, 2, 5, 10, 30, 75]
    #momentum = [0.5, 1, 2, 5, 10]
    #momentum = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10, 20, 30, 50, 75, 100]
    momentum = [1, 1.5, 2, 3, 5, 7, 10, 20, 30, 50, 75, 100]

    infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x17/HCal_p", ".h5"]

    #res = momentum_res(momentum, infile, 1.)

    #ucal1a1x17, start at 1 GeV, alpha_fix = 1
    res = [0.1636429159456063, 0.13276021606111554, 0.11446698928931372, 0.0929041695644913, 0.07352547690258085, 0.0616099487496253, 0.051355260370327185, 0.03603149003336653, 0.030287934949643127, 0.02320369758792059, 0.018863187247725524, 0.016391749514058387]

    res = [1e2*sqrt(momentum[i])*res[i] for i in range(len(res))]

    pars, cov = curve_fit(lambda x, a: a, momentum, res)
    print pars
    #pars_hp, cov_hp = curve_fit(lambda x, a: a, momentum, res_hp)

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    #ax.set_title("Electron resolution for UcalA290")
    ax.set_xlabel("Incident momentum $E_{\mathrm{beam}}$ (GeV/c)")
    ax.set_ylabel(r"$\frac{\sigma}{\langle E\rangle}\sqrt{E_b}$ (%)")
    #ax.set_ylabel("Counts / {0:.3f} GeV".format((plt.xlim()[1]-plt.xlim()[0])/nbins))

    ax.set_ylim([15.5, 19])

    set_axes_color(ax, col)
    set_grid(plt, col)

    ax.set_xscale("log")

    xlabels = [str(i) for i in momentum]
    plt.xticks(momentum, xlabels)

    #plot the fit function
    x = np.linspace(momentum[0], momentum[-1], 300)
    plt.plot(x, [pars[0] for i in x], "k-", color="blue") # fit result
    #plt.plot(x, [pars_hp[0] for i in x], "k-", color="lime")
    plt.plot(x, [18. for i in x], "k--", color="red", lw=2) # DESY 89-128 (1989)

    #plot the data
    #plt.plot(momentum, res_hp, "o", color="lime")
    plt.plot(momentum, res, "o", color="blue")

    leg_items = [leg_lin("red", "--"), leg_dot(fig, "blue"), leg_lin("blue")]
    #leg_items = [Line2D([0], [0], lw=2, ls="--", color="red"), Line2D([0], [0], lw=2, color="blue")]
    fit_str = r"${0:.3f} \pm {1:.3f}$".format(pars[0], np.sqrt(cov[0,0]))
    leg_data = [r"18\%$\sqrt{E_b}$, DESY 89-128 (1989)", "FTFP\_BERT\_HP, 10.7.p01", fit_str+r" \%$\sqrt{E_b}$"]
    ax.legend(leg_items, leg_data)

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#_____________________________________________________________________________
def run_eh():

    #electron/hadron ratio

    momentum_lhep = [1, 2, 5, 10, 30, 75]
    #momentum = [0.5, 1, 2, 5, 10]
    momentum = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10, 20, 30, 50, 75, 100]

    inp_h = ["/home/jaroslav/sim/hcal/data/ucal1a1x13/HCal_p", ".h5"]
    inp_e = ["/home/jaroslav/sim/hcal/data/ucal1a1x15/HCal_p", ".h5"]
    #inp_h = ["/home/jaroslav/sim/hcal/data/ucal1a1x16/HCal_p", ".h5"]
    #inp_e = ["/home/jaroslav/sim/hcal/data/ucal1a1x17/HCal_p", ".h5"]

    #alpha_min = momentum_alpha(momentum, inp_h)

    #alpha_min = [0.9895791583166331, 0.8324649298597193, 0.8549098196392785, 0.8933867735470942, 0.917434869739479, 0.9575150300601202, 0.9799599198396793]
    #alpha_min = [1 for i in momentum]

    #eh = []
    #for i in range(len(momentum)):
    ##    #mean_h = gfit(read_hdf(inp_h[0]+str(momentum[i])+inp_h[1]), alpha_min[i], momentum[i], False)
    #    mean_h = gfit(read_hdf(inp_h[0]+str(momentum[i])+inp_h[1]), 1., momentum[i], False)
    #    mean_e = gfit(read_hdf(inp_e[0]+str(momentum[i])+inp_e[1]), 1., momentum[i], False)

    #    eh.append( mean_e/mean_h )

    #print "eh:", eh

    #13, 14, alpha_fix = 1, reduced momentum set
    eh_lhep = [1.2399958651962177, 1.1696602240227847, 1.1728114481778955, 1.1916884239507186, 1.1503937509107587, 1.1313732698603876]

    #16, 15, alpha_fix = 1
    eh = [0.7273586532929273, 0.72128611958076, 0.7388223700018338, 0.7708778816801959, 0.7848688024695556, 0.8048516188935679, 0.816016939794907, 0.8173220332282994, 0.8241878044453269, 0.8402468342124685, 0.8490726811844678, 0.8591380593008286, 0.8684122724661077, 0.8752171835220534]

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    #ax.set_title("Electron/hadron ratio for UcalA290")
    ax.set_xlabel("Incident momentum $E_{\mathrm{beam}}$ (GeV/c)")
    ax.set_ylabel("e/h")

    ax.set_xscale("log")
    plt.xticks(momentum, [str(i) for i in momentum])

    ax.set_ylim([0.5, 1.6])

    set_axes_color(ax, col)
    set_grid(plt, col)

    #line at e/h = 1
    x = np.linspace(momentum[0], momentum[-1], 300)
    plt.plot(x, [1. for i in x], "k--", color="red", lw=2)

    #plot the data
    plt.plot(momentum, eh, "o", color="blue")
    plt.plot(momentum_lhep, eh_lhep, "o", color="lime")

    leg = legend()
    leg.add_entry(leg_lin("red", "--"), "e/h = 1")
    leg.add_entry(leg_dot(fig, "blue"), "FTFP\_BERT\_HP, 10.7.p01")
    leg.add_entry(leg_dot(fig, "lime"), "LHEP, 9.4.p03")
    leg.draw(ax)

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#_____________________________________________________________________________
def res_fit():

    #parametric fit to energy resolution

    #momentum = [0.5, 1, 2, 5, 10, 30, 75]
    #momentum = [0.5, 1, 2, 5, 10]
    #momentum = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10, 20, 30, 50, 75, 100]
    #momentum = [1, 1.5, 2, 3, 5, 7, 10, 20, 30, 50, 75, 100]
    momentum = [1, 2, 5, 10, 30, 75]

    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x7/HCal_p", ".h5"]
    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x16/HCal_p", ".h5"]
    infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x13/HCal_p", ".h5"]
    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x19/HCal_p", ".h5"]

    #res = momentum_res(momentum, infile)#, 1

    #ucal1a1x16, alpha_fix = 1, fit: [0.23203715 0.05850512]
    #res = [0.2193080489595701, 0.1984711156277112, 0.18078266572034335, 0.15840828399379805, 0.13009282933727834, 0.11610975519973563, 0.10168621535705112, 0.07801513106465013, 0.0695711734912218, 0.06249469721217424, 0.05816156074296834, 0.05588241276047411]

    #ucal1a1x19, alpha_fix = 1, fit: [0.34375418 0.03136181]
    #res = [0.31610800536324174, 0.28162160992154256, 0.2552691104509457, 0.22244311212670287, 0.17548157959587743, 0.14089615617777254, 0.11610713910553998, 0.08162116779607213, 0.06896943879206478, 0.0552551774455561, 0.04635759684210208, 0.04196737705965597]

    #ucal1a1x7, alpha_fix = 1, fit: [0.24785106 0.1011364 ]
    #res = [0.25937785564433274, 0.20522201016800912, 0.16532176438059826, 0.13628672072508746, 0.1056887100970676, 0.0941791116750464]

    #ucal1a1x13, alpha by fits, fit: [0.39724115 0.03498337]
    #res = [0.39953239509912547, 0.2733814887982889, 0.198492847444043, 0.1265011811951121, 0.0781079458675066, 0.05745226370685749]

    pars, cov = curve_fit(resf2, momentum, res)
    print pars

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    #plot the fit function
    x = np.linspace(momentum[0], momentum[-1], 300)
    plt.plot(x, resf2(x, pars[0], pars[1]), "k-", color="blue")
    x1 = np.linspace(momentum[1], momentum[-1], 300)
    plt.plot(x, resf2(x, 0.35, 0), "k--", color="red")

    #plot the data
    plt.plot(momentum, res, "o", color="blue")

    ax.set_xscale("log")

    #ax.set_title("Hadron resolution for UcalA290")
    ax.set_xlabel("Incident momentum $E_{\mathrm{beam}}$ (GeV/c)")
    ax.set_ylabel(r"Resolution $\sigma/\langle E\rangle$")

    xlabels = [str(i) for i in momentum]
    plt.xticks(momentum, xlabels)

    #fit parameters on the plot
    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    fit_param = ""
    fit_param += r"\begin{align*}"
    fit_param += r"a &= {0:.4f} \pm {1:.4f}\\".format(pars[0], np.sqrt(cov[0,0]))
    fit_param += r"b &= {0:.4f} \pm {1:.4f}".format(pars[1], np.sqrt(cov[1,1]))
    fit_param += r"\end{align*}"

    leg_items = [leg_lin("red", "--"), leg_dot(fig, "blue"), leg_lin("blue"), leg_txt()]
    ax.legend(leg_items, [r"35\%$\sqrt{E_b},$ DESY 89-128 (1989)", "FTFP\_BERT\_HP, 10.7.p01",
        r"$\frac{\sigma(E)}{\langle E\rangle} = \frac{a}{\sqrt{E}} \oplus\ b$", fit_param])

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#_____________________________________________________________________________
def resf2(E, a, b):

    #resolution function  sigma/E = sqrt( a^2/E + b^2 )
    return np.sqrt( (a**2)/E + b**2 )

#_____________________________________________________________________________
def momentum_res(momentum=None, infile=None, alpha_fix=None):

    #energy resolution as a function of beam momentum

    #momentum = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10]
    #momentum = [1]
    #momentum = [0.5, 1, 2, 5, 10, 30, 75]
    #alpha_fix = 1.2
    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x13/HCal_p", ".h5"]


    if alpha_fix is not None:
        alpha_min = [alpha_fix for i in momentum]
    else:
        alpha_min = momentum_alpha(momentum, infile)

    #alpha_min = [1.7, 1.4, 1.2, 1, 1, 1]

    res = [gfit(read_hdf(infile[0]+str(momentum[i])+infile[1]), alpha_min[i], momentum[i]) for i in range(len(momentum))]

    print "alpha_min:", alpha_min
    print "res:", res

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    res_plot = [1e2*sqrt(momentum[i])*res[i] for i in range(len(res))]

    #print res

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    #ax.set_xscale("log")

    plt.plot(momentum, res_plot, "o", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

    return res

#_____________________________________________________________________________
def momentum_alpha(momentum=None, infile=None):

    #minimal alpha as a function of beam momentum

    #momentum = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10]
    #momentum += [20, 30, 50, 75, 100]
    #momentum = [1, 2, 5, 10, 30, 75]

    #momentum = [10]

    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x16/HCal_p", ".h5"]

    #alpha = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3]
    alpha = [0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    alpha_min = [fit_alpha(alpha, p, infile) for p in momentum]

    print alpha_min

    #normalization for alpha at momentum = 30 GeV
    alpha_min_plot = [i/alpha_min[-2] for i in alpha_min]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_ylim([0.5, 1.2])

    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(momentum, alpha_min_plot, "o", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

    return alpha_min

#_____________________________________________________________________________
def fit_alpha(alpha=None, pbeam=None, infile=None):

    #polynomial fit for resolution as a function of alpha

    #alpha = [0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4]
    #alpha = [0.01, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 1, 1.1]
    #pbeam = 10
    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x16/HCal_p", ".h5"]

    res = run_alpha(alpha, pbeam, infile)

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    #make the fit
    pars, cov = curve_fit(poly_alpha, alpha, res)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    ax.set_title("p: "+str(pbeam))

    #fit function
    x = np.linspace(alpha[0], alpha[-1], 500)
    y = poly_alpha(x, pars[0], pars[1], pars[2], pars[3])
    plt.plot(x, y, "k-", color="blue")

    #minimal alpha
    alpha_min = x[ np.where( y==y.min() ) ][0]
    print "alpha_min:", alpha_min

    #normalization
    #res = [i/res[-3] for i in res]
    #ax.set_ylim([0.8, 1.6])

    plt.plot(alpha, res, "o", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

    return alpha_min

#_____________________________________________________________________________
def poly_alpha(r, a, b, c, d):

    #polynomial fit to resolution as a function of alpha

    #return a*r**2 + b*r + c
    return a + b*r + c*r**2 + d*r**3

#_____________________________________________________________________________
def run_alpha(alpha=None, pbeam=None, infile=None):

    #Gaussian fit for a given alpha

    #alpha = [1]
    #alpha = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2]
    #pbeam = 10

    #infile = "/home/jaroslav/sim/hcal/data/ucal1a1/HCal_p10.csv"
    #infile = "/home/jaroslav/sim/hcal/data/ucal1a1x1/HCal_p10.csv"
    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x16/HCal_p", ".h5"]

    #inp = read_hdf("/home/jaroslav/sim/hcal/data/ucal1a1x8/HCal_p"+str(pbeam)+".h5")
    inp = read_hdf(infile[0]+str(pbeam)+infile[1])

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    #normalization for alpha = 1
    r1 = gfit(inp, 1., pbeam)

    res = []
    for a in alpha:
        res.append( gfit(inp, a, pbeam)/r1 )

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    ax.set_title("p: "+str(pbeam))

    plt.plot(alpha, res, "o", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

    return res

#run_alpha

#_____________________________________________________________________________
def gfit(inp, alpha, pbeam=None, res_out=True):

    #Gaussian fit for energy resolution at a given momentum

    #inp = read_csv(infile)

    sum_edep = inp["ucal_edep_EMC"] + alpha*inp["ucal_edep_HAC1"] + alpha*inp["ucal_edep_HAC2"]
    #sum_edep = alpha*inp["ucal_edep_EMC"] + inp["ucal_edep_HAC1"] + inp["ucal_edep_HAC2"]
    #sum_edep = inp["ucal_edep_EMC"] + inp["ucal_edep_HAC1"] + inp["ucal_edep_HAC2"]

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

    #ax.set_title("alpha: "+str(alpha)+", p: "+str(pbeam))

    set_grid(plt, col)

    #mean_str = "{0:.4f} \pm {1:.4f}".format(pars[0], np.sqrt(cov[0,0]))
    #sigma_str = "{0:.4f} \pm {1:.4f}".format(pars[1], np.sqrt(cov[1,1]))
    res = pars[1]/pars[0]
    #res_str = "{0:.4f}".format(res)
    #fit_param = r"\begin{align*}\mu &= " + mean_str + r"\\ \sigma &= " + sigma_str + r"\\"
    #fit_param += r"\sigma/\mu &= " + res_str + r"\end{align*}"

    #plot legend
    #leg_items = [Line2D([0], [0], lw=2, color="red"), Line2D([0], [0], lw=0)]
    #plt.rc("text", usetex = True)
    #plt.rc('text.latex', preamble='\usepackage{amsmath}')
    #ax.legend(leg_items, ["Gaussian fit", fit_param])

    #simple legend
    leg = legend()
    leg.add_entry(leg_txt(), "alpha: "+str(alpha))
    leg.add_entry(leg_txt(), "p: "+str(pbeam))
    leg.add_entry(leg_txt(), "mu: {0:.4f}".format(pars[0]))
    leg.add_entry(leg_txt(), "sig: {0:.4f}".format(pars[1]))
    leg.add_entry(leg_txt(), "r: {0:.4f}".format(pars[1]/pars[0]))
    leg.draw(ax)

    #output log
    #out = open("out.txt", "w")
    #out.write( "{0:.4f} +/- {1:.4f} | ".format(pars[0], np.sqrt(cov[0,0])) )
    #out.write( "{0:.4f} +/- {1:.4f} | ".format(pars[1], np.sqrt(cov[1,1])) )
    #out.write( "{0:.4f}".format(pars[1]/pars[0]) )
    #out.close()

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

    if res_out:
        return res
    else:
        return pars[0]

#gfit

#_____________________________________________________________________________
def run_sec_fraction():

    #ratios of energy deposition in individual sections

    momentum_data = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10, 20, 30, 50, 75, 100]

    #momentum_mc = [0.5, 1, 2, 5, 10, 30, 75]
    momentum_mc = momentum_data

    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1/HCal_p", ".h5"]
    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x3/HCal_p", ".h5"]
    infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x16/HCal_p", ".h5"]
    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x22/HCal_p", ".h5"]

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fE = []
    f1 = []
    f2 = []
    for p in momentum_mc:

        fE12 = get_sec_fraction(infile[0]+str(p)+infile[1], p)
        fE.append(fE12[0])
        f1.append(fE12[1])
        f2.append(fE12[2])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    #ax.set_title("Fraction of energy deposit in each section")
    ax.set_xlabel("Incident momentum (GeV/c)")
    ax.set_ylabel("(%)")

    ax.set_xscale("log")
    ax.set_ylim([-3, 90])

    plt.xticks(momentum_data, [str(i) for i in momentum_data])

    #data from NIM A290 (1990) 95-108, Table 11
    fAE = [71.7, 64.2, 59.7, 55.5, 53.5, 46.0, 40.1, 36.4, 32.9]
    fA1 = [26.2, 34.9, 38.8, 41.5, 43.7, 51.4, 55.1, 57.2, 59.2]
    fA2 = [2.1, 0.8, 1.5, 3.0, 2.8, 2.6, 4.8, 6.4, 7.9]
    #and from DESY 89-128 (1989) starting at 20 GeV
    fAE += [27.8, 25.8, 23.8, 21.5, 21.1]
    fA1 += [61.8, 61.2, 61.7, 62.1, 62.0]
    fA2 += [10.3, 13.0, 14.5, 16.5, 16.9]

    plt.plot(momentum_mc, fE, "k-", color="blue")
    plt.plot(momentum_mc, f1, "k-", color="red")
    plt.plot(momentum_mc, f2, "k-", color="lime")

    plt.plot(momentum_data, fAE, "o", color="blue")
    plt.plot(momentum_data, fA1, "o", color="red")
    plt.plot(momentum_data, fA2, "o", color="lime")

    #plt.plot(momentum_data, fAE, "k--", color="red")
    #plt.plot(momentum_data, fA1, "k--", color="red")
    #plt.plot(momentum_data, fA2, "k--", color="red")

    #plt.plot(momentum_mc, fE, "o", color="blue")
    #plt.plot(momentum_mc, f1, "o", color="yellow")
    #plt.plot(momentum_mc, f2, "o", color="lime")

    leg = legend()
    leg.add_entry(leg_lin("blue"), "EMC")
    leg.add_entry(leg_lin("red"), "HAC1")
    #leg.add_entry(leg_lin("lime"), "HAC2")
    leg.add_entry(leg_lin("lime"), "HAC2 (all Geant)")
    #leg.add_entry(leg_txt(), "Points: NIM A290 (1990) 95-108, DESY 89-128 (1989) $\geq$20 GeV/c")
    leg.add_entry(leg_txt(), "Points: data")
    leg1 = leg.draw(plt, loc="upper center")

    #leg_items = [Line2D([0], [0], lw=2, ls="-", color="blue"), Line2D([0], [0], lw=0), Line2D([0], [0], lw=2, ls="-", color="red"),
    #    Line2D([0], [0], lw=2, ls="-", color="lime"), Line2D([0], [0], lw=0)]
    #leg_data = ["EMC", "Points: data", "HAC1", "HAC2 (all Geant4)"]
    #leg1 = plt.legend(leg_items, leg_data, ncol=3)

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    leg2i = [leg_txt(), leg_txt()]
    leg2d = ["NIM A290 (1990) 95-108", "DESY 89-128 (1989) $\geq$20 GeV/c"]
    plt.legend(leg2i, leg2d, loc="center right", handletextpad=0)

    plt.gca().add_artist(leg1)

    plt.savefig("01fig.pdf", bbox_inches = "tight")

#run_sec_fraction

#_____________________________________________________________________________
def get_sec_fraction(infile, p):

    #signal fraction in each section

    #inp = read_csv(infile)
    inp = read_hdf(infile)

    sum_all = inp["ucal_edep_EMC"] + inp["ucal_edep_HAC1"] + inp["ucal_edep_HAC2"]
    nall = sum_all.sum()

    nEMC = inp["ucal_edep_EMC"].sum()
    nHAC1 = inp["ucal_edep_HAC1"].sum()
    nHAC2 = inp["ucal_edep_HAC2"].sum()

    fE = 1e2*nEMC/nall
    f1 = 1e2*nHAC1/nall
    f2 = 1e2*nHAC2/nall

    print "{0:5.2f}:  {1:.1f}  {2:.1f}  {3:.1f}".format(p, fE, f1, f2)

    return fE, f1, f2

#get_sec_fraction

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




