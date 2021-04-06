#!/usr/bin/python

#time distribution of steps in event

import ROOT as rt
from ROOT import gROOT, TFile, TH1F

import matplotlib.pyplot as plt

#_____________________________________________________________________________
def main():

    #data directory
    basedir = "/home/jaroslav/sim/lmon/calo/macro"

    infile = basedir + "/lmon.root"

    #lmon input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    hT = TH1F()
    tree.SetBranchAddress("ucal_time_step", hT)

    #for i in range(tree.GetEntriesFast()):
    #    tree.GetEntry(i)
    #    print hT.GetEntries()

    tree.GetEntry(11)
    x = [hT.GetBinLowEdge(i)+0.5*hT.GetBinWidth(i) for i in range(1, hT.GetNbinsX()+1)]
    bins = [hT.GetBinContent(i) for i in range(1, hT.GetNbinsX()+1)]

    plt.style.use("dark_background")
    col = "lime"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(x, bins, "o", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#main





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

    gROOT.SetBatch()

    main()




















