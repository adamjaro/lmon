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
    ymin = -800
    ymax = 800.

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

    l2 = ut.prepare_leg(0.64, 0.75, 0.25, 0.12, 0.027)
    l2.AddEntry("", "Space for exit window:", "")
    l2.AddEntry("", "Center #it{z}: "+str(ew.zpos), "")
    l2.AddEntry("", "Size in #it{xy}: "+str(ew.dy), "")
    l2.AddEntry("", "Lenght in #it{z}: "+str(ew.dz), "")
    l2.Draw("same")

    l3 = ut.prepare_leg(0.45, 0.75, 0.25, 0.12, 0.027)
    l3.AddEntry("", "Specrometer dipole:", "")
    l3.AddEntry("", "Center #it{z}: "+str(mag.zpos), "")
    l3.AddEntry("", "Radius: "+str(mag.r1), "")
    l3.AddEntry("", "Lenght in #it{z}: "+str(mag.dz), "")
    l3.Draw("same")

    l4 = ut.prepare_leg(0.15, 0.75, 0.25, 0.15, 0.027)
    l4.AddEntry("", "Up detector:", "")
    l4.AddEntry("", "Center #it{z}: "+"{0:.1f}".format(up.zpos), "")
    l4.AddEntry("", "Center #it{y}: "+"{0:.1f}".format(up.ypos), "")
    l4.AddEntry("", "Size in #it{xy}: "+str(up.dy), "")
    l4.AddEntry("", "Lenght in #it{z}: "+str(up.dz), "")
    l4.Draw("same")

    l5 = ut.prepare_leg(0.1, 0.12, 0.25, 0.15, 0.027)
    l5.AddEntry("", "Down detector:", "")
    l5.AddEntry("", "Center #it{z}: "+"{0:.1f}".format(down.zpos), "")
    l5.AddEntry("", "Center #it{y}: "+"{0:.1f}".format(down.ypos), "")
    l5.AddEntry("", "Size in #it{xy}: "+str(down.dy), "")
    l5.AddEntry("", "Lenght in #it{z}: "+str(down.dz), "")
    l5.Draw("same")

    l6 = ut.prepare_leg(0.3, 0.11, 0.25, 0.12, 0.027)
    l6.AddEntry("", "Photon detector:", "")
    l6.AddEntry("", "Center #it{z}: "+"{0:.1f}".format(phot.zpos), "")
    l6.AddEntry("", "Size in #it{xy}: "+str(phot.dy), "")
    l6.AddEntry("", "Lenght in #it{z}: "+str(phot.dz), "")
    l6.Draw("same")

    l7 = ut.prepare_leg(0.5, 0.11, 0.25, 0.12, 0.027)
    l7.AddEntry("", "B2BeR magnet:", "")
    l7.AddEntry("", "Center #it{z}: "+str(b2b.zpos), "")
    l7.AddEntry("", "Radius: "+str(b2b.r1), "")
    l7.AddEntry("", "Lenght in #it{z}: "+str(b2b.dz), "")
    l7.Draw("same")

    l8 = ut.prepare_leg(0.3, 0.92, 0.25, 0.01, 0.03)
    l8.AddEntry("", "Luminosity layout, side view. All dimensions in mm.", "")
    l8.Draw("same")

    #gPad.SetGrid()

    ut.invert_col(gPad)
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

