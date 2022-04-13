#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TMath

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 3

    func = {}
    func[0] = en
    func[1] = pitheta
    func[2] = phi
    func[3] = eff_en_pitheta
    func[4] = en_spectrum

    func[iplot]()

#_____________________________________________________________________________
def en():

    #GeV
    ebin = 0.3
    emin = 3
    emax = 19

    #inp = "../../analysis/ini/spect_rec.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect_rec_pass4.root"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get("spec_rec")

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", ebin, emin, emax, ebin, emin, emax)

    tree.Draw("rec_E:true_phot_E >> hxy", sel)
    print("Entries:", hxy.GetEntries())

    ytit = "Reconstructed energy #it{E_{#gamma}} (GeV)"
    xtit = "Generated true energy #it{E_{#gamma,gen}} (GeV)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.9, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.03, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en

#_____________________________________________________________________________
def pitheta():

    #mrad
    tbin = 0.03
    tmin = 0
    tmax = 1.5

    #inp = "../../analysis/ini/spect_rec.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect_rec_pass4.root"

    sel = ""

    infile = TFile.Open(inp)
    tree = infile.Get("spec_rec")

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", tbin, tmin, tmax, tbin, tmin, tmax)

    tree.Draw("(TMath::Pi()-rec_theta)*1e3:(TMath::Pi()-true_phot_theta)*1e3 >> hxy", sel)

    ytit = "Reconstructed #it{#pi-#theta_{#gamma}} (mrad)"
    xtit = "Generated true #it{#pi-#theta_{#gamma,gen}} (mrad)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.9, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.03, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#pitheta

#_____________________________________________________________________________
def phi():

    #GeV
    pbin = 0.3
    pmin = -TMath.Pi()-0.1
    pmax = TMath.Pi()+0.1

    #inp = "../../analysis/ini/spect_rec.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect_rec_pass4.root"

    sel = ""
    sel = "(TMath::Pi()-rec_theta)>0.4e-3"

    infile = TFile.Open(inp)
    tree = infile.Get("spec_rec")

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", pbin, pmin, pmax, pbin, pmin, pmax)

    tree.Draw("rec_phi:true_phot_phi >> hxy", sel)

    ytit = "Reconstructed #it{#phi_{#gamma}} (rad)"
    xtit = "Generated true #it{#phi_{#gamma,gen}} (rad)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.9, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.03, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.85, 0.24, 0.1, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#pi-#theta_{#it{#gamma},rec} > 0.4 mrad", "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#phi

#_____________________________________________________________________________
def eff_en_pitheta():

    #reconstruction efficiency in energy (GeV) and pi - theta (mrad)

    #inp = "../../analysis/ini/spect_rec.root"
    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect_rec_pass4.root"

    #bins in theta, mrad
    xbin = 0.03
    xmin = 0
    xmax = 1.2

    #bins in energy, GeV
    ybin = 0.3
    ymin = 3
    ymax = 19

    infile = TFile.Open(inp)
    tree_in = infile.Get("event")

    tmp = TFile("tmp.root", "recreate")
    tree = tree_in.CopyTree("is_spect==1")

    can = ut.box_canvas()

    hSpe = ut.prepare_TH2D("hSpe", xbin, xmin, xmax, ybin, ymin, ymax)
    hAll = ut.prepare_TH2D("hAll", xbin, xmin, xmax, ybin, ymin, ymax)

    form = "true_phot_E:(TMath::Pi()-true_phot_theta)*1e3" # mrad
    tree.Draw(form+" >> hSpe", "is_rec==1")
    tree.Draw(form+" >> hAll")

    hSpe.Divide(hAll)

    ytit = "Generated true energy #it{E_{#gamma,gen}} (GeV)"
    xtit = "Generated true #it{#pi}-#it{#theta_{#gamma,gen}} (mrad)"
    ut.put_yx_tit(hSpe, ytit, xtit, 1.4, 1.3)

    hSpe.SetTitleOffset(1.4, "Z")
    hSpe.SetZTitle("Reconstruction efficiency")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hSpe.SetMinimum(0.)
    hSpe.SetMaximum(1.)
    hSpe.SetContour(300)

    hSpe.Draw("colz")

    #leg = ut.prepare_leg(0.15, 0.9, 0.24, 0.06, 0.035) # x, y, dx, dy, tsiz
    #leg.AddEntry("", "#bf{"+lab_sel+"}", "")
    #leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#eff_en_pitheta

#_____________________________________________________________________________
def en_spectrum():

    #spectrum in energy, reconstructed and true generated energy

    #GeV
    xbin = 0.5
    xmin = 3
    xmax = 19

    inp = "/home/jaroslav/sim/lmon/data/luminosity/lm4ax3/spect_rec_pass4.root"

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    hx = make_h1(inp, "spec_rec", "true_phot_E", xbin, xmin, xmax)
    plt.plot(hx[0], hx[1], "-", color="red", lw=1)

    hx2 = make_h1(inp, "spec_rec", "rec_E", xbin, xmin, xmax)
    plt.plot(hx2[0], hx2[1], "-", color="blue", lw=1)

    ax.set_xlabel("$E$ (GeV)")
    ax.set_ylabel("Normalized counts")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#en_spectrum

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






















