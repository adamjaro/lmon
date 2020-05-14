#!/usr/bin/python

from math import sqrt, cos, log, tan, pi, log10

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TMath, AddressOf
from ROOT import TLorentzVector, TDatabasePDG, TCrown

import plot_utils as ut

#_____________________________________________________________________________
def main():

    #infile = "../data/test/lmon.root"
    #infile = "../data/lmon_18x275_lowQ2_1Mevt.root"
    #infile = "../data/lmon_18x275_lowQ2_only_1Mevt.root"
    #infile = "../data/lmon_18x275_lowQ2_47p2cm_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_lowQ2_47p2cm_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_xB_yA_lowQ2_B2eRv2_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_xC_yA_1Mevt.root"
    #infile = "../data/lmon_18x275_qr_Qb_10Mevt.root"
    #infile = "../data/lmon_18x275_qr_Qb_beff2_1Mevt.root"
    #infile = "../data/lmon_pythia_5M_5Mevt.root"
    #infile = "../data/lmon_pythia_5M_beff2_1Mevt.root"
    #infile = "../data/lmon_pythia_5M_beff2_5Mevt.root"
    #infile = "../data/lmon_18x275_beff2_1Mevt_v2.root"
    #infile = "../data/lmon_beam_18_beff2_10Mevt.root"
    #infile = "../data/lmon_18x275_qr_Qb_beff2_Q3eR_1Mevt.root"
    infile = "../data/ir6/lmon_pythia_5M_beff2_5Mevt.root"
    #infile = "../data/ir6_close/lmon_pythia_5M_beff2_close_5Mevt.root"

    iplot = 7
    funclist = []
    funclist.append( el_en ) # 0
    funclist.append( el_theta ) # 1
    funclist.append( el_phi ) # 2
    funclist.append( q2_calc ) # 3
    funclist.append( el_hit_x ) # 4
    funclist.append( el_hit_y ) # 5
    funclist.append( el_hit_z ) # 6
    funclist.append( el_hit_xy ) # 7
    funclist.append( el_Q3eR_xy ) # 8
    funclist.append( gen_vtx_z ) # 9

    #input
    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("DetectorTree")

    #selection for hit in tagger, contains B2eR aperture
    global gQ2sel
    #gQ2sel = "lowQ2_IsHit==1 && TMath::Pi()-el_theta<0.01021"
    gQ2sel = "lowQ2_IsHit==1"

    #call the plot function
    funclist[iplot]()

#main

#_____________________________________________________________________________
def el_en():

    #electron energy for all events and for electrons hitting the tagger

    ebin = 0.1
    emin = 0
    emax = 20

    can = ut.box_canvas()

    #all generated electrons
    hEnAll = ut.prepare_TH1D("hEnAll", ebin, emin, emax)

    #electrons hitting the tagger
    hEnTag = ut.prepare_TH1D("hEnTag", ebin, emin, emax)

    tree.Draw("el_gen >> hEnAll")
    #tree.Draw("el_gen >> hEnTag", "lowQ2_IsHit == 1")
    #tree.Draw("lowQ2_en/1e3 >> hEnTag", "lowQ2_IsHit == 1")
    #tree.Draw("lowQ2_EnPrim/1e3 >> hEnTag", "lowQ2_IsHit == 1")

    ut.line_h1(hEnAll) # , rt.kBlack
    ut.set_H1D_col(hEnTag, rt.kRed)

    hEnAll.SetYTitle("Events / ({0:.3f}".format(ebin)+" GeV)")
    hEnAll.SetXTitle("#it{E}_{e^{-}} (GeV)")

    hEnAll.SetTitleOffset(1.5, "Y")
    hEnAll.SetTitleOffset(1.3, "X")

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.05, 0.02)

    hEnAll.Draw()
    #hEnTag.Draw("same")
    #hEnTag.Draw()

    leg = ut.prepare_leg(0.2, 0.8, 0.2, 0.1, 0.035)
    #leg.AddEntry(hEnAll, "All electrons", "l")
    #leg.AddEntry(hEnAll, "All quasi-real electrons", "l")
    leg.AddEntry(hEnAll, "All bremsstrahlung electrons", "l")
    #leg.AddEntry(hEnTag, "Electrons hitting the tagger", "l")
    #leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_en

