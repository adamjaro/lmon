#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TPad, TCanvas
from ROOT import TLine

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    #infile = "qrec_s1.root"
    #infile = "qrec_s1_xy5.root"
    #infile = "qrec_s2.root"
    #infile = "qrec_s2_xy5.root"
    #infile = "../../data/qr/qrec_uni_s1_qr_18x275_Qf_beff2_5Mevt.root"
    #infile = "../../data/qr/qrec_uni_s2_qr_18x275_Qf_beff2_5Mevt.root"
    #infile = "../../data/py/qrec_uni_s1_py_ep_18x275_Q2all_beff2_5Mevt.root"
    infile = "../../data/py/qrec_uni_s2_py_ep_18x275_Q2all_beff2_5Mevt.root"

    iplot = 1
    funclist = []
    funclist.append( log10_Q2_rto ) # 0
    funclist.append( lQ2_rec_gen ) # 1

    inp = TFile.Open(infile)
    global tree
    tree = inp.Get("Q2rec")

    #tree.Print()

    funclist[iplot]()

#main

#_____________________________________________________________________________
def log10_Q2_rto():

    #reconstructed and generated log_10(Q^2)

    #full range in Q^2
    lqbin = 0.04
    #lqmin = -8
    lqmin = -7
    #lqmax = -1.5
    lqmax = -1

    #minimal Q^2 for ratio plot
    #lrmin = -5
    lrmin = -5.2

    #can = ut.box_canvas()
    can = TCanvas("can", "can", 768, 768)
    gStyle.SetOptStat("")
    gStyle.SetPalette(1)
    gStyle.SetLineWidth(2)
    gStyle.SetPadTickY(1)

    hLog10Q2rec = ut.prepare_TH1D("hLog10Q2rec", lqbin, lqmin, lqmax)
    hLog10Q2gen = ut.prepare_TH1D("hLog10Q2gen", lqbin, lqmin, lqmax)

    #distributions for ratio plot
    hRecRto = ut.prepare_TH1D("hRecRto", lqbin, lrmin, lqmax)
    hGenRto = ut.prepare_TH1D("hGenRto", lqbin, lrmin, lqmax)
    hRtoPlot = ut.prepare_TH1D("hRtoPlot", lqbin, lrmin, lqmax)

    tree.Draw("rec_lq >> hLog10Q2rec")
    tree.Draw("true_lq >> hLog10Q2gen")

    #tree.Draw("lq2_rec >> hRecRto", "lq2_rec>"+str(lrmin))
    #tree.Draw("lq2_gen >> hGenRto", "lq2_rec>"+str(lrmin))
    #tree.Draw("lq2_rec >> hRecRto", "lq2_rec>"+str(lrmin)+" && lq2_gen>"+str(lrmin))
    #tree.Draw("lq2_gen >> hGenRto", "lq2_rec>"+str(lrmin)+" && lq2_gen>"+str(lrmin))
    tree.Draw("rec_lq >> hRecRto")
    tree.Draw("true_lq >> hGenRto")

    ut.line_h1(hLog10Q2gen, rt.kBlue)
    hLog10Q2gen.SetLineWidth(3)

    hLog10Q2rec.SetLineColor(rt.kRed)
    hLog10Q2rec.SetMarkerColor(rt.kRed)

    pdiv = 0.4
    pad1 = TPad("p1", "p1", 0., pdiv, 1., 1.) # upper
    pad2 = TPad("p2", "p2", 0., 0., 1., pdiv) # lower
    pad1.Draw()
    pad2.Draw()

    #upper plot

    pad1.cd()

    #frame1 = gPad.DrawFrame(lqmin, 1e-3, lqmax, 8e3)
    frame1 = gPad.DrawFrame(lqmin, 1e-3, lqmax, 6e3)
    #frame1 = gPad.DrawFrame(lqmin, 1e-3, lqmax, 1.4e3)
    siz = 0.045
    ut.set_H1_text_size(frame1, siz)
    frame1.Draw()

    frame1.SetYTitle("Events / {0:.3f}".format(lqbin))
    frame1.SetTitleOffset(1.4, "Y")

    hLog10Q2gen.Draw("same")
    hLog10Q2rec.Draw("e1same")

    lmg = 0.12
    rmg = 0.01

    ut.set_margin_lbtr(gPad, lmg, 0, 0.04, rmg)

    #leg = ut.prepare_leg(0.5, 0.75, 0.2, 0.15, siz)
    leg = ut.prepare_leg(0.2, 0.75, 0.2, 0.15, siz)
    leg.AddEntry(hLog10Q2gen, "Pythia6 generated events", "l")
    leg.AddEntry(hLog10Q2rec, "Reconstruction in low #it{Q}^{2} tagger", "lp")
    leg.Draw("same")

    ut.invert_col(rt.gPad)

    #lower plot

    pad2.cd()

    frame2 = gPad.DrawFrame(lqmin, 0.5, lqmax, 1.5-1e-5)
    siz2 = siz*(1.+(1.-pdiv))
    ut.set_H1_text_size(frame2, siz2)
    frame2.Draw()

    ut.put_yx_tit(frame2, "Reconstructed / generated", "log_{10}(Q^{2}) (GeV)", 0.85, 1.3)

    #line at one
    unity = TLine(lqmin, 1., lqmax, 1.)
    unity.SetLineColor(rt.kBlack)
    unity.SetLineWidth(1)
    unity.Draw()

    #ratio rec/gen
    hRto = hRecRto.Clone()
    hRto.Sumw2()
    hRto.Divide(hGenRto)

    for i in xrange(1, hRtoPlot.GetNbinsX()+1):

        if hRtoPlot.GetBinLowEdge(i) < lrmin: continue

        hRtoPlot.SetBinContent(i, hRto.GetBinContent(i))
        hRtoPlot.SetBinError(i, hRto.GetBinError(i))

    #hRto.Draw("same")
    hRtoPlot.Draw("same")

    ut.set_margin_lbtr(gPad, lmg, 0.22, 0, rmg)

    leg2 = ut.prepare_leg(0.12, 0.83, 0.2, 0.1, siz2)
    leg2.AddEntry(hRto, "Ratio rec / gen", "lp")
    leg2.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#log10_Q2_rto

#_____________________________________________________________________________
def lQ2_rec_gen():

    #reconstructed and generated log_10(Q^2)

    lqbin = 0.1
    lqmin = -9
    lqmax = 0

    hLQ2 = ut.prepare_TH2D("hLQ2", lqbin, lqmin, lqmax, lqbin, lqmin, lqmax)

    tree.Draw("rec_lq:true_lq >> hLQ2")

    can = ut.box_canvas()

    ytit = "Reconstructed log_{10}(Q^{2}) / "+"{0:.2f}".format(lqbin)
    xtit = "Generated log_{10}(Q^{2}) / "+"{0:.2f}".format(lqbin)
    ut.put_yx_tit(hLQ2, ytit, xtit, 1.4, 1.3)

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.11)

    hLQ2.Draw()

    hLQ2.SetMinimum(0.98)
    hLQ2.SetContour(300)

    gPad.SetGrid()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#lQ2_rec_gen

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

    #beep when done
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")















