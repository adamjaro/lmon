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

    iplot = 2

    func = {}
    func[0] = radial
    func[1] = rz
    func[2] = beampipe
    func[3] = hit_en

    func[iplot]()

#main

#_____________________________________________________________________________
def radial():

    #Hz
    #total_rate = 685833. # full range
    total_rate = 2442171. # full range

    #all simulated events
    nall = 10e6

    #zlabel = "0"
    #zlabel = "5 m"
    #zlabel = "3.6 m"
    #zlabel = "-2 m"
    zlabel = "-3.55 m"

    #input
    #infile = "/home/jaroslav/sim/lmon/data/beam-gas/rc_2e.root"
    infile = "/home/jaroslav/sim/Athena/data/beam-gas/bg2c/rc_vtx.root"

    #photon and electron rate
    #xp, yp, ptot = get_rate(infile, "ptree", total_rate, nall)
    #exp, eyp, etot = get_rate(infile, "etree", total_rate, nall)
    dxp, dyp, dtot = get_rate(infile, "htree", total_rate, nall)

    #print("Sum rate (kHz):", (ptot+etot)/1e3)
    print("Sum rate (kHz):", (dtot)/1e3)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    #plt.plot(xp, yp, "-", color="blue", lw=1)
    #plt.plot(exp, eyp, "-", color="red", lw=1)
    plt.plot(dxp, dyp, "-", color="blue", lw=1)

    #ax.set_xlabel("$r_{xy}$ (cm) at $z$ = "+zlabel)
    ax.set_xlabel("Radius $r$ (cm)")
    ax.set_ylabel("Event rate per unit area (Hz/cm$^2$)")

    leg = legend()
    leg.add_entry(leg_txt(), "Plane at $z$ = "+zlabel)
    leg.add_entry(leg_lin("red"), "Electron rate")
    leg.add_entry(leg_lin("blue"), "Photon rate")
    leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#radial

#_____________________________________________________________________________
def get_rate(infile, tnam, total_rate, nall):

    #cm
    rmin = 3.2
    rmax = 70
    rbin = 1
    #rbin = 0.8

    infile = TFile.Open(infile)
    tree = infile.Get(tnam)

    print("Tree entries:", tree.GetEntries())

    hr = ut.prepare_TH1D("hr", rbin, rmin, rmax)

    tree.Draw("rpos/1e1 >> hr", "rpos>"+str(rmin*10))

    print("Plot entries:", hr.GetEntries())

    #rate per simulated event
    rsim = total_rate/nall
    print("rsim:", rsim)

    xp = []
    yp = []
    all_rate = 0.
    for ibin in range(1,hr.GetNbinsX()+1):

        #radii and surface
        r1 = hr.GetBinLowEdge(ibin)
        r2 = r1 + hr.GetBinWidth(ibin)
        surf = ma.pi*r2**2 - ma.pi*r1**2

        xp.append( r1 )
        xp.append( r2 )

        #rate in a given bin
        rate = rsim*hr.GetBinContent(ibin)
        #print(rate)

        yp.append( rate/surf )
        yp.append( rate/surf )

        all_rate += rate

    print("Integrated rate:", all_rate)

    return xp, yp, all_rate

#get_rate

