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
    funclist.append( fit_alpha ) # 0
    funclist.append( run_eh ) # 1
    funclist.append( run_res ) # 2
    funclist.append( plot_alpha_en ) # 3
    funclist.append( run_eh_abso ) # 4
    funclist.append( gfit ) # 5
    funclist.append( plot_signal ) # 6

    funclist[iplot]()

#_____________________________________________________________________________
def plot_signal():

    #signal for a set of energies

    en = [3, 5, 7, 10, 20, 30, 50] # , 75
    #en = [3, 50]

    inp = ["/home/jaroslav/sim/hcal/data/hcal3c/HCal_en", ".h5"]

    #alpha = run_alpha(inp, en)
    #print alpha

    alpha = [1.2148296593186374, 1.2148296593186374, 1.2248496993987976, 1.2549098196392785, 1.2769539078156313, 1.2729458917835672, 1.3070140280561122]
    #alpha = [1.2148296593186374, 1.3070140280561122]

    nbins = 60

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)

    ax.set_xlabel(r"EM + $\alpha$HAD (GeV)")
    ax.set_ylabel("Normalized counts")

    for i in range(len(en)):

        #data input
        infile = read_hdf(inp[0]+str(en[i])+inp[1])

        #signal
        sum_edep = infile["ecal_edep"] + alpha[i]*infile["hcal_edep_HAD"]
        plt.hist(sum_edep, bins=nbins, color="blue", density=True, histtype="step", lw=1.5)

        #Gaussian fit to the signal
        p0, p1, fitran = gfit(inp[0]+str(en[i])+inp[1], alpha[i], True)
        x = np.linspace(fitran[0], fitran[1], 300)
        y= norm.pdf(x, p0, p1)
        plt.plot(x, y, "k-", color="red", lw=1)

        #label for a given energy
        xpos =  x[ np.where( y==y.max() ) ][0]
        ypos = y[ np.where( y==y.max() ) ][0]
        plt.text(xpos, ypos, r" {0:d} GeV, $\alpha$ = {1:.2f}".format(en[i], alpha[i]), color=col)

    set_grid(plt, col)

    leg = legend()
    leg.add_entry(leg_txt(), "W/ScFi + Fe/Sc (20/3 mm)")
    leg.add_entry(leg_lin("blue"), "FTFP_BERT_HP, 10.7.p01")
    leg.add_entry(leg_lin("red"), "Gaussian fit in $\pm 2\sigma$")
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#plot_signal

#_____________________________________________________________________________
def run_eh_abso():

    #e/h ratio for varying abso

    #abso_z = [12, 14, 16, 18, 20, 22, 24, 26, 28]
    abso_z = [10, 12, 14, 16, 18]

    #scin_z = 3
    scin_z = 5

    #inp_h = ["/home/jaroslav/sim/hcal/data/hcal3d1/HCal_a", ".h5"]
    inp_h = ["/home/jaroslav/sim/hcal/data/hcal3d2/HCal_a", ".h5"]
    inp_e = ["/home/jaroslav/sim/hcal/data/hcal3c1/HCal_en", ".h5"]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    alpha = run_alpha(inp_h, abso_z)

    mean_e, sigma_e = gfit(inp_e[0]+str(10)+inp_e[1], 1.)

    eh = []
    for i in range(len(abso_z)):
        mean_h, sigma_h = gfit(inp_h[0]+str(abso_z[i])+inp_h[1], alpha[i])
        #mean_e, sigma_e = gfit(inp_e[0]+str(en[i])+inp_e[1], 1.)
        eh.append(mean_e/mean_h)
    print eh

    #eh = [1.0858526391044294, 1.1351275132375536, 1.1086482937497302, 1.1194831057553014, 1.115021115675016, 1.1200781329488123, 1.1209093682220816, 1.1289521198274362, 1.141533410214289]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    #ax.set_ylim([0.9, 1.3])
    ax.set_ylim([0.5, 1.3])

    plt.rc("text", usetex = True)
    plt.rc('text.latex', preamble='\usepackage{amsmath}')
    #ax.set_xlabel("abso")
    ax.set_xlabel("Rd")
    ax.set_ylabel("e/h")

    set_axes_color(ax, col)
    set_grid(plt, col)

    #ax.set_xscale("log")
    #plt.xticks(abso_z, [str(i) for i in abso_z])
    Rd = [float(i)/scin_z for i in abso_z]
    #plt.xticks(Rd, ["{0:.1f}".format(i) for i in Rd])
    plt.xticks(Rd, ["{0:.1f} ({1:d}/{2:d})".format(Rd[i], abso_z[i], scin_z) for i in range(len(Rd))])

    #line at e/h = 1
    x = np.linspace(Rd[0], Rd[-1], 300)
    plt.plot(x, [1. for i in x], "k--", color="red", lw=2)

    #plt.plot(abso_z, eh, "o", color="blue")
    plt.plot(Rd, eh, "o", color="blue")

    leg = legend()
    leg.add_entry(leg_txt(), "scin\_z: {0:d}".format(scin_z))
    #leg.add_entry(leg_lin("red", "--"), "e/h = 1")
    leg.add_entry(leg_dot(fig, "blue"), "FTFP\_BERT\_HP, 10.7.p01")
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#run_eh_abso

