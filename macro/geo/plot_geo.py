#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TCanvas

import sys
sys.path.append('../')
import plot_utils as ut

from segment import segment
from magnet import magnet
from vacuum import vacuum

#_____________________________________________________________________________
def main():

    zmin = -40000.
    zmax = -10100.
    xmin = -1300.
    xmax = 800.

    c1 = TCanvas("c1","c1",1000,700)
    frame = gPad.DrawFrame(zmin, xmin, zmax, xmax) # xmin, ymin, xmax, ymax in ROOT
    frame.SetTitle(";Length #it{z} (mm);Horizontal #it{x} (mm)")
    siz = 0.035
    frame.SetTitleSize(siz)
    frame.SetLabelSize(siz)
    frame.SetTitleSize(siz, "Y")
    frame.SetLabelSize(siz, "Y")

    frame.GetYaxis().SetTitleOffset(1.3)
    frame.GetXaxis().SetTitleOffset(1.2)
    frame.GetYaxis().CenterTitle()
    frame.GetXaxis().CenterTitle()
    gPad.SetLeftMargin(0.09)
    gPad.SetRightMargin(0.01)
    gPad.SetTopMargin(0.02)
    gPad.SetBottomMargin(0.09)

    #geometry
    geo = rt.GeoParser("../../config/geom_all.in")

    #spectrometer magnet
    mag = magnet("lumi_dipole", geo)
    mag.label = "Spectr. dipole"
    mag.draw()

    #B2BeR magnet
    b2b = magnet("B2BeR", geo)
    b2b.label = "B2BeR"
    b2b.draw()

    #Q3eR magnet
    q3 = magnet("Q3eR", geo)
    q3.label = "Q3eR"
    q3.draw()

    #beam vacuum
    bvac = vacuum(geo)
    bvac.add_point("vac_b2b_drift", "zQB", "xQB")
    bvac.add_point("vac_b2b_drift", "zQT", "xQT")
    bvac.add_point("vac_b2b_drift", "zW", "xW")
    bvac.add_point("vac_b2b_window", "win_z", "win_xmax")
    bvac.add_point_2("vac_b2b_window.b2b_end_z", "B2BeR.r2")
    bvac.add_point("vac_tag1_win", "zB", "xB")
    bvac.draw()

    #vacuum in front of Tagger 1
    vac_t1 = vacuum(geo)
    vac_t1.add_point("vac_tag1_win", "zTB", "xTB")
    vac_t1.add_point("vac_tag1_win", "zT", "xT")
    vac_t1.add_point("vac_tag1_win", "zB", "xB")
    vac_t1.draw()

    #vacuum in front of Tagger 2
    vac_t2 = vacuum(geo)
    vac_t2.add_point("vac_tag2_win", "zTB", "xTB")
    vac_t2.add_point("vac_tag2_win", "zT", "xT")
    vac_t2.add_point("vac_tag2_win", "zB", "xB")
    vac_t2.draw()

    #vacuum from exit window to spectrometer magnet
    vac_win = vacuum(geo)
    vac_win.add_point("vac_lumi_win_mag", "z1", "dX1", -1.)
    vac_win.add_point("vac_lumi_win_mag", "z1", "dX1")
    vac_win.add_point("vac_lumi_win_mag", "z0", "dX0")
    vac_win.add_point("vac_lumi_win_mag", "z0", "dX0", -1.)
    #vac_win.add_point("", "", "")
    #vac_win.draw()

    #vacuum from spectrometer magnet to spectrometer detectors
    vac_mag = vacuum(geo)
    vac_mag.add_point("vac_lumi_mag_spec", "z1", "dX1", -1.)
    vac_mag.add_point("vac_lumi_mag_spec", "z1", "dX1")
    vac_mag.add_point("vac_lumi_mag_spec", "z0", "dX0")
    vac_mag.add_point("vac_lumi_mag_spec", "z0", "dX0", -1.)
    #vac_mag.draw()

    #vacuum section from spectrometers to direct photon detector
    vac_phot = vacuum(geo)
    vac_phot.add_point("vac_lumi_spec_phot", "z1", "dX1", -1.)
    vac_phot.add_point("vac_lumi_spec_phot", "z1", "dX1")
    vac_phot.add_point("vac_lumi_spec_phot", "z0", "dX0")
    vac_phot.add_point("vac_lumi_spec_phot", "z0", "dX0", -1.)
    #vac_phot.draw()

    #Tagger1
    tag1 = segment("Tagger1box", geo)
    tag1.label = "Tagger 1"
    tag1.draw()

    #Tagger2
    tag2 = segment("Tagger2box", geo)
    tag2.label = "Tagger 2"
    tag2.draw()

    #Luminosity exit window
    ew = segment("ExitWinBox", geo)
    ew.label = "Exit window"
    ew.fill_col = rt.kGreen+1
    ew.draw()

    #up spectrometer for both spectrometers
    up = segment("LumiSUbox", geo)
    up.theta = 0
    up.label = "Spectrometers"
    up.draw()

    #Luminosity direct photon detector
    phot = segment("LumiDbox", geo)
    phot.label = "Photon detector"
    phot.draw()

    leg = ut.prepare_leg(0.8, 0.21, 0.25, 0.15, 0.03)#, 0.027) # x, y, dx, dy, tsiz
    leg.AddEntry(tag1.gbox, "Detector", "f")
    leg.AddEntry(b2b.gbox, "Magnet", "f")
    leg.AddEntry(bvac.gbox, "Vacuum", "f")
    leg.Draw("same")

    gPad.SetGrid()

    #ut.invert_col(gPad)
    c1.SaveAs("01fig.pdf")

#main

#_____________________________________________________________________________
if __name__ == "__main__":

    gSystem.AddIncludePath(" -I/home/jaroslav/sim/lmon/include")
    gSystem.AddIncludePath(" -I/home/jaroslav/sim/geant/geant4.10.07.p01/install/include/Geant4")
    gROOT.ProcessLine(".L ../../src/GeoParser.cxx+")

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetPadTickY(1)
    gStyle.SetFrameLineWidth(2)

    main()


























