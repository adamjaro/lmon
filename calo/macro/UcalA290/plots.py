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

    iplot = 4
    funclist = []
    funclist.append( run_alpha ) # 0
    funclist.append( run_sec_fraction ) # 1
    funclist.append( fit_alpha ) # 2
    funclist.append( momentum_alpha ) # 3
    funclist.append( momentum_res ) # 4

    funclist[iplot]()

#_____________________________________________________________________________
def momentum_res():

    #energy resolution as a function of beam momentum

    momentum = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10]
    momentum += [20, 30, 50, 75, 100]

    infile = ["/home/jaroslav/sim/hcal/data/ucal1a1/HCal_p", ".h5"]  # +str(pbeam)+
    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x2/HCal_p", ".h5"]

    #alpha_min = [1.0438877755511022, 0.7769539078156313, 0.7246492985971944, 0.7336673346693388, 0.7498997995991985, 0.7444889779559118, 0.7589178356713426, 0.7553106212424849, 0.7733466933867736]
    alpha_min = [1.0438877755511022, 0.7769539078156313, 0.7246492985971944, 0.7336673346693388, 0.7498997995991985, 0.7444889779559118, 0.7589178356713426, 0.7553106212424849, 0.7733466933867736, 0.7985971943887775, 0.8148296593186373, 0.8292585170340682, 0.8418837675350701, 0.8581162324649299]
    #alpha_min = [1.04749498997996, 0.7733466933867736, 0.7228456913827656, 0.7318637274549098, 0.7535070140280562, 0.7462925851703407, 0.7589178356713426, 0.7589178356713426, 0.7697394789579158, 0.7931863727454911, 0.8112224448897796, 0.8364729458917837, 0.8454909819639278, 0.8581162324649299]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    res = []
    for i in range(len(momentum)):
        inp = read_hdf(infile[0]+str(momentum[i])+infile[1])
        res.append( gfit(inp, alpha_min[i], momentum[i]) )

    print res

    #res = [0.378309214646451, 0.330370519825307, 0.2980614162915459, 0.2565883204529302, 0.23708631123491672, 0.20745290032813926, 0.18080942863875213, 0.16890713625696185, 0.15452339236086574]

    res = [1e2*sqrt(momentum[i])*res[i] for i in range(len(res))]

    #print res

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(momentum, res, "o", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#_____________________________________________________________________________
def momentum_alpha():

    #minimal alpha as a function of beam momentum

    momentum = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10]
    momentum += [20, 30, 50, 75, 100]

    #momentum = [10]

    alpha = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    alpha_min = []
    for p in momentum:
        alpha_min.append( fit_alpha(alpha, p) )

    print alpha_min

    #alpha_min = [1.0438877755511022, 0.7769539078156313, 0.7246492985971944, 0.7336673346693388, 0.7498997995991985, 0.7444889779559118, 0.7589178356713426, 0.7553106212424849, 0.7733466933867736]
    #alpha_min = [1.0438877755511022, 0.7769539078156313, 0.7246492985971944, 0.7336673346693388, 0.7498997995991985, 0.7444889779559118, 0.7589178356713426, 0.7553106212424849, 0.7733466933867736, 0.7985971943887775, 0.8148296593186373, 0.8292585170340682, 0.8418837675350701, 0.8581162324649299]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(momentum, alpha_min, "o", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#_____________________________________________________________________________
