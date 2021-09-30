#!/usr/bin/python3

import sys
import configparser

from pandas import DataFrame, HDFStore, read_hdf
from pyHepMC3 import HepMC3 as hepmc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 2

    func = {}
    func[0] = pressure_func
    func[1] = sigma_xy
    func[2] = vtx_xz
    func[3] = vtx_yz
    func[4] = div_xy
    func[5] = phot_theta
    func[6] = vtx_xz_df
    func[7] = phot_en_df
    func[8] = phot_theta_df
    func[9] = el_en_df
    func[10] = el_theta_df
    func[11] = phot_proj_z0
    func[12] = phot_proj_z_ecal
    func[13] = el_proj_z0
    func[14] = el_proj_z_ecal

    func[101] = create_df

    func[iplot]()

#main

#_____________________________________________________________________________
def pressure_func():

    gen = make_gen()

    #pressure function
    pf = gen.pressure_func

    ut.set_F1(pf, rt.kBlue)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(-5.5e3, 0, 15.5e3, 7e-9)

    pf.Draw("same")

    gPad.SetGrid()

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#pressure_func

#_____________________________________________________________________________
def sigma_xy():

    #beam sigma in x and y

    gen = make_gen()
    beam = gen.beam_par

    gx = TGraph(beam.hz.GetNbinsX()+1)
    gy = TGraph(beam.hz.GetNbinsX()+1)

    for ibin in range(beam.hz.GetNbinsX()+1):
        zpos = beam.hz.GetBinCenter(ibin)
        sx = beam.gx[ibin].GetParameter(2)
        sy = beam.gy[ibin].GetParameter(2)

        gx.SetPoint(ibin, zpos, sx)
        gy.SetPoint(ibin, zpos, sy)

    ut.set_graph(gx, rt.kBlue)
    ut.set_graph(gy, rt.kRed)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(-10e3, 0, 15.5e3, 3.3)

    gx.Draw("lsame")
    gy.Draw("lsame")

    gPad.SetGrid()

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#sigma_xy

#_____________________________________________________________________________
def vtx_xz():

    #vertex position in xz plane
    zmin = -5.5
    zmax = 15.5
    zbin = 1e-1

    xmax = 15
    xbin = 0.1

    #gdir = "/home/jaroslav/sim/GETaLM_data/beam_gas/"
    #inp = "beam_gas_ep_10GeV_emin0p1_10Mevt.root"
    gdir = "/home/jaroslav/sim/GETaLM/cards/"
    inp = "bg.root"

    infile = TFile.Open(gdir+inp)
    tree = infile.Get("ltree")

    can = ut.box_canvas()

    hxz = ut.prepare_TH2D("hxz", zbin, zmin, zmax, xbin, -xmax, xmax)

    tree.Draw("vtx_x:(vtx_z/1e3) >> hxz")

    hxz.SetXTitle("#it{z} (m)")
    hxz.SetYTitle("#it{x} (mm)")

    hxz.SetTitleOffset(1.3, "Y")
    hxz.SetTitleOffset(1.3, "X")

    hxz.GetXaxis().CenterTitle()
    hxz.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hxz.SetMinimum(0.98)
    hxz.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#vtx_xz

#_____________________________________________________________________________
def vtx_yz():

    #vertex position in yz plane
    zmin = -5.5
    zmax = 15.5
    zbin = 1e-1

    ymax = 15
    ybin = 0.1

    #gdir = "/home/jaroslav/sim/GETaLM_data/beam_gas/"
    #inp = "beam_gas_ep_10GeV_emin0p1_10Mevt.root"
    gdir = "/home/jaroslav/sim/GETaLM/cards/"
    inp = "bg.root"

    infile = TFile.Open(gdir+inp)
    tree = infile.Get("ltree")

    can = ut.box_canvas()

    hyz = ut.prepare_TH2D("hyz", zbin, zmin, zmax, ybin, -ymax, ymax)

    tree.Draw("vtx_y:(vtx_z/1e3) >> hyz")

    hyz.SetXTitle("#it{z} (m)")
    hyz.SetYTitle("#it{y} (mm)")

    hyz.SetTitleOffset(1.3, "Y")
    hyz.SetTitleOffset(1.3, "X")

    hyz.GetXaxis().CenterTitle()
    hyz.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.09, 0.1, 0.02, 0.11)

    hyz.SetMinimum(0.98)
    hyz.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#vtx_yz

