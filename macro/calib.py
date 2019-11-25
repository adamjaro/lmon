#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, AddressOf
from ROOT import TGraph, TF1

from ROOT import RooFit as rf
from ROOT import RooRealVar, RooDataHist, RooArgList, RooBreitWigner

import plot_utils as ut
from parameter_descriptor import parameter_descriptor as pdesc

#_____________________________________________________________________________
def resolution():

    #relative energy resolution

    #ALICE PHOS has 3% in 0.2 - 10 GeV, PHOS TDR page 113 (127)

    emin = -0.4
    emax = 0.4
    ebin = 0.01

    #reconstruct the energy from detected optical photons

    gRec = rec(False)

    #construct the relative energy resolution
    nbins, emax = ut.get_nbins(ebin, emin, emax)
    hRes = ut.prepare_TH1D_n("hRes", nbins, emin, emax)

    egen = rt.Double()
    erec = rt.Double()
    for i in xrange(gRec.GetN()):
        gRec.GetPoint(i, egen, erec)
        hRes.Fill( (erec-egen)/egen )

    #fit the resolution with Breit-Wigner pdf
    x = RooRealVar("x", "x", -0.5, 0.5)
    x.setRange("fitran", -0.21, 0.21)
    rfRes = RooDataHist("rfRes", "rfRes", RooArgList(x), hRes)

    #Breit-Wigner pdf
    mean = RooRealVar("mean", "mean", 0., -0.1, 0.1)
    sigma = RooRealVar("sigma", "sigma", 0.01, 0., 0.9)
    bwpdf = RooBreitWigner("bwpdf", "bwpdf", x, mean, sigma)

    rfres = bwpdf.fitTo(rfRes, rf.Range("fitran"), rf.Save())

    #log the results to a file
    out = open("out.txt", "w")
    out.write(ut.log_fit_result(rfres))

    #plot the resolution
    can = ut.box_canvas()

    frame = x.frame(rf.Bins(nbins), rf.Title(""))
    frame.SetTitle("")
    frame.SetXTitle("Relative energy resolution (#it{E}_{rec}-#it{E}_{gen})/#it{E}_{gen}")

    frame.GetXaxis().SetTitleOffset(1.4)
    frame.GetYaxis().SetTitleOffset(1.6)

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.01, 0.03)

    rfRes.plotOn(frame, rf.Name("data"))

    bwpdf.plotOn(frame, rf.Precision(1e-6), rf.Name("bwpdf"))

    frame.Draw()

    leg = ut.prepare_leg(0.65, 0.78, 0.28, 0.15, 0.035)
    leg.SetMargin(0.17)
    hx = ut.prepare_TH1D("hx", 1, 0, 1)
    hx.Draw("same")
    leg.AddEntry(hx, "#frac{#it{E}_{rec} - #it{E}_{gen}}{#it{E}_{gen}}")
    lx = ut.col_lin(rt.kBlue)
    leg.AddEntry(lx, "Breit-Wigner fit", "l")
    leg.Draw("same")

    #fit parameters on the plot
    desc = pdesc(frame, 0.67, 0.7, 0.05); #x, y, sep
    #desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", frame.chiSquare("bwpdf", "data", 2), -1, rt.kBlue)
    desc.prec = 4
    desc.itemR("mean", mean, rt.kBlue)
    desc.itemR("#sigma", sigma, rt.kBlue)
    desc.draw()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def rec(plot=True):

    #reconstruction from number of detected optical photons to energy
    #and comparison with generated energy

    #calibration function with parameters from the fit
    calib = TF1("calib", "[0]+[1]*x + [2]*x*x", 0, 100)

    #calib.FixParameter(0, 0.0683505)
    #calib.FixParameter(1, 0.265056)
    #calib.FixParameter(2, -0.000238363)

    calib.FixParameter(0, -0.0904673)
    calib.FixParameter(1, 0.278804)
    calib.FixParameter(2, -0.000435157)

    #get number of detected optical photon from the tree
    gROOT.ProcessLine("struct EntryL {ULong64_t val;};")
    gROOT.ProcessLine("struct EntryD {Double_t val;};")
    nphot = rt.EntryL()
    gen = rt.EntryD()

    tree.SetBranchStatus("*", 0)

    tree.SetBranchStatus("phot_nphotDet", 1)
    tree.SetBranchAddress("phot_nphotDet", AddressOf(nphot, "val"))

    tree.SetBranchStatus("phot_gen", 1)
    tree.SetBranchAddress("phot_gen", AddressOf(gen, "val"))

    #reconstructed energy as a function of generated photon energy
    nev = tree.GetEntries()
    gRec = TGraph(nev)

    #tree loop
    for i in xrange(nev):
        tree.GetEntry(i)
        #reconstruct the energy, GeV
        en = calib.Eval( float(nphot.val)/1e3 )
        gRec.SetPoint(i, gen.val/1e3, en)
        #print i, nphot.val, en, gen.val/1e3

    #plot the reconstructed vs. generated graph
    can = ut.box_canvas()
    frame = gPad.DrawFrame(0, 0, 21, 21)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.01, 0.01)

    frame.SetXTitle("Generated energy #it{E}_{gen} (GeV)")
    frame.SetYTitle("Reconstructed energy #it{E}_{rec} (GeV)")

    frame.SetTitleOffset(1.4, "Y")
    frame.SetTitleOffset(1.3, "X")

    gRec.SetMarkerStyle(7)

    gRec.Draw("psame")

    #unity line for rec = gen
    unity = TF1("unity", "x", 0, 21)
    unity.Draw("same")

    leg = ut.prepare_leg(0.15, 0.78, 0.28, 0.15, 0.04)
    leg.SetMargin(0.17)
    leg.AddEntry(unity, "#it{E}_{rec} = #it{E}_{gen}", "l")
    leg.Draw("same")

    if plot:
        ut.invert_col(rt.gPad)
        can.SaveAs("01fig.pdf")

    return gRec

