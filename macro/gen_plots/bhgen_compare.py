#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    funclist = {}
    funclist[0] = el_en
    funclist[1] = el_pitheta
    funclist[2] = el_phi

    funclist[iplot]()

#main

#_____________________________________________________________________________
def el_en():

    #electron energy

    #GeV
    xmin = 0
    xmax = 19
    xbin = 0.1

    inp1 = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5_100Mevt/evt.root"
    inp2 = "/home/jaroslav/sim/GETaLM_data/lumi/lumi_18x275_Lif_emin0p5_T3p3_10Mevt.root"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    h1 = make_h1(inp1, "bhgen_tree", "el_en", xbin, xmin, xmax)
    h2 = make_h1(inp2, "ltree", "true_el_E", xbin, xmin, xmax)

    plt.plot(h1[0], h1[1], "-", color="red", lw=1)
    plt.plot(h2[0], h2[1], "--", color="blue", lw=1)

    ax.set_xlabel(r"$E_e$ (GeV)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#el_en

#_____________________________________________________________________________
def el_pitheta():

    #electron pi - theta in mrad

    #mrad
    xmin = 0
    xmax = 20
    xbin = 0.05

    inp1 = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5_100Mevt/evt.root"
    inp2 = "/home/jaroslav/sim/GETaLM_data/lumi/lumi_18x275_Lif_emin0p5_T3p3_10Mevt.root"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    h1 = make_h1(inp1, "bhgen_tree", "(TMath::Pi()-el_theta)*1e3", xbin, xmin, xmax)
    h2 = make_h1(inp2, "ltree", "(TMath::Pi()-true_el_theta)*1e3", xbin, xmin, xmax)

    plt.plot(h1[0], h1[1], "-", color="red", lw=1)
    plt.plot(h2[0], h2[1], "--", color="blue", lw=1)

    ax.set_xlabel(r"$\pi-\theta_e$ (mrad)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#el_pitheta

#_____________________________________________________________________________
def el_phi():

    #electron phi in rad

    #rad
    xbin = 0.01
    xmin = -3.5
    xmax = 3.5

    inp1 = "/home/jaroslav/sim/bhgen/data/g18x275_emin0p5_100Mevt/evt.root"
    inp2 = "/home/jaroslav/sim/GETaLM_data/lumi/lumi_18x275_Lif_emin0p5_T3p3_10Mevt.root"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    h1 = make_h1(inp1, "bhgen_tree", "el_phi", xbin, xmin, xmax)
    h2 = make_h1(inp2, "ltree", "true_el_phi", xbin, xmin, xmax)

    plt.plot(h1[0], h1[1], "-", color="red", lw=1)
    plt.plot(h2[0], h2[1], "--", color="blue", lw=1)

    ax.set_xlabel(r"$\pi-\theta_e$ (mrad)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#el_phi

#_____________________________________________________________________________
def make_h1(infile, tnam, val, xbin, xmin, xmax, sel=""):

    inp = TFile.Open(infile)
    tree = inp.Get(tnam)

    #tree.Print()

    #hx = ut.prepare_TH1D(tnam+"_"+val+"_hx", xbin, xmin, xmax)
    #tree.Draw(val+" >> "+tnam+"_"+val+"_hx", sel)
    hx = ut.prepare_TH1D(tnam+"_hx", xbin, xmin, xmax)
    tree.Draw(val+" >> "+tnam+"_hx", sel)

    print(val, "entries:", hx.GetEntries())

    ut.norm_to_integral(hx, 1.)

    return ut.h1_to_arrays(hx)

#make_h1

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

    main()