#_____________________________________________________________________________
def div_xy():

    #beam divergence in x and y

    gen = make_gen()
    beam = gen.beam_par

    gx = TGraph(beam.hz.GetNbinsX()+1)
    gy = TGraph(beam.hz.GetNbinsX()+1)

    for ibin in range(beam.hz.GetNbinsX()+1):
        zpos = beam.hz.GetBinCenter(ibin)
        dx = beam.divx[ibin].GetParameter(2)
        dy = beam.divy[ibin].GetParameter(2)

        gx.SetPoint(ibin, zpos, dx)
        gy.SetPoint(ibin, zpos, dy)

    ut.set_graph(gx, rt.kBlue)
    ut.set_graph(gy, rt.kRed)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(-10e3, 0, 15.5e3, 600e-6)

    gx.Draw("lsame")
    gy.Draw("lsame")

    gPad.SetGrid()

    ut.invert_col(gPad)
    can.SaveAs("01fig.pdf")

#div_xy

#_____________________________________________________________________________
def phot_theta():

    #polar angle of generated photons

    tbin = 0.01
    tmax = 4

    gdir = "/home/jaroslav/sim/GETaLM/cards/"
    inp = "bg.root"

    infile = TFile.Open(gdir+inp)
    tree = infile.Get("ltree")

    can = ut.box_canvas()

    ht1 = ut.prepare_TH1D("ht1", tbin, 0, tmax)
    ht2 = ut.prepare_TH1D("ht2", tbin, 0, tmax)
    ht2.SetMarkerColor(rt.kRed)
    ht2.SetLineColor(rt.kRed)

    #tree.Draw("(TMath::Pi()-true_phot_theta)*1000 >> ht")
    tree.Draw("(TMath::Pi()-phot_theta)*1000 >> ht1", "vtx_z>5000 && vtx_z<12000")
    tree.Draw("(TMath::Pi()-phot_theta)*1000 >> ht2", "vtx_z>-5000 && vtx_z<5000")

    #ht.SetYTitle("Events / ({0:.3f}".format(tbin)+" mrad)")
    #ht.SetYTitle("Counts")
    #ht.SetXTitle("Photon #it{#theta} (mrad)")

    #ht.SetTitleOffset(1.5, "Y")
    #ht.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.025)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.11)

    gPad.SetGrid()

    ht1.Draw()
    ht2.Draw("e1same")

    #leg = ut.prepare_leg(0.2, 0.87, 0.18, 0.08, 0.035)
    #leg.AddEntry(None, "Angular distribution of Bethe-Heitler photons", "")
    #leg.Draw("same")

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#phot_theta

#_____________________________________________________________________________
def vtx_xz_df():

    inp = read_hdf("bg.h5")

    nbins = 100

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.hist2d(inp["vtx_z"], inp["vtx_x"], bins=nbins)#, color="blue", density=True, histtype="step", lw=2)
    cbar = plt.colorbar()

    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#vtx_xz_df