#_____________________________________________________________________________
def rz():

    #rate in radius and vertex z-position

    #Hz
    total_rate = 685833. # full range

    #all simulated events
    nall = 100e6 # full range

    #meters
    #zmin = -1
    #zmin = 3
    #zmin = 2
    #zmin = -4
    zmin = -6
    zmax = 16
    zbin = 0.7

    #cm
    rmin = 0
    rmax = 85
    rbin = 3

    #zlabel = "0"
    #zlabel = "5 m"
    #zlabel = "3.6 m"
    #zlabel = "-2 m"
    zlabel = "-3.55 m"
    pelabel = "Photons + electrons"

    #infile = "/home/jaroslav/sim/lmon/data/beam-gas/rc_2a.root"
    #infile = "/home/jaroslav/sim/lmon/data/beam-gas/rc_2b.root"
    #infile = "/home/jaroslav/sim/lmon/data/beam-gas/rc_2c.root"
    #infile = "/home/jaroslav/sim/lmon/data/beam-gas/rc_2d.root"
    infile = "/home/jaroslav/sim/lmon/data/beam-gas/rc_2e.root"

    infile = TFile.Open(infile)
    ptree = infile.Get("ptree")
    etree = infile.Get("etree")

    can = ut.box_canvas()

    hz = ut.prepare_TH2D("hz", zbin, zmin, zmax, rbin, rmin, rmax)

    ptree.Draw("(rpos/1e1):(vtx_z/1e3) >> hz", "rpos>32")
    etree.Draw("(rpos/1e1):(vtx_z/1e3) >>+hz", "rpos>32")

    print("Entries:", hz.GetEntries())

    hz.SetXTitle("Vertex #it{z} (m)")
    hz.SetYTitle("#it{r_{xy}} (cm) at #it{z} = "+zlabel)
    hz.SetZTitle("Event rate per unit area (Hz/cm^{2})")

    hz.SetTitleOffset(1.3, "Y")
    hz.SetTitleOffset(1.3, "X")
    hz.SetTitleOffset(1.5, "Z")

    hz.GetXaxis().CenterTitle()
    hz.GetYaxis().CenterTitle()

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.02, 0.16)

    #rate per simulated event
    rsim = total_rate/nall

    minr = 1e9
    maxr = -1e9
    totr = 0
    for ix in range(1, hz.GetNbinsX()+1):
        for iy in range(1, hz.GetNbinsY()+1):

            #radii and surface
            r1 = hz.GetYaxis().GetBinLowEdge(ix)
            r2 = r1 + hz.GetYaxis().GetBinWidth(ix)
            surf = ma.pi*r2**2 - ma.pi*r1**2

            rate = rsim*hz.GetBinContent(ix, iy)
            totr += rate

            if hz.GetBinContent(ix, iy) > 0:
                if rate/surf > maxr: maxr = rate/surf
                if rate/surf < minr: minr = rate/surf

            hz.SetBinContent(ix, iy, rate/surf)

    print(minr, maxr)

    print("Integrated rate (kHz): ", totr/1e3)

    hz.SetMinimum(minr-0.1*minr)
    hz.SetMaximum(maxr+0.1*maxr)
    hz.SetContour(300)

    leg = ut.prepare_leg(0.2, 0.86, 0.18, 0.1, 0.035)
    leg.AddEntry("", "Plane at #it{z} = "+zlabel, "")
    leg.AddEntry("", pelabel, "")
    leg.Draw("same")

    gPad.SetLogz()

    gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rz

#_____________________________________________________________________________
def beampipe():

    #Hz
    total_rate = 2441830.6 # full range, Eg > 100 keV
    total_rate2 = 3177253.7 # Eg > 10 keV

    #all simulated events
    nall = 10e6 # full range

    #input
    infile = "/home/jaroslav/sim/lmon/data/beam-gas/bg3d/rc.root"
    infile2 = "/home/jaroslav/sim/lmon/data/beam-gas/bg3e/rc.root"

    #lmon rate
    xp, yp, ltot = get_rate_beampipe(infile, "htree", total_rate, nall)
    xp2, yp2, ltot2 = get_rate_beampipe(infile2, "htree", total_rate2, nall)

    #dd4hep rate
    #infile_dd = "/home/jaroslav/sim/Athena/data/beam-gas/bg2c/rc_vtx.root"
    #nall_dd = 1e7
    #dxp, dyp, dtot = get_rate_beampipe(infile_dd, "htree", total_rate, nall_dd)

    print("Lmon rate (kHz):", ltot/1e3)
    print("Lmon rate2 (kHz):", ltot2/1e3)
    #print("DD4hep rate (kHz):", dtot/1e3)

    #plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(xp, yp, "-", color="blue", lw=1)
    plt.plot(xp2, yp2, "-", color="red", lw=1)
    #plt.plot(dxp, dyp, "-", color="red", lw=1)

    ax.set_xlabel("$z$ (mm)")
    ax.set_ylabel("Event rate per unit area (Hz/cm$^2$)")

    leg = legend()
    leg.add_entry(leg_lin("red"), "$E_\gamma$ > 10 keV")
    leg.add_entry(leg_lin("blue"), "$E_\gamma$ > 100 keV")
    #leg.add_entry(leg_lin("red"), "DD4hep observed rate")
    #leg.add_entry(leg_lin("blue"), "Geant4 incident rate")
    leg.draw(plt, col)

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#beampipe

