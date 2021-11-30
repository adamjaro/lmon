#!/usr/bin/python3

from ctypes import c_double, c_bool, c_int
import numpy as np

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath, TTree, TDatabasePDG, TF1
from ROOT import std

import sys
sys.path.append('../')
import plot_utils as ut

from ParticleCounterHits import ParticleCounterHits
from spec_acc import spec_acc

#_____________________________________________________________________________
def main():

    iplot = 0

    func = {}
    func[0] = acc_spec
    func[1] = up_rate
    func[2] = en_bun
    func[3] = hit_z

    func[iplot]()

#main

#_____________________________________________________________________________
def acc_spec():

    #infile = "hits_spect.root"
    infile = "/home/jaroslav/sim/lmon/data/luminosity/lm2ax1/hits_spect.root"
    #infile = "/home/jaroslav/sim/lmon/data/luminosity/lm1b/hits.root"
    #infile = "/home/jaroslav/sim/lmon/data/luminosity/lm1c/hits.root"

    emin = 0
    emax = 19

    amax = 0.06

    inp_lmon = TFile.Open(infile)
    tree_lmon = inp_lmon.Get("event")

    acc_lmon = rt.acc_Q2_kine(tree_lmon, "gen_en", "is_spect")
    acc_lmon.prec = 0.04
    #acc_lmon.prec = 0.08
    acc_lmon.delt = 1e-2
    #acc_lmon.bmin = 0.1
    #acc_lmon.nev = int(1e5)
    gLmon = acc_lmon.get()

    can = ut.box_canvas()
    frame = gPad.DrawFrame(emin, 0, emax, amax)

    ut.put_yx_tit(frame, "Spectrometer acceptance", "Photon energy #it{E} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gLmon, rt.kBlue)
    gLmon.Draw("psame")

    #integrate the acceptance to scale the parametrization
    en = c_double(0)
    av = c_double(0)
    iacc = 0.
    for i in range(gLmon.GetN()):
        gLmon.GetPoint(i, en, av)
        iacc += av.value*(gLmon.GetErrorXhigh(i)+gLmon.GetErrorXlow(i))

    print("iacc:", iacc)

    geo = rt.GeoParser("../../config/geom_all.in")
    length = geo.GetD("lumi_dipole", "zpos") - geo.GetD("vac_lumi_spec_mid", "z0")
    field = 0.37 # T
    #field = 0.2 # T
    #field = 0.1 # T

    acc = spec_acc(length, field, geo.GetD("vac_lumi_spec_mid", "dY0"), geo.GetD("vac_lumi_mag_spec", "dY1"))
    acc.scale = iacc/acc.acc_func.Integral(1, 21)
    acc.acc_func.Draw("same")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_spec

#_____________________________________________________________________________
def up_rate():

    #detector = "up"
    #detector = "down"
    detector = "phot"

    #plot range
    xybin = 5.
    xylen = 110.

    inp_lmon = TFile.Open("lmon.root")
    #number of interactions from event tree
    ni = inp_lmon.Get("event").GetEntries()
    #hits tree
    tree = inp_lmon.Get(detector)

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xylen, xylen, xybin, -xylen, xylen)
    tree.Draw("y:x >> hXY")

    #scale to hits per unit area per second
    scale = get_scale(ni)
    print("scale:", scale)
    lam = scale["lambda"]
    tb = scale["Tb"]

    #bin area in mm^2
    bin_area = xybin**2
    print("area:", bin_area)

    #scale_area = scale/bin_area # mm^-2 sec^-1
    #print("scale_area:", scale_area)

    nhits_all = 0.

    for ix in range(1, hXY.GetNbinsX()+1):
        for iy in range(1, hXY.GetNbinsY()+1):

            nh = hXY.GetBinContent(ix, iy)
            nhits_all += nh

            #hits in bunch crossing
            nhb = (nh/ni)*lam

            #rate per area, mm^-2 sec^-1
            rA = (1.-np.e**(-nhb))*(1./tb)*(1./bin_area)
            #print(rA)

            hXY.SetBinContent(ix, iy, rA)

    #hits per interaction
    print("Hits per interaction:", nhits_all/ni)

    #integrated rate
    rate_all = (1.-np.e**(-(nhits_all/ni)*lam))*(1./tb)
    print("Integrated rate (MHz):", 1e-6*rate_all)

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    ytit = "#it{y} (mm)"
    xtit = "#it{x} (mm)"
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    hXY.SetZTitle("Event rate (mm^{-2} s^{-1})")
    hXY.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.15)

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#up_rate

#_____________________________________________________________________________
def en_bun():

    #energy in bunch crossing

    infile = "/home/jaroslav/sim/lmon/data/luminosity/lm1a/hits.root"

    #detector = "bun_up_en"
    #detector = "bun_down_en"
    #detector = "bun_phot_en"
    detector = "bun_up_en+bun_down_en"

    cond = "(bun_up_en>1)&&(bun_down_en>1)"

    #plot range
    ebin = 0.5
    emax = 35.
    #emax = 150.

    inp_lmon = TFile.Open(infile)
    tree = inp_lmon.Get("bunch")

    can = ut.box_canvas()
    hE = ut.prepare_TH1D("hE", ebin, 0, emax)

    tree.Draw(detector+" >> hE", cond, "", 100000)

    ut.set_H1D_col(hE, rt.kBlue)

    ut.put_yx_tit(hE, "Counts", "Incident energy in bunch crossing (GeV)", 1.5, 1.4)

    ut.set_margin_lbtr(gPad, 0.11, 0.11, 0.02, 0.03)

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en_bun

#_____________________________________________________________________________
def hit_z():

    #hit z position

    #detector = "up"
    #detector = "down"
    detector = "phot"

    #plot range
    zbin = 1e-3
    zmin = -0.1
    zmax = 0.1

    inp_lmon = TFile.Open("lmon.root")
    tree = inp_lmon.Get(detector)

    can = ut.box_canvas()
    hZ = ut.prepare_TH1D("hZ", zbin, zmin, zmax)

    tree.Draw("z >> hZ")
    print("Entries:", hZ.GetEntries())

    ut.set_H1D_col(hZ, rt.kBlue)

    ut.put_yx_tit(hZ, "Counts", "Hit #it{z} (mm)", 1.5, 1.4)

    ut.set_margin_lbtr(gPad, 0.11, 0.11, 0.02, 0.03)

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hit_z

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gROOT.ProcessLine(".L ../acc_Q2_kine.h+")

    gSystem.AddIncludePath(" -I/home/jaroslav/sim/lmon/include")
    gSystem.AddIncludePath(" -I/home/jaroslav/sim/geant/geant4.10.07.p01/install/include/Geant4")
    gROOT.ProcessLine(".L ../../src/GeoParser.cxx+")

    main()