#_____________________________________________________________________________
def phot_en_df():

    inp = read_hdf("bg.h5")

    nbins = 120

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.hist(inp["phot_en"], bins=nbins, color="blue", density=True, histtype="step", lw=2)

    ax.set_xlabel("Photon energy $E_\gamma$ (GeV)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#phot_en_df

#_____________________________________________________________________________
def phot_theta_df():

    inp = read_hdf("bg.h5")

    inp1 = inp.query("vtx_z>5000 and vtx_z<12000")# and phot_theta<0.004")
    inp2 = inp.query("vtx_z>-5000 and vtx_z<5000")# and phot_theta<0.004")

    nbins = 120

    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.hist((np.pi-inp1["phot_theta"])*1e3, bins=nbins, color="red", density=True, histtype="step", lw=1, range=(0,4))
    plt.hist((np.pi-inp2["phot_theta"])*1e3, bins=nbins, color="blue", density=True, histtype="step", lw=1, range=(0,4))

    ax.set_xlabel(r"Photon polar angle $\theta_\gamma$ (mrad)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_txt(), "$E_e$ = 10 GeV")
    leg.add_entry(leg_lin("blue"), "|$z$| < 5 m")
    leg.add_entry(leg_lin("red"), "5 < $z$ < 12 m")
    leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#phot_theta_df

#_____________________________________________________________________________
def el_en_df():

    inp = read_hdf("bg.h5")

    nbins = 120

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.hist(inp["el_en"], bins=nbins, color="blue", density=True, histtype="step", lw=1)

    ax.set_xlabel("Electron energy $E'_e$ (GeV)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#el_en_df

#_____________________________________________________________________________
def el_theta_df():

    inp = read_hdf("bg.h5")

    #inp1 = inp.query("vtx_z>5000 and vtx_z<12000")# and phot_theta<0.004")
    #inp2 = inp.query("vtx_z>-5000 and vtx_z<5000")# and phot_theta<0.004")

    nbins = 120

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    #plt.hist((np.pi-inp1["phot_theta"])*1e3, bins=nbins, color="red", density=True, histtype="step", lw=1, range=(0,4))
    #plt.hist((np.pi-inp2["phot_theta"])*1e3, bins=nbins, color="blue", density=True, histtype="step", lw=1, range=(0,4))
    plt.hist((np.pi-inp["el_theta"])*1e3, bins=nbins, color="blue", density=True, histtype="step", lw=1, range=(0,100))

    ax.set_xlabel(r"Electron polar angle $\theta_e$ (mrad)")
    ax.set_ylabel("Normalized counts")

    #leg = legend()
    #leg.add_entry(leg_txt(), "$E_e$ = 10 GeV")
    #leg.add_entry(leg_lin("blue"), "|$z$| < 5 m")
    #leg.add_entry(leg_lin("red"), "5 < $z$ < 12 m")
    #leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#el_theta_df

#_____________________________________________________________________________
def phot_proj_z0():

    inp = read_hdf("bg.h5")

    inp = inp.query("vtx_z>0")

    nbins = 120

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    #theta in rad:      (np.pi-inp["el_theta"])
    #  tan(theta) = rxy/z
    #radial position:   rxy = z * tan(theta)

    #plot in cm
    plt.hist( ( inp["vtx_z"]*np.tan( (np.pi-inp["phot_theta"]) ) + np.sqrt(inp["vtx_x"]**2 + inp["vtx_y"]**2) )/10, bins=nbins,\
        color="blue", density=True, histtype="step", lw=1) # , range=(0,150)

    ax.set_xlabel("$r_{xy}$ at $z$ = 0 (cm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_txt(), "Photon projection on $xy$ plane, $z$ = 0")
    leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#phot_proj_z0

#_____________________________________________________________________________
def phot_proj_z_ecal():

    #photon projection at z = 3700 mm, location for the end of forward ecal

    inp = read_hdf("bg.h5")

    inp = inp.query("vtx_z>3700")

    nbins = 120

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    #theta in rad:      (np.pi-inp["el_theta"])
    #  tan(theta) = rxy/z
    #radial position:   rxy = z * tan(theta)

    #plot in cm
    plt.hist( ( (inp["vtx_z"]-3700)*np.tan( (np.pi-inp["phot_theta"]) ) + np.sqrt(inp["vtx_x"]**2 + inp["vtx_y"]**2) )/10, bins=nbins,\
        color="blue", density=True, histtype="step", lw=1) # , range=(0,150)

    ax.set_xlabel("$r_{xy}$ at $z$ = 3.7 m (cm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_txt(), "Photon projection on $xy$ plane, $z$ = 3.7 m")
    leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#phot_proj_z_ecal

#_____________________________________________________________________________
def el_proj_z0():

    inp = read_hdf("bg.h5")

    inp = inp.query("vtx_z>0")

    nbins = 120

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    #theta in rad:      (np.pi-inp["el_theta"])
    #  tan(theta) = rxy/z
    #radial position:   rxy = z * tan(theta)

    #plot in cm
    plt.hist( ( inp["vtx_z"]*np.tan( (np.pi-inp["el_theta"]) ) + np.sqrt(inp["vtx_x"]**2 + inp["vtx_y"]**2) )/10, bins=nbins,\
        color="blue", density=True, histtype="step", lw=1, range=(0,150))

    ax.set_xlabel("$r_{xy}$ at $z$ = 0 (cm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_txt(), "Electron projection on $xy$ plane, $z$ = 0")
    leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#el_proj_z0

#_____________________________________________________________________________
def el_proj_z_ecal():

    #photon projection at z = 3700 mm, location for the end of forward ecal

    inp = read_hdf("bg.h5")

    inp = inp.query("vtx_z>3700")

    nbins = 120

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    #theta in rad:      (np.pi-inp["el_theta"])
    #  tan(theta) = rxy/z
    #radial position:   rxy = z * tan(theta)

    #plot in cm
    plt.hist( ( (inp["vtx_z"]-3700)*np.tan( (np.pi-inp["el_theta"]) ) + np.sqrt(inp["vtx_x"]**2 + inp["vtx_y"]**2) )/10, bins=nbins,\
        color="blue", density=True, histtype="step", lw=1, range=(0,150))

    ax.set_xlabel("$r_{xy}$ at $z$ = 3.7 m (cm)")
    ax.set_ylabel("Normalized counts")

    leg = legend()
    leg.add_entry(leg_txt(), "Electron projection on $xy$ plane, $z$ = 3.7 m")
    leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#el_proj_z_ecal

#_____________________________________________________________________________
def make_gen():

    sys.path.append('/home/jaroslav/sim/GETaLM/models')
    sys.path.append('/home/jaroslav/sim/GETaLM/base')

    from gen_beam_gas import gen_beam_gas

    parse = configparser.RawConfigParser(inline_comment_prefixes=(";","#"))
    parse.add_section("main")
    parse.set("main", "Ee", "10")
    parse.set("main", "emin", "0.1")

    return gen_beam_gas(parse)

#make_gen

#_____________________________________________________________________________
def create_df():

    #input hepmc
    #inp = "/home/jaroslav/sim/GETaLM_data/beam_gas/beam_gas_ep_10GeV_emin0p1_10Mevt.hepmc"
    inp = "/home/jaroslav/sim/GETaLM/cards/bg.hepmc"
    read = hepmc.ReaderAscii(inp)

    #output dataframe
    col = ["vtx_x", "vtx_y", "vtx_z", "phot_en", "phot_theta", "phot_phi", "el_en", "el_theta", "el_phi"]
    val = []

    nmax = 3000000
    iev = 0

    #event loop
    while(True):

        iev += 1
        if iev > nmax: break

        mc = hepmc.GenEvent(hepmc.Units.GEV, hepmc.Units.MM)
        read.read_event(mc)
        if( read.failed() ): break

        lin = []

        pos = mc.event_pos()
        lin.append( pos.x() )
        lin.append( pos.y() )
        lin.append( pos.z() )

        #photon and electron particles
        phot = None
        el = None
        for i in mc.particles():
            if i.pid() == 22:
                phot = i
            if i.pid() == 11:
                el = i

        lin.append( phot.momentum().e() )
        lin.append( phot.momentum().theta() )
        lin.append( phot.momentum().phi() )

        lin.append( el.momentum().e() )
        lin.append( el.momentum().theta() )
        lin.append( el.momentum().phi() )

        val.append( lin )

    df = DataFrame(val, columns=col)

    print(df)

    out = HDFStore("bg.h5")
    out["bg"] = df
    out.close()

    read.close()

#create_df

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
class legend:
    def __init__(self):
        self.items = []
        self.data = []
    def add_entry(self, i, d):
        self.items.append(i)
        self.data.append(d)
    def draw(self, px, col=None, **kw):
        leg = px.legend(self.items, self.data, **kw)
        if col != None:
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

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()



