#_____________________________________________________________________________
def get_rate_beampipe(infile, tnam, total_rate, nall):

    #cylindrical rate along z

    #mm
    zmin = -200.
    zmax = 200.
    zbin = 20.

    #cylindrical radius, mm
    rbeam = 33.

    infile = TFile.Open(infile)
    tree = infile.Get(tnam)

    print("Tree entries:", tree.GetEntries())

    hz = ut.prepare_TH1D("hz", zbin, zmin, zmax)

    tree.Draw("zpos >> hz", "(zpos<150.)") # &&(rpos<35)

    print("Plot entries:", hz.GetEntries())

    #rate per simulated event
    rsim = total_rate/nall
    print("rsim:", rsim)

    xp = []
    yp = []
    all_rate = 0.
    for ibin in range(1,hz.GetNbinsX()+1):

        #z of the interval, meters
        z1 = hz.GetBinLowEdge(ibin)
        z2 = z1 + hz.GetBinWidth(ibin)

        #surface element, cm^2
        dz = (z2-z1)*0.1 # cm
        surf = dz*2*ma.pi*rbeam*0.1 # cm^2

        xp.append( z1 )
        xp.append( z2 )

        #rate in a given bin
        rate = rsim*hz.GetBinContent(ibin)

        yp.append( rate/surf )
        yp.append( rate/surf )

        all_rate += rate

    print("Integrated rate:", all_rate)

    return xp, yp, all_rate

#get_rate_beampipe

#_____________________________________________________________________________
def hit_en():

    #hit energy

    infile = "/home/jaroslav/sim/lmon/data/beam-gas/bg3d/rc.root"

    emin = -9
    emax = 9
    ebin = 0.1

    inp = TFile.Open(infile)
    htree = inp.Get("htree")

    #can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)
    htree.Draw("TMath::Log10(en*1e6) >> hE", "zpos<150.")
    xp, yp = ut.h1_to_arrays(hE)

    infile2 = "/home/jaroslav/sim/lmon/data/beam-gas/bg3e/rc.root"
    inp2 = TFile.Open(infile2)
    htree2 = inp2.Get("htree")
    hE2 = ut.prepare_TH1D("hE2", ebin, emin, emax)
    htree2.Draw("TMath::Log10(en*1e6) >> hE2", "zpos<150.")
    xp2, yp2 = ut.h1_to_arrays(hE2)

    #plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(xp, yp, "-", color="blue", lw=1)
    plt.plot(xp2, yp2, "-", color="red", lw=1)

    ax.set_xlabel("Incident hit energy (keV)")
    ax.set_ylabel("Counts")

    leg = legend()
    leg.add_entry(leg_lin("red"), "$E_\gamma$ > 10 keV")
    leg.add_entry(leg_lin("blue"), "$E_\gamma$ > 100 keV")
    leg.draw(plt, col)

    ax.set_yscale("log")

    plt.xticks(ax.get_xticks()[1:-1], ["$10^{"+"{0:.0f}".format(i)+"}$" for i in ax.get_xticks()[1:-1]])

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#hit_en

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




















