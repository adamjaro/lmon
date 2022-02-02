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
    zmax = -4000.
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
    geo = rt.GeoParser("../../config/pro2/geom_pro2.in")

    #Q1eR magnet
    q1 = magnet("Q1eR", geo)
    q1.label = "Q1eR"
    q1.draw()

    #Q2eR magnet
    q2 = magnet("Q2eR", geo)
    q2.label = "Q2eR"
    q2.draw()

    #B2eR magnet
    b2 = magnet("B2eR", geo)
    b2.label = "B2eR"
    b2.draw()

    #Q3eR magnet
    q3 = magnet("Q3eR", geo)
    q3.label = "Q3eR"
    q3.draw()

    #vacuum from Q1eR to Q2eR
    q1q2 = vacuum(geo)
    q1q2.add_point_const("Q1eR_End_Z", "Q1eR_InnerRadius", -1)
    q1q2.add_point_const("Q2eR_Start_Z", "Q1eR_InnerRadius", -1)
    q1q2.add_point_const("Q2eR_Start_Z", "Q1eR_InnerRadius")
    q1q2.add_point_const("Q1eR_End_Z", "Q1eR_InnerRadius")
    q1q2.draw()

    #vacuum from Q2eR to B2eR
    q2b2 = vacuum(geo)
    q2b2.add_point_const("Q2eR_End_Z", "Q2eR_InnerRadius", -1)
    q2b2.add_point_const("B2eR_Start_Z", "Q2eR_InnerRadius", -1)
    q2b2.add_point_const("B2eR_Start_Z", "Q2eR_InnerRadius")
    q2b2.add_point_const("Q2eR_End_Z", "Q2eR_InnerRadius")
    q2b2.draw()

    #beam vacuum
    bvac = vacuum(geo)
    bvac.add_point("vac_B2", "z1BI", "x1BI")
    bvac.add_point("vac_win_tag1", "z0BI", "x0BI")
    bvac.add_point("vac_win_tag1", "z0TO", "x0TO")
    bvac.add_point("vac_win_tag2", "z0BI", "x0BI")
    bvac.add_point("vac_win_tag2", "z0TO", "x0TO")
    bvac.add_point("vac_Q3", "z0BI", "x0BI")
    bvac.add_point("vac_Q3", "z0TI", "x0TI")
    bvac.add_point_2("vac_B2.z0TO", "ExitWinBox.dx", -0.5)
    bvac.add_point("vac_B2", "z0TO", "x0TI")
    bvac.add_point("vac_B2", "z1TI", "x1TI")
    bvac.draw()

    #Luminosity exit window
    ew = segment("ExitWinBox", geo)
    ew.label = "Exit window"
    ew.fill_col = rt.kGreen+1
    ew.draw()

    #Tagger1
    tag1 = segment("Tagger1box", geo)
    tag1.label = "Tagger 1"
    tag1.draw()

    #Tagger2
    tag2 = segment("Tagger2box", geo)
    tag2.label = "Tagger 2"
    tag2.draw()

    leg = ut.prepare_leg(0.8, 0.21, 0.25, 0.15, 0.03)#, 0.027) # x, y, dx, dy, tsiz
    leg.AddEntry(tag1.gbox, "Detector", "f")
    leg.AddEntry(b2.gbox, "Magnet", "f")
    leg.AddEntry(bvac.gbox, "Vacuum", "f")
    leg.Draw("same")

    gPad.SetGrid()

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