#_____________________________________________________________________________
def el_theta():

    #electron generated polar angle

    tbin = 1e-3
    #tmin = 3
    #tmax = TMath.Pi()
    tmin = 0
    #tmax = 1e-1
    tmax = 0.04

    can = ut.box_canvas()

    hTheta = ut.prepare_TH1D("hTheta", tbin, tmin, tmax)

    #tree.Draw("el_theta >> hTheta")
    tree.Draw("TMath::Pi()-el_theta >> hTheta")

    gPad.SetLogy()

    hTheta.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_theta

#_____________________________________________________________________________
def el_phi():

    #electron generated azimuthal angle

    pbin = 1e-1
    pmin = -TMath.Pi()
    pmax = TMath.Pi()


    can = ut.box_canvas()

    hPhi = ut.prepare_TH1D("hPhi", pbin, pmin, pmax)

    tree.Draw("el_phi >> hPhi")

    #gPad.SetLogy()

    hPhi.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_phi

#_____________________________________________________________________________
def q2_calc():

    #calculate the generated Q^2 from definition and from kinematics

    qbin = 1e-6
    qmin = 1e-7
    qmax = 3e-2

    lqbin = 5e-2
    lqmin = -5
    lqmax = 2

    can = ut.box_canvas()

    hQ2def = ut.prepare_TH1D("hQ2def", qbin, qmin, qmax)
    hQ2defTag = ut.prepare_TH1D("hQ2defTag", qbin, qmin, qmax)

    hQ2kine = ut.prepare_TH1D("hQ2kine", qbin, qmin, qmax)
    hQ2kineTag = ut.prepare_TH1D("hQ2kineTag", qbin, qmin, qmax)

    hLog10q2Def = ut.prepare_TH1D("hLog10q2Def", lqbin, lqmin, lqmax)
    hLog10q2DefTag = ut.prepare_TH1D("hLog10q2DefTag", lqbin, lqmin, lqmax)

    hLog10q2kine = ut.prepare_TH1D("hLog10q2kine", lqbin, lqmin, lqmax)
    hLog10q2kineTag = ut.prepare_TH1D("hLog10q2kineTag", lqbin, lqmin, lqmax)

    #set the tree
    tree.SetBranchStatus("*", 0)
    tree.SetBranchStatus("el_gen", 1)
    tree.SetBranchStatus("el_theta", 1)
    tree.SetBranchStatus("el_phi", 1)
    tree.SetBranchStatus("lowQ2_IsHit", 1)

    #connect the generated electron variables
    gROOT.ProcessLine("struct Entry {Double_t val;};")
    gROOT.ProcessLine("struct EntryBool {Bool_t val;};")
    en = rt.Entry()
    theta = rt.Entry()
    phi = rt.Entry()
    is_hit = rt.EntryBool()
    tree.SetBranchAddress("el_gen", AddressOf(en, "val"))
    tree.SetBranchAddress("el_theta", AddressOf(theta, "val"))
    tree.SetBranchAddress("el_phi", AddressOf(phi, "val"))
    tree.SetBranchAddress("lowQ2_IsHit", AddressOf(is_hit, "val"))

    nevt = tree.GetEntries()
    #nevt = 30000

    #counters for skipped entries
    nskip_def = 0
    nskip_kine = 0

    #tree loop
    for i in xrange(nevt):
        tree.GetEntry(i)

        #if en.val > 10: continue

        #vector of beam electron
        el_beam = TLorentzVector()
        el_beam.SetPxPyPzE(0, 0, -18, 18);

        #scattered electron Lorentz vector
        el_vec = q2_calc_vec_from_kine(en.val, theta.val, phi.val)

        q2_def = -(el_beam - el_vec).Mag2()

        hQ2def.Fill( q2_def )
        if is_hit.val == 1: hQ2defTag.Fill( q2_def )

        #if q2_def < 1e-4: continue

        q2kine = 2.*18*en.val*(1-cos(pi-theta.val))

        hQ2kine.Fill( q2kine )
        if is_hit.val == 1: hQ2kineTag.Fill( q2kine )

        if q2_def > 0.:
            hLog10q2Def.Fill( log10(q2_def) )
            if is_hit.val == 1: hLog10q2DefTag.Fill( log10(q2_def) )
            #print log10(q2_def)
        else:
            nskip_def += 1

        if q2kine > 0.:
            hLog10q2kine.Fill( log10(q2kine) )
            if is_hit.val == 1: hLog10q2kineTag.Fill( log10(q2kine) )
        else:
            nskip_kine += 1

        #print q2_def, q2, q2_def-q2

        #print el_vec.Px(), el_vec.Py(), el_vec.Pz()

    #tree loop

    #release the tree at the end
    tree.ResetBranchAddresses()
    tree.SetBranchStatus("*", 1)

    print "Events skipped for Q^2 from definition:", nskip_def
    print "Events skipped for Q^2 from kinematics:", nskip_kine

    #draw the plot

    ut.set_H1D_col(hQ2defTag, rt.kRed)
    ut.set_H1D_col(hQ2kine, rt.kBlue)
    ut.set_H1D_col(hQ2kineTag, rt.kMagenta)

    #gPad.SetLogy()
    #gPad.SetLogx()

    #hQ2def.Draw()
    #hQ2defTag.Draw("e1same")
    #hQ2kine.Draw("e1same")
    #hQ2kineTag.Draw("e1same")

    ut.set_H1D_col(hLog10q2DefTag, rt.kRed)
    ut.set_H1D_col(hLog10q2kine, rt.kBlue)
    ut.set_H1D_col(hLog10q2kineTag, rt.kMagenta)

    hLog10q2Def.Draw()
    hLog10q2DefTag.Draw("e1same")
    #hLog10q2kine.Draw("e1same")
    #hLog10q2kineTag.Draw("e1same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#q2_calc