def fit_alpha(alpha=None, pbeam=None):

    #polynomial fit for resolution as a function of alpha

    #alpha = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2]

    #res = [1.6095357603323173, 1.1914606471540563, 0.9766833753243835, 0.8965160801980067, 0.8941847587425313, 0.9335774779851417, 1.0, 1.0767531351804083, 1.1561039821761605]
    res = run_alpha(alpha, pbeam)

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

    plt.plot(alpha, res, "o", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")

    return alpha_min

#_____________________________________________________________________________
def poly_alpha(r, a, b, c, d):

    #polynomial fit to resolution as a function of alpha

    #return a*r**2 + b*r + c
    return a + b*r + c*r**2 + d*r**3

#_____________________________________________________________________________
def run_alpha(alpha=None, pbeam=None):

    #Gaussian fit for a given alpha

    #alpha = [0.8, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15]
    #alpha = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2]
    #alpha = [1]

    #infile = "/home/jaroslav/sim/hcal/data/ucal1a1/HCal_p10.csv"
    #infile = "/home/jaroslav/sim/hcal/data/ucal1a1x1/HCal_p10.csv"
    #infile = "/home/jaroslav/sim/hcal/data/ucal1a2/HCal_p10.csv"

    #inp = read_hdf("/home/jaroslav/sim/hcal/data/ucal1a1/HCal_p"+str(pbeam)+".h5")
    inp = read_hdf("/home/jaroslav/sim/hcal/data/ucal1a1x2/HCal_p"+str(pbeam)+".h5")

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

    return res

#run_alpha

#_____________________________________________________________________________
def gfit(inp, alpha, pbeam=None):

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

    print "pass1:", pars[0], pars[1]

    #pass2, fit in +/- 2*sigma range
    fitran = [pars[0] - 2.*pars[1], pars[0] + 2.*pars[1]] # fit range at 2*sigma
    fit_data = fit_data[ fit_data["E"].between(fitran[0], fitran[1], inclusive=False) ] # select the data to the range
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), fit_data["E"], fit_data["density"])

    print "pass2:", pars[0], pars[1]

    #fit function
    x = np.linspace(fitran[0], fitran[1], 300)
    y = norm.pdf(x, pars[0], pars[1])

    plt.plot(x, y, "k-", label="norm", color="red")

    ax.set_xlabel("Calorimeter signal (GeV)")
    ax.set_ylabel("Counts / {0:.3f} GeV".format((plt.xlim()[1]-plt.xlim()[0])/nbins))

    ax.set_title("alpha: "+str(alpha)+", p: "+str(pbeam))

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
    plt.close()

    return res

#gfit

#_____________________________________________________________________________
def run_sec_fraction():

    #ratios of energy deposition in individual sections

    momentum = [0.5, 0.75, 1, 1.5, 2, 3, 5, 7, 10]
    p2 = [20, 30, 50, 75, 100]
    #momentum = [10]
    momentum += p2

    infile = ["/home/jaroslav/sim/hcal/data/ucal1a1/HCal_p", ".h5"]
    #infile = ["/home/jaroslav/sim/hcal/data/ucal1a1x2/HCal_p", ".h5"]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fE = []
    f1 = []
    f2 = []
    for p in momentum:

        fE12 = get_sec_fraction(infile[0]+str(p)+infile[1], p)
        fE.append(fE12[0])
        f1.append(fE12[1])
        f2.append(fE12[2])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    #momentum_plot = [log10(i) for i in momentum]

    #print momentum_plot

    ax.set_xscale("log")

    #data from NIM A290 (1990) 95-108, Table 11
    fAE = [71.7, 64.2, 59.7, 55.5, 53.5, 46.0, 40.1, 36.4, 32.9]
    fA1 = [26.2, 34.9, 38.8, 41.5, 43.7, 51.4, 55.1, 57.2, 59.2]
    fA2 = [2.1, 0.8, 1.5, 3.0, 2.8, 2.6, 4.8, 6.4, 7.9]
    #and from DESY 89-128 (1989) starting at 20 GeV
    fAE += [27.8, 25.8, 23.8, 21.5, 21.1]
    fA1 += [61.8, 61.2, 61.7, 62.1, 62.0]
    fA2 += [10.3, 13.0, 14.5, 16.5, 16.9]


    plt.plot(momentum, fAE, "k--", color="red")
    plt.plot(momentum, fA1, "k--", color="red")
    plt.plot(momentum, fA2, "k--", color="red")

    plt.plot(momentum, fE, "o", color="blue")
    plt.plot(momentum, f1, "o", color="yellow")
    plt.plot(momentum, f2, "o", color="lime")

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




