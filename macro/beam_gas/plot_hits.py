#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 0

    func = {}
    func[0] = hit_phot_en

    func[iplot]()

#main

#_____________________________________________________________________________
def hit_phot_en():

    #hit probability as a function of generated photon energy

    #infile = "/home/jaroslav/sim/lmon/data/beam-gas/bg3d/rc.root"
    infile = "/home/jaroslav/sim/lmon/data/beam-gas/bg3e/rc.root"

    emin = -6
    emax = 2

    pmin = 1e-4
    pmax = 0.15

    inp = TFile.Open(infile)
    tree = inp.Get("event")

    hp = rt.acc_Q2_kine(tree, "phot_en", "is_hit")
    #hp = rt.acc_Q2_kine(tree, "el_en", "is_hit")
    hp.modif = 1 # for log_10(phot_en)
    hp.prec = 0.1
    hp.delt = 1e-2
    #hp.nev = 100000
    ghp = hp.get()

    #can = ut.box_canvas()
    #frame = gPad.DrawFrame(emin, pmin, emax, pmax)

    #ut.put_yx_tit(frame, "Hit probability", "Photon energy #it{E} (GeV)", 1.6, 1.3)

    #frame.Draw()

    #ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    #ut.set_graph(ghp, rt.kBlue)
    #ghp.Draw("psame")

    #gPad.SetLogy()

    #gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    #can.SaveAs("01fig.pdf")

    xp, yp = ut.graph_to_arrays(ghp)

    #plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(xp, yp, "-", color="blue", lw=1)

    ax.set_xlabel("Generated photon energy $E_\gamma$ (keV)")
    ax.set_ylabel("Hit probability")

    ax.set_yscale("log")

    plt.xticks(ax.get_xticks()[1:-1], ["$10^{"+"{0:.0f}".format(i+6)+"}$" for i in ax.get_xticks()[1:-1]])

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#hit_phot_en

#_____________________________________________________________________________
def set_axes_color(ax, col):

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

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    main()























