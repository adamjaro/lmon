#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, AddressOf

import plot_utils as ut

#_____________________________________________________________________________
def plot_nphot_det(det):

    #number of photoelectrons per detector cell

    ncells = 7

    dx = 10.5

    if det == "phot":
        dy = [-10.5, 10.5]
    if det == "up":
        dy = [4.2, 25.2]
    if det == "down":
        dy = [-25.2, -4.2]

    nevt = 1000

    can = ut.box_canvas()

    hCells = ut.prepare_TH2D_n("hCells", ncells, -dx, dx, ncells, dy[0], dy[1])

    #cells loop
    gROOT.ProcessLine("struct Entry {ULong64_t val;};")
    entry = rt.Entry()
    for ix in xrange(ncells):
        for iy in xrange(ncells):
    #for ix in xrange(0,1):
    #    for iy in xrange(0,1):

            #branch for the cell
            xform = "{0:02d}".format(ix)
            yform = "{0:02d}".format(iy)
            bnam = det + "_" + xform + "x" + yform + "_OpDet_nphot"

            #photoelectrons in the cell
            tree.ResetBranchAddresses()
            tree.SetBranchStatus("*", 0)
            tree.SetBranchStatus(bnam, 1)
            tree.SetBranchAddress(bnam, AddressOf(entry, "val"))
            nphot_cell = 0
            for i in xrange(nevt):
                tree.GetEntry(i)
                nphot_cell += entry.val

            #print xform, yform, ecell/1000./nevt

            hCells.SetBinContent(ix+1, ncells-iy, float(nphot_cell)/nevt)

    hCells.SetXTitle("Horizontal #it{x} (cm)")
    hCells.SetYTitle("Vertical #it{y} (cm)")

    hCells.GetXaxis().CenterTitle()
    hCells.GetYaxis().CenterTitle()

    hCells.SetTitleOffset(1.2, "Y")
    hCells.SetTitleOffset(1.2, "X")

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.12)
    gPad.SetBottomMargin(0.09)
    gPad.SetLeftMargin(0.09)

    hCells.Draw()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_nphot_det


#_____________________________________________________________________________
def plot_en(det):

    #energy per detector cell

    ncells = 7

    dx = 10.5

    if det == "phot":
        dy = [-10.5, 10.5]
    if det == "up":
        dy = [4.2, 25.2]
    if det == "down":
        dy = [-25.2, -4.2]

    nevt = 1000

    can = ut.box_canvas()

    hCells = ut.prepare_TH2D_n("hCells", ncells, -dx, dx, ncells, dy[0], dy[1])

    #cells loop
    gROOT.ProcessLine("struct Entry {Double_t val;};")
    entry = rt.Entry()
    for ix in xrange(ncells):
        for iy in xrange(ncells):
    #for ix in xrange(0,1):
    #    for iy in xrange(0,1):

            #branch for the cell
            xform = "{0:02d}".format(ix)
            yform = "{0:02d}".format(iy)
            bnam = det + "_" + xform + "x" + yform + "_en"

            #energy in the cell
            tree.ResetBranchAddresses()
            tree.SetBranchStatus("*", 0)
            tree.SetBranchStatus(bnam, 1)
            tree.SetBranchAddress(bnam, AddressOf(entry, "val"))
            ecell = 0.
            for i in xrange(nevt):
                tree.GetEntry(i)
                ecell += entry.val

            #print xform, yform, ecell/1000./nevt

            hCells.SetBinContent(ix+1, ncells-iy, ecell/1000./nevt)

    hCells.SetXTitle("Horizontal #it{x} (cm)")
    hCells.SetYTitle("Vertical #it{y} (cm)")

    hCells.GetXaxis().CenterTitle()
    hCells.GetYaxis().CenterTitle()

    hCells.SetTitleOffset(1.2, "Y")
    hCells.SetTitleOffset(1.2, "X")

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.12)
    gPad.SetBottomMargin(0.09)
    gPad.SetLeftMargin(0.09)

    hCells.Draw()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#plot_en

#_____________________________________________________________________________
if __name__ == "__main__":

    infile = "../data/lmon.root"
    #infile = "../data/pdet2_uni_0p5_20GeV_1kevt.daq.root"


    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 0
    det = "phot"

    funclist = []
    funclist.append( plot_en ) # 0
    funclist.append( plot_nphot_det ) # 1

    #open the input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #call the plot function
    funclist[iplot](det)

