#_____________________________________________________________________________
def q2_calc_vec_from_kine(en, theta, phi):

    #create Lorentz vector from electron kinematics loaded from the tree

    #transverse momentum
    m = TDatabasePDG.Instance().GetParticle(11).Mass()
    pt = sqrt( 0.5*(en**2 - m**2)*(1.-cos(2.*theta)) )

    #pseudorapidity
    eta = -log( tan(theta/2.) )

    #set the Lorentz vector
    vec = TLorentzVector()
    vec.SetPtEtaPhiE(pt, eta, phi, en)

    return vec

#q2_calc_vec_from_kine

#_____________________________________________________________________________
def el_hit_x():

    #electron hit on the tagger in x

    xbin = 1
    xmin = 350
    xmax = 600

    can = ut.box_canvas()

    #x of the electron
    hX = ut.prepare_TH1D("hX", xbin, xmin, xmax)

    tree.Draw("lowQ2_hx >> hX", "lowQ2_IsHit == 1")
    #tree.Draw("lowQ2_hx >> hX")

    hX.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_hit_x

#_____________________________________________________________________________
def el_hit_y():

    #electron hit on the tagger in y

    ybin = 0.1
    ymin = -8
    ymax = 8
    #ymin = -110
    #ymax = 110

    can = ut.box_canvas()

    #y of the electron
    hY = ut.prepare_TH1D("hY", ybin, ymin, ymax)

    tree.Draw("lowQ2_hy >> hY", "lowQ2_IsHit == 1")
    #tree.Draw("lowQ2_hy >> hY")

    gPad.SetLogy()

    hY.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_hit_y

