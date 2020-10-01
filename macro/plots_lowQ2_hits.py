#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem

import plot_utils as ut
from BoxCalV2Hits import BoxCalV2Hits

#_____________________________________________________________________________
def main():

    #infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_1Mevt.root"
    #infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_NoFilter_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_Qd_beff2_5Mevt.root"
    #infile = "../data/lmon_18x275_qr_Qd_beff2_1Mevt.root"
    infile = "../data/lmon_py_18x275_Q2all_beff2_5Mevt.root"

    iplot = 1
    funclist = []
    funclist.append( hits_xy_s1 ) # 0
    funclist.append( hits_xy_s2 ) # 1
    funclist.append( hits_en_z_s1 ) # 2
    funclist.append( hits_en_z_s2 ) # 3
    funclist.append( hits_en ) # 4
    funclist.append( rate_xy_s1 ) # 5

    #input
    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("DetectorTree")

    #tree.Print()
    #return

    #call the plot function
    funclist[iplot]()

#main

#_____________________________________________________________________________
def hits_xy_s1():

    #hits on s1 tagger in xy

    #bin in mm
    xybin = 3

    #tagger location in x and z
    xpos = 528.56 # mm
    zpos = -24000 # mm
    rot_y = -0.018332 # rad, rotation in x-z plane by rotation along y
    #rot_y = 0

    #front area, mm
    xysiz = 430

    #minimal z to select the front face
    zmin = -5 # mm

    #minimal energy for the hit
    emin = 1 # GeV

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xysiz/2., xysiz/2., xybin, -xysiz/2., xysiz/2.)

    #nevt = tree.GetEntries()
    nevt = 1000000

    hits = BoxCalV2Hits("lowQ2s1", tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        for ihit in xrange(hits.GetN()):

            hit = hits.GetHit(ihit)
            hit.GlobalToLocal(xpos, 0, zpos, rot_y)

            if hit.z < zmin: continue
            if hit.en < emin: continue

            hXY.Fill(hit.x, hit.y)


    ut.put_yx_tit(hXY, "#it{x} (mm)", "#it{y} (mm)")
    ut.set_margin_lbtr(gPad, 0.11, 0.08, 0.01, 0.12)

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_xy_s1

#_____________________________________________________________________________
def hits_xy_s2():

    #hits on s2 tagger in xy

    #Tagger 2 position
    xpos = 661.88 # mm
    zpos = -37000 # mm
    rot_y = -0.018332 # rad

    #front area, mm
    xysiz = 330

    #minimal z to select the front face
    zmin = -5 # mm

    #bin in mm
    xybin = 3

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xysiz/2., xysiz/2., xybin, -xysiz/2., xysiz/2.)

    #nevt = tree.GetEntries()
    nevt = 100000

    hits = BoxCalV2Hits("lowQ2s2", tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        for ihit in xrange(hits.GetN()):
            hit = hits.GetHit(ihit)
            hit.GlobalToLocal(xpos, 0, zpos, rot_y)

            if hit.z < zmin: continue
            #if hit.en < emin: continue

            hXY.Fill(hit.x, hit.y)

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_xy_s2

#_____________________________________________________________________________
def hits_en_z_s1():

    #energy along the z position of the hit in s1

    #tagger location in x and z
    xpos = 528.56 # mm
    zpos = -24000 # mm
    rot_y = -0.018332 # rad, rotation in x-z plane by rotation along y

    zbin = 0.05 # cm
    zmax = 2 # cm
    #zmin = -36 # cm
    zmin = -2 # cm

    ebin = 0.1
    emin = 0
    emax = 20

    can = ut.box_canvas()
    hEnZ = ut.prepare_TH2D("hEnZ", zbin, zmin, zmax, ebin, emin, emax)

    ut.put_yx_tit(hEnZ, "#it{E} (GeV)", "#it{z} (cm)")

    nevt = tree.GetEntries()
    #nevt = 100000

    hits = BoxCalV2Hits("lowQ2s1", tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        for ihit in xrange(hits.GetN()):

            hit = hits.GetHit(ihit)
            hit.GlobalToLocal(xpos, 0, zpos, rot_y)

            hEnZ.Fill( hit.z/10, hit.en) # cm

    hEnZ.SetMinimum(0.98)
    hEnZ.SetContour(300)

    hEnZ.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_en_z_s1

#_____________________________________________________________________________
def hits_en_z_s2():

    #energy along the z position of the hit in s2

    #Tagger 2 position
    xpos = 661.88 # mm
    zpos = -37000 # mm
    rot_y = -0.018332 # rad

    zbin = 0.1 # cm
    zmax = 2 # cm
    #zmin = -36 # cm
    zmin = -2 # cm

    ebin = 0.1
    emin = 0
    emax = 20

    can = ut.box_canvas()
    hEnZ = ut.prepare_TH2D("hEnZ", zbin, zmin, zmax, ebin, emin, emax)
    ut.put_yx_tit(hEnZ, "#it{E} (GeV)", "#it{z} (cm)")

    nevt = tree.GetEntries()
    #nevt = 100000

    hits = BoxCalV2Hits("lowQ2s2", tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        for ihit in xrange(hits.GetN()):

            hit = hits.GetHit(ihit)
            hit.GlobalToLocal(xpos, 0, zpos, rot_y)

            hEnZ.Fill( hit.z/10, hit.en) # cm

    hEnZ.SetMinimum(0.98)
    hEnZ.SetContour(300)

    hEnZ.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_en_z_s2

#_____________________________________________________________________________
def hits_en():

    #energy of the hits

    ebin = 0.1
    emin = 0
    emax = 20

    name = "lowQ2s1"
    #name = "lowQ2s2"

    can = ut.box_canvas()
    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    nevt = tree.GetEntries()
    #nevt = 10000

    hits = BoxCalV2Hits(name, tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        nhit = hits.GetN()
        if nhit <= 0: continue

        en_evt = 0.
        for ihit in xrange(nhit):
            en_evt += hits.GetEn(ihit)

        hE.Fill( en_evt )

    hE.Draw()

    gPad.SetGrid()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#hits_en

#_____________________________________________________________________________
def rate_xy_s1():

    #event rate on the front of s1 tagger in xy

    #size of bin (pad) in xy, mm
    xybin = 1

    #tagger location in x and z
    xpos = 528.56 # mm
    zpos = -24000 # mm

    #front area, mm
    xysiz = 430

    #instantaneous luminosity
    lumi = 1.45e6 # mb^-1 s^-1

    #energy acceptance for tagger 1
    acc = ["5.9", "12"] # GeV

    #generator input with total cross section
    inp_gen = TFile.Open("/home/jaroslav/sim/lgen/data/lgen_18x275_zeus_0p1GeV_beff2_1Mevt.root")
    tree_gen = inp_gen.Get("ltree")
    sigma = 276.346654276 # mb, zeus 0.1 GeV

    #fiducial cross section based on energy acceptance
    sigma_fid = sigma*float(tree_gen.Draw("", "el_en>"+acc[0]+" && el_en<"+acc[1]))/tree_gen.GetEntries()

    print "Generator cross section:", sigma, "mb"
    print "Fiducial cross section:", sigma_fid, "mb"

    #units to show the rate
    #rate_units = 1e-6 # MHz
    rate_units = 1e-3 # kHz

    #minimal z to select the front face
    zmin = -10 # mm

    #minimal energy for the hit
    emin = 1 # GeV

    can = ut.box_canvas()
    hXY = ut.prepare_TH2D("hXY", xybin, -xysiz/2., xysiz/2., xybin, -xysiz/2., xysiz/2.)
    hE = ut.prepare_TH1D("hE", 0.1, 0, 20)

    nevt = tree.GetEntries()
    #nevt = 10000

    #generated electron energy
    gROOT.ProcessLine("struct Entry {Double_t val;};")
    el_gen = rt.Entry()
    tree.SetBranchAddress("el_gen", rt.AddressOf(el_gen, "val"))

    #events with hit
    nevt_hit = 0

    #event loop
    hits = BoxCalV2Hits("lowQ2s1", tree)
    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        if hits.GetN() > 0: nevt_hit += 1
        hit_sel = False

        for ihit in xrange(hits.GetN()):

            hit = hits.GetHit(ihit)
            hit.GlobalToLocal(xpos, 0, zpos)

            if hit.z < zmin: continue
            if hit.en < emin: continue

            hit_sel = True

            hXY.Fill(hit.x, hit.y)

        if hit_sel: hE.Fill(el_gen.val)

    #total hits
    nhit_all = hXY.GetEntries()

    print "Events with hit:", nevt_hit
    print "All selected hits:", nhit_all
    print "Selected hits per event:", nhit_all/nevt

    #total event rate
    print "Total event rate:", 1e-6*sigma_fid*lumi*nhit_all/nevt, "MHz"

    #get the rate from counts in x and y
    hXY.Scale(rate_units*sigma_fid*lumi/nevt)

    ut.put_yx_tit(hXY, "#it{x} (mm)", "#it{y} (mm)")
    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.05, 0.2)

    #hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw()
    #hE.Draw()

    gPad.SetGrid()

    #gPad.SetLogz()
    #gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rate_xy_s1


#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

    #beep when finished
    gSystem.Exec("mplayer computerbeep_1.mp3 > /dev/null 2>&1")



















