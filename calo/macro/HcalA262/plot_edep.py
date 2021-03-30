#!/usr/bin/python

from pandas import read_csv, DataFrame, read_hdf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import norm
from scipy.optimize import curve_fit
import numpy as np
import collections

import os
from math import ceil

#_____________________________________________________________________________
def main():

    #infile = "HCal.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2a/piPos_en10_12kevt/HCal.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2a/el_en3_12kevt/HCal.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2ax1/HCal_el_en3_12kevt.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2ax2/HCal_en3.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2ax2/HCal_en10.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2ax2/HCal_en50.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2ax3/HCal_en3.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2ax4/HCal_en10.csv"
    #infile = "/home/jaroslav/sim/lmon-lite/calo/macro/HCal_1200.csv"
    #infile = "/home/jaroslav/sim/lmon-lite/calo/macro/HCal_en75_1200.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2b/HCal_en50.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2bx1/HCal_en50.csv"
    #infile = "/home/jaroslav/sim/hcal/data/hcal2c/HCal_en10.csv"
    infile = "/home/jaroslav/sim/hcal/data/hcal2c/HCal_en50.csv"

    iplot = 4
    funclist = []
    funclist.append( fit_err_sum ) # 0
    funclist.append( fit_err_sum_all ) # 1
    funclist.append( plot_EM ) # 2
    funclist.append( fit_range ) # 3
    funclist.append( plot_shower_shape ) # 4

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
    prim_en = "x"

    global inp

    #separate input
    if infile is not None:
        global inp
        inp = read_csv(infile)
        prim_en = str(en)

    #inp = inp[inp["hcal_edep_EM"] > 0.2]

    sum_edep = inp["hcal_edep_EM"] + inp["hcal_edep_HAD"]
    #sum_edep = inp["hcal_edep"]

    nbins = 60

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

    ax.set_xlabel("EM + HAD (GeV)")
    ax.set_ylabel("Counts / {0:.3f} GeV".format((xmax-xmin)/nbins))

    mean_str = "{0:.4f} \pm {1:.4f}".format(pars[0], np.sqrt(cov[0,0]))
    sigma_str = "{0:.4f} \pm {1:.4f}".format(pars[1], np.sqrt(cov[1,1]))
    res_str = "{0:.4f}".format(pars[1]/pars[0])
    fit_param = r"\begin{align*}\mu &= " + mean_str + r"\\ \sigma &= " + sigma_str + r"\\"
    fit_param += r"\sigma/\mu &= " + res_str + r"\end{align*}"

    #plot legend
    leg_items = [Line2D([0], [0], lw=0), Line2D([0], [0], lw=2, color="red"), Line2D([0], [0], lw=0)]
    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    #ax.legend(leg_items, ["$E(\pi^+)$ = "+str(prim_en)+" GeV", "Gaussian fit", fit_param])
    ax.legend(leg_items, ["$E$ = "+str(prim_en)+" GeV", "Gaussian fit", fit_param])

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
def fit_err_sum_all():

    #run the fit_err_sum function with a set of inputs

    #input
    en = [3, 5, 7, 10, 20, 30, 50, 75]
    #en = [10, 20, 30, 50, 75]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2a/el_en", "_12kevt/HCal.csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2ax1/HCal_el_en", "_12kevt.csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2ax2/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2ax3/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2ax4/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2b/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2bx1/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2bx2/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2bx3/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2bx4/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2c/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2cx1/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2cx2/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2cx3/HCal_en", ".csv"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2cx4/HCal_en", ".csv"]
    infile = ["/home/jaroslav/sim/hcal/data/hcal2c2/HCal_en", ".csv"]

    #template for output
    outfile = "edep_"
    #outfile = "edep_hcal2bx3_"

    #output log
    out = open("out_all.txt", "w")
    enres = ["en = [", "res = ["]

    #loop over energies
    for e in en:

        #pars, cov = fit_err_sum(infile[0]+str(e)+infile[1], outfile+str(e)+".pdf", e)
        pars, cov = fit_range(infile[0]+str(e)+infile[1], outfile+str(e)+".pdf", e)

        #out.write(str(e)+" | ")
        #out.write( "{0:.4f} +/- {1:.4f} | ".format(pars[0], np.sqrt(cov[0,0])) )
        #out.write( "{0:.4f} +/- {1:.4f} | ".format(pars[1], np.sqrt(cov[1,1])) )
        #out.write( "{0:.4f}\n".format(pars[1]/pars[0]) )
        out.write(str(e)+" & ")
        out.write( "{0:.4f} $\pm$ {1:.4f} & ".format(pars[0], np.sqrt(cov[0,0])) )
        out.write( "{0:.4f} $\pm$ {1:.4f} & ".format(pars[1], np.sqrt(cov[1,1])) )
        out.write( "{0:.4f}\\\\\n".format(pars[1]/pars[0]) )
        enres[0] += str(e) + ", "
        enres[1] += "{0:.4f}, ".format(pars[1]/pars[0])

    out.write("\n")
    for i in range(len(enres)):
        out.write( enres[i][:-2] + "]\n" )

    out.close()