#_____________________________________________________________________________
def calib_graph():

    #calibration graph from number of detected photons to generated energy

    #get the tree
    gROOT.ProcessLine("struct EntryD {Double_t val;};")
    gROOT.ProcessLine("struct EntryL {ULong64_t val;};")

    gen_energy = rt.EntryD()
    nphot = rt.EntryL()

    tree.SetBranchStatus("*", 0)

    tree.SetBranchStatus("phot_gen", 1)
    tree.SetBranchAddress("phot_gen", AddressOf(gen_energy, "val"))

    tree.SetBranchStatus("phot_nphotDet", 1)
    tree.SetBranchAddress("phot_nphotDet", AddressOf(nphot, "val"))

    nev = tree.GetEntries()

    #fill the graph of generated energy as a function of number of detected photons
    gGenNphot = TGraph(nev)

    for i in xrange(nev):
        tree.GetEntry(i)
        gGenNphot.SetPoint(i, float(nphot.val)/1e3, gen_energy.val/1e3)

    #verify values in the graph
    gx = rt.Double()
    gy = rt.Double()
    for i in xrange(gGenNphot.GetN()):
        gGenNphot.GetPoint(i, gx, gy)
        #print i, gx, gy

    #calibration function
    calib = TF1("calib", "[0]+[1]*x + [2]*x*x", 0, 100) # 1, 82   0 100
    calib.SetParameter(0, 0)
    calib.SetParameter(1, 0.2)
    calib.SetParameter(2, -1e-5)

    #calib.FixParameter(2, 0)

    #make the fit
    res = ( gGenNphot.Fit(calib, "RS") ).Get()

    #log the results to a file
    out = open("out.txt", "w")
    out.write(ut.log_tfit_result(res))

    can = ut.box_canvas()
    frame = gPad.DrawFrame(0, 0, 100, 21)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.01, 0.03)

    frame.SetXTitle("Number of photoelectrons #it{N}_{phot} #times 1000")
    frame.SetYTitle("Generated energy #it{E}_{gen} (GeV)")

    frame.SetTitleOffset(1.4, "Y")
    frame.SetTitleOffset(1.4, "X")

    gGenNphot.SetMarkerStyle(7)
    #gGenNphot.SetMarkerSize(1)

    gGenNphot.Draw("psame")

    calib.Draw("same")

    leg = ut.prepare_leg(0.15, 0.8, 0.3, 0.1, 0.04)
    leg.SetMargin(0.17)
    leg.AddEntry(calib, "#it{c}_{0} + #it{c}_{1}#kern[0.05]{#it{N}_{phot}} + #it{c}_{2}#it{N}_{phot}^{2}", "l")
    leg.Draw("same")

    #fit parameters on the plot
    desc = pdesc(frame, 0.64, 0.35, 0.057)
    #desc.set_text_size(0.03)
    desc.itemD("#chi^{2}/ndf", res.Chi2()/res.Ndf(), -1, rt.kRed)
    desc.itemRes("#it{c}_{0}", res, 0, rt.kRed)
    desc.itemRes("#it{c}_{1}", res, 1, rt.kRed)
    desc.prec = 5
    desc.itemRes("#it{c}_{2}", res, 2, rt.kRed)
    desc.draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#calib_graph


#_____________________________________________________________________________
if __name__ == "__main__":

    infile = "../data/lmon.root"
    #infile = "../data/pdet2_uni_0p5_20GeV_1kevt.daq.root"

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 1

    funclist = []
    funclist.append( calib_graph ) # 0
    funclist.append( rec ) # 1
    funclist.append( resolution ) # 2

    #open the input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")

    #call the plot function
    funclist[iplot]()




