#_____________________________________________________________________________
def plot_alpha_en():

    #minimal alpha as a function of energy

    en = [3, 5, 7, 10, 20, 30, 50, 75]
    inp = ["/home/jaroslav/sim/hcal/data/hcal3c/HCal_en", ".h5"]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    alpha = run_alpha(inp, en)
    print alpha

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)

    ax.set_xscale("log")
    plt.xticks(en, [str(i) for i in en])

    ax.set_xlabel("E (GeV)")
    ax.set_ylabel("alpha")

    ax.set_ylim([1, 1.4])

    plt.grid(True, color = col, linewidth = 0.5, linestyle = "--")

    plt.plot(en, alpha, marker="o", linestyle="", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#plot_alpha_en

#_____________________________________________________________________________
def run_res():

    #energy resolution as a function of energy

    #GeV
    #en = [6, 8, 12, 16, 25, 32, 64]
    en = [3, 5, 7, 10, 20, 30, 50, 75]
    #en = [3, 5]

    inp = ["/home/jaroslav/sim/hcal/data/hcal3c/HCal_en", ".h5"]
    #inp = ["/home/jaroslav/sim/hcal/data/hcal3c1/HCal_en", ".h5"]
    #inp = ["/home/jaroslav/sim/hcal/data/hcal3c2/HCal_en", ".h5"]
    #inp = ["/home/jaroslav/sim/hcal/data/hcal3c3/HCal_en", ".h5"]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    alpha = run_alpha(inp, en)
    print alpha

    #resolution as sigma/mean
    res = [ms[1]/ms[0] for ms in [gfit(inp[0]+str(en[i])+inp[1], alpha[i]) for i in range(len(en))]]
    #res = [ms[1]/ms[0] for ms in [gfit(inp[0]+str(en[i])+inp[1], 1) for i in range(len(en))]]

    print res

    #res = [0.18536713994367082, 0.15090768986862743, 0.12602019940767245, 0.11164185039212438, 0.09165626367846519, 0.08308090453575402, 0.07590065737234164, 0.07221679796791246]

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
    leg.add_entry(leg_txt(), "W/ScFi + Fe/Sc (20/3 mm)")
    #leg.add_entry(leg_txt(), "W/ScFi (17cm, 10$^\circ$/1$^\circ$)")
    #leg.add_entry(leg_txt(), "+ Fe/Sc (20/3 mm)")
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
    en = [3, 5, 7, 10, 20, 30, 50, 75]

    #inp_h = ["/home/jaroslav/sim/hcal/data/hcal3c/HCal_en", ".h5"]
    #inp_h = ["/home/jaroslav/sim/hcal/data/hcal3c2/HCal_en", ".h5"]
    inp_h = ["/home/jaroslav/sim/hcal/data/hcal3c3/HCal_en", ".h5"]
    inp_e = ["/home/jaroslav/sim/hcal/data/hcal3c1/HCal_en", ".h5"]

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    #alpha = run_alpha(inp_h, en)

    #eh = []
    #for i in range(len(en)):
    #    mean_h, sigma_h = gfit(inp_h[0]+str(en[i])+inp_h[1], alpha[i])
    #    mean_e, sigma_e = gfit(inp_e[0]+str(en[i])+inp_e[1], 1.)
    #    eh.append(mean_e/mean_h)
    #print eh

    #eh = [1.1843121055569938, 1.1712184048681817, 1.1510946757405278, 1.1299514803026915, 1.115021115675016, 1.1142540693206178, 1.0940572767145802, 1.0858602110652527]

    eh = [1.0783978255818747, 1.0470998098908393, 1.0095102295698088, 0.9892973774844975, 0.9610145332516115, 0.951324266586261, 0.9394926546022618, 0.9310279185588818]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_ylim([0.9, 1.3])

    #plt.rc("text", usetex = True)
    #plt.rc('text.latex', preamble='\usepackage{amsmath}')
    ax.set_xlabel("Incident energy $E$ (GeV)")
    ax.set_ylabel("e/h")

    set_axes_color(ax, col)
    set_grid(plt, col)

    ax.set_xscale("log")
    plt.xticks(en, [str(i) for i in en])

    #line at e/h = 1
    x = np.linspace(en[0], en[-1], 300)
    plt.plot(x, [1. for i in x], "k--", color="red", lw=2)

    plt.plot(en, eh, "o", color="blue")

    leg = legend()
    leg.add_entry(leg_txt(), "W/ScFi + Fe/Sc (20/3 mm)")
    leg.add_entry(leg_dot(fig, "blue"), "FTFP_BERT_HP, 10.7.p01")
    leg.add_entry(leg_lin("red", "--"), "e/h = 1")
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#run_eh


#_____________________________________________________________________________
def run_alpha(inp=None, en=None):

    alpha_min = [fit_alpha(inp[0]+str(i)+inp[1]) for i in en]

    return alpha_min

#run_alpha

#_____________________________________________________________________________
def fit_alpha(infile=None):

    #Gaussian fit for a given alpha

    #alpha = [1]
    alpha = [0.8, 1., 1.2, 1.4, 1.6, 1.8]
    #alpha = [0.4, 0.6, 0.8, 1., 1.2, 1.4, 1.6, 1.8]
    #alpha = [0.2, 0.4, 0.6, 0.8, 1., 1.2, 1.4, 1.6]

    #infile = "/home/jaroslav/sim/hcal/data/hcal3c/HCal_en50.h5"
    #infile = "/home/jaroslav/sim/hcal/data/hcal3d2/HCal_a16.h5"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    res = []
    for a in alpha:
        mean, sigma = gfit(infile, a)
        res.append( sigma/mean )

        #print a, res

    #return

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_xlabel("alpha")
    ax.set_ylabel("Resolution")

    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(alpha, res, "o", color="blue")

    #polynomial fit
    pars, cov = curve_fit(poly_alpha, alpha, res)
    x = np.linspace(alpha[0], alpha[-1], 500)
    y = poly_alpha(x, pars[0], pars[1], pars[2], pars[3])
    plt.plot(x, y, "k-", color="red")

    #minimal alpha
    alpha_min = x[ np.where( y==y.min() ) ][0]
    print "alpha_min:", alpha_min

    leg = legend()
    leg.add_entry(leg_txt(), (infile.split("/"))[-1])
    leg.add_entry(leg_lin("blue"), "a + b*alpha + c*alpha^2 + d*alpha^3")
    leg.add_entry(leg_txt(), "a: {0:.4f} +/- {1:.4f}".format( pars[0], np.sqrt(cov[0,0]) ))
    leg.add_entry(leg_txt(), "b: {0:.4f} +/- {1:.4f}".format( pars[1], np.sqrt(cov[1,1]) ))
    leg.add_entry(leg_txt(), "c: {0:.4f} +/- {1:.4f}".format( pars[2], np.sqrt(cov[2,2]) ))
    leg.add_entry(leg_txt(), "d: {0:.4f} +/- {1:.4f}".format( pars[3], np.sqrt(cov[3,3]) ))
    leg.add_entry(leg_txt(), "alpha_min: {0:.4f}".format( alpha_min ))
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

    return alpha_min

#fit_alpha

#_____________________________________________________________________________
def poly_alpha(alpha, a, b, c, d):

    #polynomial fit to resolution as a function of alpha
    return a + b*alpha + c*alpha**2 + d*alpha**3

#poly_alpha

#_____________________________________________________________________________
def gfit(infile=None, alpha=None, put_fitran=False):

    #Gaussian fit for energy resolution at a given energy

    #infile = "/home/jaroslav/sim/hcal/data/hcal3c/HCal_en50.h5"
    #alpha = 1.3

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
    hx = plt.hist(sum_edep, bins=nbins, color="blue", density=True, histtype="step", lw=2)

    #nh = np.histogram(sum_edep, bins=nbins, density=True)
    #plt.plot(nh[1][1:], nh[0], ls="steps")

    #bin centers for the fit
    centers = (0.5*(hx[1][1:]+hx[1][:-1]))

    #pass1, fit over the full range
    fit_data = DataFrame({"E": centers, "density": hx[0]})
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), fit_data["E"], fit_data["density"])

    #print "pass1:", pars[0], pars[1]

    #pass2, fit in +/- 2*sigma range
    smax = 2
    fitran = [pars[0] - smax*pars[1], pars[0] + smax*pars[1]] # fit range at 2*sigma
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
    leg.add_entry(leg_txt(), (infile.split("/"))[-1])
    leg.add_entry(leg_txt(), "alpha: "+str(alpha))
    leg.add_entry(leg_txt(), "mu: {0:.4f}".format(pars[0]))
    leg.add_entry(leg_txt(), "sig: {0:.4f}".format(pars[1]))
    leg.add_entry(leg_txt(), "r: {0:.4f}".format(pars[1]/pars[0]))
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

    if put_fitran is True:
        return pars[0], pars[1], fitran

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





