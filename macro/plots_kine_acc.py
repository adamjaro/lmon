#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath

import plot_utils as ut

#_____________________________________________________________________________
def main():

    #tagger acceptance in electron kinematics

    inp_qr = "../data/qr/lmon_qr_18x275_Qe_beff2_5Mevt.root"
    inp_py = "../data/py/lmon_py_ep_18x275_Q2all_beff2_5Mevt.root"

    iplot = 7
    funclist = []
    funclist.append( acc_pT_s1 ) # 0
    funclist.append( acc_pT_s2 ) # 1
    funclist.append( acc_theta_s1 ) # 2
    funclist.append( acc_theta_s2 ) # 3
    funclist.append( acc_phi_s1 ) # 4
    funclist.append( acc_phi_s2 ) # 5
    funclist.append( acc_en_s1 ) # 6
    funclist.append( acc_en_s2 ) # 7

    global tree_qr; global tree_py
    tree_qr, infile_qr = get_tree(inp_qr)
    tree_py, infile_py = get_tree(inp_py)

    funclist[iplot]()

#main

#_____________________________________________________________________________
def acc_pT_s1():

    ptmin = 0
    ptmax = 0.18
    #ptmax = 0.25

    amax = 0.08
    #amax = 0.25

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_pT", "lowQ2s1_IsHit")
    acc_qr.prec = 0.05
    acc_qr.bmin = 0.003
    #acc_qr.nev = int(1e5)
    gPtQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_pT", "lowQ2s1_IsHit")
    acc_py.prec = 0.05
    acc_py.bmin = 0.003
    #acc_py.nev = int(1e4)
    gPtPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(ptmin, 0, ptmax, amax)

    ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, ytit, "#it{p}_{T} (GeV)", 1.6, 1.2)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gPtQr, rt.kRed)
    gPtQr.Draw("psame")

    ut.set_graph(gPtPy, rt.kBlue)
    gPtPy.Draw("psame")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_pT_s1

#_____________________________________________________________________________
def acc_pT_s2():

    ptmin = 0
    ptmax = 0.25

    amax = 0.25

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_pT", "lowQ2s2_IsHit")
    acc_qr.prec = 0.05
    acc_qr.bmin = 0.003
    #acc_qr.nev = int(1e5)
    gPtQr = acc_qr.get()

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_pT", "lowQ2s2_IsHit")
    acc_py.prec = 0.05
    acc_py.bmin = 0.003
    #acc_py.nev = int(1e4)
    gPtPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(ptmin, 0, ptmax, amax)

    ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, ytit, "#it{p}_{T} (GeV)", 1.6, 1.2)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.025)

    ut.set_graph(gPtQr, rt.kRed)
    gPtQr.Draw("psame")

    ut.set_graph(gPtPy, rt.kBlue)
    gPtPy.Draw("psame")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_pT_s1

#_____________________________________________________________________________
def acc_theta_s1():

    tmin = TMath.Pi() - 2.1e-2
    tmax = TMath.Pi() + 0.5e-2

    amax = 0.08

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_theta", "lowQ2s1_IsHit")
    acc_qr.prec = 0.05
    acc_qr.bmin = 2e-4
    #acc_qr.nev = int(1e4)
    gThetaQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_theta", "lowQ2s1_IsHit")
    acc_py.prec = 0.05
    acc_py.bmin = 2e-4
    #acc_py.nev = int(1e4)
    gThetaPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(tmin, 0, tmax, amax)

    ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, ytit, "#theta (GeV)", 1.6, 1.2)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gThetaQr, rt.kRed)
    gThetaQr.Draw("psame")

    ut.set_graph(gThetaPy, rt.kBlue)
    gThetaPy.Draw("psame")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_theta_s1

#_____________________________________________________________________________
def acc_theta_s2():

    #Tagger 2 theta

    tmin = TMath.Pi() - 2.1e-2
    tmax = TMath.Pi() + 0.5e-2

    amax = 0.3

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_theta", "lowQ2s2_IsHit")
    acc_qr.prec = 0.03
    acc_qr.bmin = 2e-4
    #acc_qr.nev = int(1e4)
    gThetaQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_theta", "lowQ2s2_IsHit")
    acc_py.prec = 0.03
    acc_py.bmin = 2e-4
    #acc_py.nev = int(1e4)
    gThetaPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(tmin, 0, tmax, amax)

    ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, ytit, "#theta (GeV)", 1.6, 1.2)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gThetaQr, rt.kRed)
    gThetaQr.Draw("psame")

    ut.set_graph(gThetaPy, rt.kBlue)
    gThetaPy.Draw("psame")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_theta_s2

