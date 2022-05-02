#!/usr/bin/python3

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TGraph
from ROOT import std

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = single_pulse
    func[1] = multiple_pulses

    func[iplot]()

#_____________________________________________________________________________
def single_pulse():

    #single pulse of photoelectrons for a given event

    inp = "pwo.root"

    ievt = 0

    cell = "03x03"

    infile = TFile.Open(inp)
    tree = infile.Get("DetectorTree")

    tree.Print()

    #return

    #get the hits from the tree
    hitTime = std.vector(float)()
    hitNphot = std.vector(int)()

    tree.SetBranchAddress("cal_"+cell+"_OpDet_hits_time", hitTime)
    tree.SetBranchAddress("cal_"+cell+"_OpDet_hits_nphot", hitNphot)

    tree.GetEntry(ievt)

    nhits = hitTime.size()

    can = ut.box_canvas()

    gHits = TGraph(nhits)

    for i in range(nhits):
        gHits.SetPoint(i, hitTime.at(i), hitNphot.at(i))

    gHits.Draw("A*l")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#single_pulse

#_____________________________________________________________________________
def multiple_pulses():

    #draw signal pulses over multiple events

    inp = "pwo_100evt.root"

    nevt = 100
    #nevt = 1000

    cell = "03x03"

    emin = 17.5  # 0
    emax = 3

    ofs = 0  # 10 or 500

    infile = TFile.Open(inp)
    tree = infile.Get("DetectorTree")

    can = ut.box_canvas()

    #frame = gPad.DrawFrame(100, -6.2e3, 150, 200)
    frame = gPad.DrawFrame(0, -1e3, 30, 200)
    frame.Draw()
    #frame.SetLineColor(rt.kWhite)

    ytit = "Charge (# of photoelectrons)"
    xtit = "Time (ns)"
    ut.put_yx_tit(frame, ytit, xtit, 2.2, 1.3)

    ut.set_margin_lbtr(gPad, 0.15, 0.1, 0.01, 0.03)

    hitTime = std.vector(float)()
    hitNphot = std.vector(int)()

    tree.SetBranchAddress("cal_"+cell+"_OpDet_hits_time", hitTime)
    tree.SetBranchAddress("cal_"+cell+"_OpDet_hits_nphot", hitNphot)

    gROOT.ProcessLine("struct Entry {Double_t val;};")
    phot_en = rt.Entry()
    #tree.SetBranchAddress("phot_en", AddressOf(phot_en, "val"))

    glist = []

    ievt = 0
    for i in range(tree.GetEntriesFast()):

        if i < ofs: continue

        tree.GetEntry(i)

        #if phot_en.val/1e3 < emin: continue
        #if phot_en.val/1e3 < emin and phot_en.val/1e3 > emax:
            #continue

        nhits = hitTime.size()

        glist.append( TGraph(nhits) )
        gh = glist[len(glist)-1]

        for ihit in range(nhits):
            gh.SetPoint(ihit, hitTime.at(ihit), -hitNphot.at(ihit))

        gh.SetLineColor(rt.kBlue)

        gh.Draw("lsame")

        ievt += 1
        if ievt >= nevt: break

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#multiple_pulses

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

