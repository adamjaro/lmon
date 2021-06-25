#!/usr/bin/python3

from pandas import read_csv, DataFrame
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import norm
from scipy.optimize import curve_fit
import numpy as np

#_____________________________________________________________________________
def main():

    iplot = 2
    funclist = []
    funclist.append( plot_x ) # 0
    funclist.append( plot_y ) # 1
    funclist.append( plot_z ) # 2

    funclist[iplot]()

#main

#_____________________________________________________________________________
def plot_x():

    #x of primary vertex

    infile = "data/vtx_18x275_3p3_r2.csv"
    #infile = "data/vtx_18x275_3p4.csv"

    inp = read_csv(infile)

    #print(inp)

    nbins = 60

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = plt.hist(inp["x"], bins=nbins, color="blue", density=True, histtype="step", lw=2)

    #Gaussian fit, bin centers and values
    centers = (0.5*(hx[1][1:]+hx[1][:-1]))
    fit_data = DataFrame({"E": centers, "density": hx[0]})
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), fit_data["E"], fit_data["density"])

    #fit function
    x = np.linspace(plt.xlim()[0], plt.xlim()[1], 300)
    y = norm.pdf(x, pars[0], pars[1])
    plt.plot(x, y, "-", label="norm", color="red")

    ax.set_xlabel("$x$ (mm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_lin("red"), "Gaussian fit:")
    leg.add_entry(leg_txt(), "$\mu$ (mm): {0:.4f} $\pm$ {1:.4f}".format( pars[0], np.sqrt(cov[0,0]) ))
    leg.add_entry(leg_txt(), "$\sigma$ (mm): {0:.4f} $\pm$ {1:.4f}".format( pars[1], np.sqrt(cov[1,1]) ))
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#plot_x

#_____________________________________________________________________________
def plot_y():

    #y of primary vertex

    infile = "data/vtx_18x275_3p3_r2.csv"
    #infile = "data/vtx_18x275_3p4.csv"

    inp = read_csv(infile)

    nbins = 60

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = plt.hist(inp["y"], bins=nbins, color="blue", density=True, histtype="step", lw=2)

    #Gaussian fit, bin centers and values
    centers = (0.5*(hx[1][1:]+hx[1][:-1]))
    fit_data = DataFrame({"E": centers, "density": hx[0]})
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), fit_data["E"], fit_data["density"])

    #fit function
    x = np.linspace(plt.xlim()[0], plt.xlim()[1], 300)
    y = norm.pdf(x, pars[0], pars[1])
    plt.plot(x, y, "-", label="norm", color="red")

    plt.rc("text", usetex = True)
    plt.rc("text.latex", preamble=r"\usepackage{siunitx}")

    ax.set_xlabel("$y$ (mm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_lin("red"), "Gaussian fit:")
    leg.add_entry(leg_txt(), "$\mu$ (\si{\micro\meter}): "+"{0:.4f} $\pm$ {1:.4f}".format( pars[0]*1e3, np.sqrt(cov[0,0]*1e3) ))
    leg.add_entry(leg_txt(), "$\sigma$ (\si{\micro\meter}): "+"{0:.4f} $\pm$ {1:.4f}".format( pars[1]*1e3, np.sqrt(cov[1,1]*1e3) ))
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#plot_y

#_____________________________________________________________________________
def plot_z():

    #z of primary vertex

    infile = "data/vtx_18x275_3p3_r2.csv"
    #infile = "data/vtx_18x275_3p4.csv"

    inp = read_csv(infile)

    nbins = 50

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = plt.hist(inp["z"], bins=nbins, color="blue", density=True, histtype="step", lw=2)

    #Gaussian fit, bin centers and values
    centers = (0.5*(hx[1][1:]+hx[1][:-1]))
    fit_data = DataFrame({"E": centers, "density": hx[0]})
    pars, cov = curve_fit(lambda x, mu, sig : norm.pdf(x, loc=mu, scale=sig), fit_data["E"], fit_data["density"])

    #fit function
    x = np.linspace(plt.xlim()[0], plt.xlim()[1], 300)
    y = norm.pdf(x, pars[0], pars[1])
    plt.plot(x, y, "-", label="norm", color="red")

    ax.set_xlabel("$z$ (mm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_lin("red"), "Gaussian fit:")
    leg.add_entry(leg_txt(), "$\mu$ (mm): {0:.3f} $\pm$ {1:.3f}".format( pars[0], np.sqrt(cov[0,0]) ))
    leg.add_entry(leg_txt(), "$\sigma$ (mm): {0:.3f} $\pm$ {1:.3f}".format( pars[1], np.sqrt(cov[1,1]) ))
    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#plot_z

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


