#_____________________________________________________________________________
def acc_phi_s1():

    #Tagger 1 phi

    pmin = -TMath.Pi() - 0.3
    pmax = TMath.Pi() + 0.3

    amax = 0.08

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_phi", "lowQ2s1_IsHit")
    acc_qr.prec = 0.02
    #acc_qr.bmin = 2e-4
    #acc_qr.nev = int(1e4)
    gPhiQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_phi", "lowQ2s1_IsHit")
    acc_py.prec = 0.02
    #acc_py.bmin = 2e-4
    #acc_py.nev = int(1e4)
    gPhiPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(pmin, 0, pmax, amax)

    ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, ytit, "#phi (GeV)", 1.6, 1.2)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gPhiQr, rt.kRed)
    gPhiQr.Draw("psame")

    ut.set_graph(gPhiPy, rt.kBlue)
    gPhiPy.Draw("psame")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_phi_s1

#_____________________________________________________________________________
def acc_phi_s2():

    #Tagger 2 phi

    pmin = -TMath.Pi() - 0.3
    pmax = TMath.Pi() + 0.3

    amax = 0.3

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_phi", "lowQ2s2_IsHit")
    acc_qr.prec = 0.01
    #acc_qr.bmin = 2e-4
    #acc_qr.nev = int(1e4)
    gPhiQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_phi", "lowQ2s2_IsHit")
    acc_py.prec = 0.01
    #acc_py.bmin = 2e-4
    #acc_py.nev = int(1e4)
    gPhiPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(pmin, 0, pmax, amax)

    ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, ytit, "#phi (GeV)", 1.6, 1.2)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gPhiQr, rt.kRed)
    gPhiQr.Draw("psame")

    ut.set_graph(gPhiPy, rt.kBlue)
    gPhiPy.Draw("psame")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_phi_s2

#_____________________________________________________________________________
def acc_en_s1():

    #Tagger 1 energy

    emin = 0
    emax = 15

    amax = 1

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_E", "lowQ2s1_IsHit")
    acc_qr.prec = 0.05
    acc_qr.bmin = 0.1
    #acc_qr.nev = int(1e4)
    gEnQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_E", "lowQ2s1_IsHit")
    acc_py.prec = 0.05
    acc_py.bmin = 0.1
    #acc_py.nev = int(1e4)
    gEnPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(emin, 0, emax, amax)

    ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, ytit, "#it{E} (GeV)", 1.6, 1.2)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gEnQr, rt.kRed)
    gEnQr.Draw("psame")

    ut.set_graph(gEnPy, rt.kBlue)
    gEnPy.Draw("psame")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en_s1

#_____________________________________________________________________________
def acc_en_s2():

    #Tagger 2 energy

    emin = 0
    emax = 20

    amax = 1

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_E", "lowQ2s2_IsHit")
    acc_qr.prec = 0.05
    acc_qr.bmin = 0.1
    #acc_qr.nev = int(1e4)
    gEnQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_E", "lowQ2s2_IsHit")
    acc_py.prec = 0.05
    acc_py.bmin = 0.1
    #acc_py.nev = int(1e4)
    gEnPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(emin, 0, emax, amax)

    ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, ytit, "#it{E} (GeV)", 1.6, 1.2)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gEnQr, rt.kRed)
    gEnQr.Draw("psame")

    ut.set_graph(gEnPy, rt.kBlue)
    gEnPy.Draw("psame")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en_s2



#_____________________________________________________________________________
def gprint(g):

    #graph print

    gtot = 0.
    for ip in xrange(g.GetN()):

        xp = rt.Double(0)
        yp = rt.Double(0)
        g.GetPoint(ip, xp, yp)

        fmt = "{0:4d}{1:8.5f}".format(ip, xp)
        fmt += "{0:8.5f}".format(g.GetErrorX(ip))
        fmt += "{0:8.5f}{1:8.5f}".format(g.GetErrorXlow(ip), g.GetErrorXhigh(ip))
        fmt += "{0:8.5f}".format(yp)
        print fmt
        gtot += yp*(g.GetErrorXlow(ip) + g.GetErrorXhigh(ip))

    print "gtot:", gtot

#_____________________________________________________________________________
def get_tree(infile):

    #get tree from input file

    inp = TFile.Open(infile)
    return inp.Get("DetectorTree"), inp

#get_tree

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    gROOT.ProcessLine(".L acc_Q2_kine.h+")

    main()

    #beep when done
    gSystem.Exec("mplayer computerbeep_1.mp3 > /dev/null 2>&1")