#_____________________________________________________________________________
def el_hit_z():

    #electron hit on the tagger in z

    zbin = 1e-3
    zmin = -27.4
    zmax = -26.9

    can = ut.box_canvas()

    #z of the electron
    hZ = ut.prepare_TH1D("hZ", zbin, zmin, zmax)

    #tree.Draw("lowQ2_hz/1e3 >> hZ", "lowQ2_IsHit == 1")
    tree.Draw("lowQ2_hz/1e3 >> hZ", gQ2sel)
    #tree.Draw("lowQ2_hz/1e3 >> hZ")

    gPad.SetLogy()

    hZ.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_hit_z

#_____________________________________________________________________________
def el_hit_xy():

    #electron hit on the tagger in x and y

    #xybin = 0.3 # s1
    #xpos = 51
    #xysiz = 42
    #xybin = 0.1 # s2
    #xpos = 63
    #xysiz = 28
    xybin = 0.5 # ecal
    xpos = 0
    xysiz = 200
    #xpos = 472 # Q3eR
    #xysiz = 20
    #xybin = 0.1

    #ybin = 1

    #nam = "lowQ2s1"
    #nam = "lowQ2s2"
    nam = "ecal"
    #nam = "Q3eR"

    can = ut.box_canvas()

    #x and y of the electrons
    hXY = ut.prepare_TH2D("hXY", xybin, xpos-(xysiz/2.), xpos+(xysiz/2.), xybin, -xysiz/2., xysiz/2.)
    #hXY = ut.prepare_TH2D_n("hXY", 50, xmin, xmax, 50, ymin, ymax)

    tree.Draw(nam+"_hy/10:"+nam+"_hx/10 >> hXY", nam+"_IsHit==1")
    #tree.Draw("lowQ2_hy:lowQ2_hx >> hXY")

    print "Entries:", hXY.GetEntries()

    ut.put_yx_tit(hXY, "Vertical #it{y} (cm)", "Horizontal #it{x} (cm)", 1.4, 1.2)

    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.09, 0.12)

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)
    hXY.GetXaxis().SetMoreLogLabels()

    hXY.Draw()

    gPad.SetGrid()

    gPad.SetLogz()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_hit_xy

#_____________________________________________________________________________
def el_Q3eR_xy():

    #electron hit at Q3eR position in x and y

    #dxy = 25
    #dxy = 140
    dxy = 700

    #xbin = 0.1
    xbin = 1
    xmin = 400
    #xmin = 460
    xmax = xmin+dxy

    #ybin = 0.1
    ybin = 1
    #ymin = -50
    ymin = -dxy/2
    ymax = ymin+dxy

    can = ut.box_canvas()

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    #tree.Draw("Q3eR_hy:Q3eR_hx >> hXY", "Q3eR_IsHit==1")
    #tree.Draw("Q3eR_hy:Q3eR_hx >> hXY", "", "", 10000)
    #tree.Draw("Q3eR_hy:Q3eR_hx >> hXY", "Q3eR_hx>500")
    tree.Draw("Q3eR_hy:Q3eR_hx >> hXY")

    print "Entries:", hXY.GetEntries()

    ut.put_yx_tit(hXY, "Vertical #it{y} (mm)", "Horizontal #it{x} (mm)", 1.4, 1.2)

    ut.set_margin_lbtr(gPad, 0.1, 0.09, 0.08, 0.12)

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    hXY.Draw()

    #Q3eR entering radius
    r1 = TCrown(472.033, 0, 40, 0)
    r1.SetLineColor(rt.kOrange)
    r1.SetLineStyle(rt.kDashed)
    r1.SetLineWidth(3)
    r1.Draw("same")

    gPad.SetGrid()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_Q3eR_xy

#_____________________________________________________________________________
def gen_vtx_z():

    #generated vertex position along z

    vbin = 1
    vmin = -100
    vmax = 100

    can = ut.box_canvas()
    hZ = ut.prepare_TH1D("hZ", vbin, vmin, vmax)

    tree.Draw("vtx_z >> hZ")

    #gPad.SetLogy()

    hZ.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_vtx_z

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()




