#fit_err_sum_all

#_____________________________________________________________________________
def fit_range(infile=None, outfile=None, en=None):

    #fit in selected range

    #primary energy for legend, GeV
    prim_en = "x"

    global inp

    #separate input
    if infile is not None:
        global inp
        inp = read_csv(infile)
        prim_en = str(en)

    sum_edep = inp["hcal_edep_EM"] + inp["hcal_edep_HAD"]
    #sum_edep = inp["hcal_edep"]

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

    ax.set_xlabel("EM + HAD (GeV)")
    ax.set_ylabel("Counts / {0:.3f} GeV".format((plt.xlim()[1]-plt.xlim()[0])/nbins))

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    mean_str = "{0:.4f} \pm {1:.4f}".format(pars[0], np.sqrt(cov[0,0]))
    sigma_str = "{0:.4f} \pm {1:.4f}".format(pars[1], np.sqrt(cov[1,1]))
    res_str = "{0:.4f}".format(pars[1]/pars[0])
    fit_param = r"\begin{align*}\mu &= " + mean_str + r"\\ \sigma &= " + sigma_str + r"\\"
    fit_param += r"\sigma/\mu &= " + res_str + r"\end{align*}"

    #plot legend
    leg_items = [Line2D([0], [0], lw=0), Line2D([0], [0], lw=2, color="red"), Line2D([0], [0], lw=0)]
    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    ax.legend(leg_items, ["$E$ = "+str(prim_en)+" GeV", "Gaussian fit", fit_param])

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

#fit_range

#_____________________________________________________________________________
def plot_EM():

    #energy in EM section

    nbins = 60
    emax = 2
    #emax = 0.3

    #primary energy for legend, GeV
    #prim_en = "10"
    prim_en = "50"

    #global inp
    #inp = inp[inp["hcal_edep_EM"] > 0.05]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)

    #data plot
    hx = plt.hist(inp["hcal_edep_EM"], bins = nbins, range=(0, emax), color = "blue", density = False, label = "edep")

    ax.set_xlabel("EM (GeV)")
    ax.set_ylabel("Counts")

    set_grid(plt, col)

    leg_items = [Line2D([0], [0], lw=0)]
    ax.legend(leg_items, ["Energy in EM section (E = "+prim_en+" GeV)"])

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#plot_EM

#_____________________________________________________________________________
def plot_shower_shape():

    #input
    en = {3:"blue", 5:"magenta", 7:"lime", 10:"gold", 20:"darkviolet", 30:"orange", 50:"cyan", 75:"red"}
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2c2/HCal_en", ".h5"]
    #infile = ["/home/jaroslav/sim/hcal/data/hcal2cx5/HCal_en", ".h5"]
    infile = ["/home/jaroslav/sim/hcal/data/hcal2cx6/HCal_en", ".h5"]

    #geometry for scintillator plates
    z0 = 11.75 # mm, center of the first scintillator
    dz = 13.5 # mm, total layer thickness along z
    nlay = 97 # all layers

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    leg_items = []
    leg_val = []

    #sort by energy
    en = collections.OrderedDict(sorted(en.items()))

    #loop over energies
    for e in en.iterkeys():

        #input for a given energy
        #df = read_csv(infile[0]+str(e)+infile[1])
        df = read_hdf(infile[0]+str(e)+infile[1])

        #layer positions and energies
        zlay = []
        elay = []

        #loop over layers
        for ilay in range(nlay):

            zlay.append( z0 + ilay*dz )
            elay.append( df["hcal_edep_layer"+str(ilay)].mean() )

        #plot for a given energy
        plt.plot(zlay, elay, ls="steps", color=en[e])

        #legend for a given energy
        leg_items.append(Line2D([0], [0], lw=2, color=en[e]))
        leg_val.append("$E(\pi^+)$ = "+str(e)+" GeV")

    ax.legend(leg_items, leg_val)

    ax.set_title("Shower profile for HcalA262")
    ax.set_xlabel("Longitudinal position $z$ (mm)")
    ax.set_ylabel("Mean energy in layer (GeV)")

    plt.savefig("01fig.pdf", bbox_inches = "tight")

#plot_shower_shape

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



















