#!/usr/bin/python

import ROOT as rt
from ROOT import TF1, gPad, gROOT, gStyle, TFile, gSystem, AddressOf
from ROOT import TMath

import plot_utils as ut
from BoxCalV2Hits import BoxCalV2Hits
from TagV2Evt import TagV2Evt
from read_con import read_con

#_____________________________________________________________________________
def main():

    #infile = "../data/qr/lmon_qr_18x275_Qe_beff2_5Mevt.root"
    #infile = "../data/py/lmon_py_ep_18x275_Q2all_beff2_5Mevt.root"
    infile = "../data/qr/lmon_qr_18x275_Qf_beff2_5Mevt.root"

    iplot = 7
    funclist = []
    funclist.append( hits_xy_s1 ) # 0
    funclist.append( hits_xy_s2 ) # 1
    funclist.append( hits_en_z_s1 ) # 2
    funclist.append( hits_en_z_s2 ) # 3
    funclist.append( hits_en ) # 4
    funclist.append( rate_xy_s1 ) # 5
    funclist.append( recchar ) # 6
    funclist.append( diff_hitE_trueE ) # 7

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
            #if hit.en < emin: continue

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
def recchar():

    #reconstruction characteristics

    #tagger configuration
    #config = "recchar_s1.ini"
    config = "recchar_s2.ini"

    cf = read_con(config)

    #tagger parametrization
    xpos = cf("xpos")
    zpos = cf("zpos")
    rot_y = cf("rot_y")
    zmin = cf("zmin")

    can = ut.box_canvas(3*768)
    can.Divide(3,1)
    hXY = ut.prepare_TH2D("hXY", cf("xybin"), -cf("xsiz")/2., cf("xsiz")/2., cf("xybin"), -cf("ysiz")/2., cf("ysiz")/2.)
    hET = ut.prepare_TH2D("hET", cf("tbin"), cf("tmin"), cf("tmax"), cf("ebin"), cf("emin"), cf("emax"))
    hQ2 = ut.prepare_TH1D("hQ2", cf("qbin"), cf("qmin"), cf("qmax"))

    #numerical minima and maxima
    xlo = 1e9; xhi = -1e9; ylo = 1e9; yhi = -1e9
    elo = 1e9; ehi = -1e9; tlo = 1e9; thi = -1e9;
    qlo = 1e9; qhi = -1e9;

    nevt = tree.GetEntries()
    #nevt = 1200

    hits = BoxCalV2Hits(cf.str("name"), tree)
    gROOT.ProcessLine("struct Entry {Double_t v;};")
    true_el_theta = rt.Entry()
    true_el_E = rt.Entry()
    true_Q2 = rt.Entry()
    tree.SetBranchAddress("true_el_theta", AddressOf(true_el_theta, "v"))
    tree.SetBranchAddress("true_el_E", AddressOf(true_el_E, "v"))
    tree.SetBranchAddress("true_Q2", AddressOf(true_Q2, "v"))

    for ievt in xrange(nevt):
        tree.GetEntry(ievt)

        nhsel = 0

        for ihit in xrange(hits.GetN()):

            hit = hits.GetHit(ihit)
            hit.GlobalToLocal(xpos, 0, zpos, rot_y)

            if hit.z < zmin: continue

            nhsel += 1

        #just one selected hit
        if nhsel != 1: continue

        #hit coordinats on front of the tagger
        hXY.Fill(hit.x, hit.y)

        if hit.x < xlo: xlo = hit.x
        if hit.y < ylo: ylo = hit.y

        if hit.x > xhi: xhi = hit.x
        if hit.y > yhi: yhi = hit.y

        #true electron energy and angle for the hit
        en = true_el_E.v
        lt = -TMath.Log10(TMath.Pi()-true_el_theta.v)
        hET.Fill(lt, en)

        if en < elo: elo = en
        if en > ehi: ehi = en

        if lt < tlo: tlo = lt
        if lt > thi: thi = lt

        #event true Q^2
        lq = TMath.Log10(true_Q2.v)
        hQ2.Fill( lq )

        if lq < qlo: qlo = lq
        if lq > qhi: qhi = lq

    print "xlo:", xlo, "xhi:", xhi, "ylo:", ylo, "yhi:", yhi
    print "elo:", elo, "ehi:", ehi, "tlo:", tlo, "thi:", thi
    print "qlo:", qlo, "qhi:", qhi

    ut.put_yx_tit(hXY, "#it{y} (mm)", "#it{x} (mm)")
    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    ut.put_yx_tit(hET, "#it{E} (GeV)", "-log_{10}(#pi-#theta) (rad)")
    hET.SetMinimum(0.98)
    hET.SetContour(300)

    ut.put_yx_tit(hQ2, "Counts", "log_{10}(#it{Q}^{2}) (GeV^{2})")
    ut.line_h1(hQ2, rt.kBlue)

    can.cd(1)
    ut.set_margin_lbtr(gPad, 0.11, 0.08, 0.01, 0.12)
    hXY.Draw()
    gPad.SetGrid()
    gPad.SetLogz()

    can.cd(2)
    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.02, 0.12)
    hET.Draw()
    gPad.SetGrid()
    gPad.SetLogz()

    can.cd(3)
    ut.set_margin_lbtr(gPad, 0.11, 0.09, 0.02, 0.12)
    hQ2.Draw()
    gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    ut.invert_col_can(can)
    can.SaveAs("01fig.pdf")

#recchar

#_____________________________________________________________________________
def diff_hitE_trueE():

    #energy in hit and true generated energy

    #tagger configuration
    config = "recchar_s1.ini"
    #config = "recchar_s2.ini"

    cf = read_con(config)

    #event in tagger
    evt = TagV2Evt(tree, cf)

    nevt = tree.GetEntries()
    #nevt = 320

    #difference plot
    ebin = 0.01
    emin = -10
    emax = 10

    hEdiff = ut.prepare_TH1D("hEdiff", ebin, emin, emax)

    can = ut.box_canvas()

    for iev in xrange(nevt):

        if not evt.read(iev): continue

        hEdiff.Fill( (evt.hit_E - evt.true_el_E)*1000. )


    ut.put_yx_tit(hEdiff, "Events", "(#it{E}_{hit} - #it{E}_{true}) #times 1000", 1.4, 1.2)

    hEdiff.Draw()

    gPad.SetLogy()
    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#diff_hitE_trueE

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

    #beep when finished
    gSystem.Exec("mplayer computerbeep_1.mp3 > /dev/null 2>&1")



















