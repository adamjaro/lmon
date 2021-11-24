#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath, TTree, TDatabasePDG, TF1
from ROOT import std

import sys
sys.path.append('../')
import plot_utils as ut

from spec_acc import spec_acc

#_____________________________________________________________________________
def main():

    #field = 0.37 # T, 18 GeV
    #field = 0.2 # T, 10 GeV
    field = 0.1 # T, 5 GeV

    emin = 0
    emax = 19

    amax = 1

    can = ut.box_canvas()
    frame = gPad.DrawFrame(emin, 0, emax, amax)

    ut.put_yx_tit(frame, "Spectrometer acceptance", "Photon energy #it{E} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.02)

    #geometry
    geo = rt.GeoParser("../../config/geom_all.in")

    #distance from magnet center to the front of spectrometer detectors
    length = geo.GetD("lumi_dipole", "zpos") - geo.GetD("vac_lumi_spec_mid", "z0")

    #print(geo.GetD("lumi_dipole", "zpos"))
    #print(geo.GetD("vac_lumi_spec_mid", "z0"))
    #print(geo.GetD("vac_lumi_spec_mid", "dY0"))
    #print(geo.GetD("vac_lumi_mag_spec", "dY1"))

    #acc = spec_acc(9700, 0.26, 42, 242)
    acc = spec_acc(length, field, geo.GetD("vac_lumi_spec_mid", "dY0"), geo.GetD("vac_lumi_mag_spec", "dY1"))
    acc.scale = 1
    acc.acc_func.Draw("same")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gSystem.AddIncludePath(" -I/home/jaroslav/sim/lmon/include")
    gSystem.AddIncludePath(" -I/home/jaroslav/sim/geant/geant4.10.07.p01/install/include/Geant4")
    gROOT.ProcessLine(".L ../../src/GeoParser.cxx+")

    main()







