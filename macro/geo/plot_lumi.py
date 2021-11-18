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
    ymin = -390
    ymax = 400.

    c1 = TCanvas("c1","c1",1000,700)
    frame = gPad.DrawFrame(zmin, ymin, zmax, ymax) # xmin, ymin, xmax, ymax in ROOT
    frame.SetTitle(";Length #it{z} (mm);Vertical #it{y} (mm)")
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

    #B2BeR magnet
    b2b = magnet("B2BeR", geo)
    b2b.label = "B2BeR"
    b2b.draw()

    #beam vacuum from B2BeR to exit window
    bvac = vacuum(geo)
    bvac.add_point("vac_b2b_window", "b2b_end_z", "b2b_end_xy", -0.5)
    bvac.add_point("vac_b2b_window", "win_z", "win_xmax", -1)
    bvac.add_point("vac_b2b_window", "win_z", "win_xmax")
    bvac.add_point("vac_b2b_window", "b2b_end_z", "b2b_end_xy", 0.5)
    bvac.draw()

    #vacuum from exit window to spectometer magnet
    vac_win_spec = vacuum(geo)
    vac_win_spec.add_point("vac_lumi_win_mag", "z0", "dY0", -1)
    vac_win_spec.add_point("vac_lumi_win_mag", "z1", "dY1", -1)
    vac_win_spec.add_point("vac_lumi_win_mag", "z1", "dY1")
    vac_win_spec.add_point("vac_lumi_win_mag", "z0", "dY0")
    vac_win_spec.draw()

    #vacuum from specrometer magnet to detectors
    vac_det = vacuum(geo)
    vac_det.add_point("vac_lumi_mag_spec", "z0", "dY0", -1)
    vac_det.add_point("vac_lumi_mag_spec", "z1", "dY1", -1)
    vac_det.add_point("vac_lumi_spec_mid", "z0", "dY0", -1)
    vac_det.add_point("vac_lumi_spec_phot", "z0", "dY0", -1)
    vac_det.add_point("vac_lumi_spec_phot", "z1", "dY1", -1)
    vac_det.add_point("vac_lumi_spec_phot", "z1", "dY1")
    vac_det.add_point("vac_lumi_spec_phot", "z0", "dY0")
    vac_det.add_point("vac_lumi_spec_mid", "z0", "dY0")
    vac_det.add_point("vac_lumi_mag_spec", "z1", "dY1")
    vac_det.add_point("vac_lumi_mag_spec", "z0", "dY0")
    vac_det.draw()

    #spectrometer magnet
    mag = magnet("lumi_dipole", geo)
    mag.label = "Spectr. dipole"
    mag.draw()

    #luminosity exit window
    ew = segment("ExitWinBox", geo)
    ew.y_project = True
    ew.label = "Exit window"
    ew.fill_col = rt.kGreen+1
    ew.draw()

    #up spectrometer
    up = segment("LumiSUbox", geo)
    up.y_project = True
    up.theta = -1.*up.theta
    up.label = "Up"
    up.draw()

    #down spectrometer
    down = segment("LumiSDbox", geo)
    down.y_project = True
    down.theta = -1.*down.theta
    down.label = "Down"
    down.draw()

    #photon detector
    phot = segment("LumiDbox", geo)
    phot.y_project = True
    phot.label = "Photon detector"
    phot.draw()

    leg = ut.prepare_leg(0.8, 0.21, 0.25, 0.15, 0.03)#, 0.027) # x, y, dx, dy, tsiz
    leg.AddEntry(phot.gbox, "Detector", "f")
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

