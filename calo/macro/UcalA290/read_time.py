#!/usr/bin/python

#time distribution of steps in event

import ROOT as rt
from ROOT import gROOT, TFile, TH1F

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame

#_____________________________________________________________________________
def main():

    #data directory
    #basedir = "/home/jaroslav/sim/lmon/calo/macro"
    basedir = "/home/jaroslav/sim/hcal/data/ucal1a1x18"

    #infile = basedir + "/lmon.root"
    infile = basedir + "/lmon_p75.root"

    iplot = 1
    funclist = []
    funclist.append( plot_single ) # 0
    funclist.append( plot_mean ) # 1

    #lmon input
    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("DetectorTree")

    funclist[iplot]()

#main

#_____________________________________________________________________________
def plot_mean():

    #mean time in each bin over all events

    #initialize
    hT = TH1F()
    tree.SetBranchAddress("ucal_time_step", hT)
    tree.GetEntry(0)
    nev = tree.GetEntries()
    data = {i:np.zeros(nev) for i in range(1, hT.GetNbinsX()+1)}
    x = [hT.GetBinLowEdge(i)+0.5*hT.GetBinWidth(i) for i in range(1, hT.GetNbinsX()+1)]
    x2 = [j for i in range(1, hT.GetNbinsX()+1) for j in (hT.GetBinLowEdge(i), hT.GetBinLowEdge(i)+hT.GetBinWidth(i))]
    #print x2

    #tree loop
    for iev in range(tree.GetEntriesFast()):
        tree.GetEntry(iev)

        for ibin in range(1, hT.GetNbinsX()+1):
            dat_bin = data[ibin]
            dat_bin[iev] = hT.GetBinContent(ibin)

    df = DataFrame(data)
    #print df

    #mean at each bin
    mean_time = [df[i].mean() for i in range(1,len(x)+1)]
    mean_time2 = [j for i in mean_time for j in (i, i)]
    #print mean_time2

    plt.style.use("dark_background")
    col = "lime"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    set_axes_color(ax, col)
    set_grid(plt, col)

    #plt.plot(x, mean_time, ls="steps", color="blue")
    plt.plot(x2, mean_time2, ls="steps", color="blue")

    fig.savefig("01fig.pdf", bbox_inches = "tight")

#plot_mean

#_____________________________________________________________________________
def plot_single():

    #time in a single event
    iev = 3

    hT = TH1F()
    tree.SetBranchAddress("ucal_time_step", hT)

    #for i in range(tree.GetEntriesFast()):
    #    tree.GetEntry(i)
    #    print hT.GetEntries()

    tree.GetEntry(iev)
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

#plot_single





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




















