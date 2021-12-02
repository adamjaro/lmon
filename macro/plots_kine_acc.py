#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem
from ROOT import TGraph, TMath

import plot_utils as ut

#_____________________________________________________________________________
def main():

    #tagger acceptance in electron kinematics

    #inp_qr = "../data/qr/lmon_qr_18x275_Qf_beff2_5Mevt.root"
    inp_qr = "taggers/hits_tag.root"
    inp_py = "../data/py/lmon_py_ep_18x275_Q2all_beff2_5Mevt.root"

    iplot = 18
    funclist = []
    funclist.append( acc_pT_s1 ) # 0
    funclist.append( acc_pT_s2 ) # 1
    funclist.append( acc_theta_s1 ) # 2
    funclist.append( acc_theta_s2 ) # 3
    funclist.append( acc_phi_s1 ) # 4
    funclist.append( acc_phi_s2 ) # 5
    funclist.append( acc_en_s1 ) # 6
    funclist.append( acc_en_s2 ) # 7
    funclist.append( acc_eta_s1 ) # 8
    funclist.append( acc_eta_s2 ) # 9
    funclist.append( acc_lQ2_s1 ) # 10
    funclist.append( acc_lQ2_s2 ) # 11

    funclist.append( el_pT ) # 12
    funclist.append( el_theta ) # 13
    funclist.append( el_eta ) # 14
    funclist.append( el_phi ) # 15
    funclist.append( el_E ) # 16
    funclist.append( evt_W ) # 17

    funclist.append( acc_en_theta ) # 18
    funclist.append( acc_phi_eta ) # 19
    funclist.append( acc_ly_lx ) # 20

    funclist.append( el_en_theta ) # 21
    funclist.append( el_phi_eta ) # 22

    funclist.append( el_theta_beff ) # 23
    funclist.append( el_eta_beff ) # 24
    funclist.append( el_phi_beff ) # 25

    funclist.append( export_acc ) # 26

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

    #ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, "Acceptance", "Electron #it{p}_{T} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.04)

    ut.set_graph(gPtQr, rt.kRed)
    gPtQr.Draw("psame")

    ut.set_graph(gPtPy, rt.kBlue)
    gPtPy.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.72, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 1", "")
    leg.AddEntry(gPtPy, "Pythia6", "l")
    leg.AddEntry(gPtQr, "QR", "l")
    leg.Draw("same")

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

    #ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, "Acceptance", "Electron #it{p}_{T} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.05)

    ut.set_graph(gPtQr, rt.kRed)
    gPtQr.Draw("psame")

    ut.set_graph(gPtPy, rt.kBlue)
    gPtPy.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.72, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 2", "")
    leg.AddEntry(gPtPy, "Pythia6", "l")
    leg.AddEntry(gPtQr, "QR", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_pT_s2

#_____________________________________________________________________________
def acc_theta_s1():

    tmin = TMath.Pi() - 2.1e-2
    tmax = TMath.Pi() + 0.5e-2

    amax = 0.08

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_theta", "lowQ2s1_IsHit")
    acc_qr.prec = 0.05
    acc_qr.bmin = 2e-4
    #acc_qr.nev = int(1e5)
    gThetaQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_theta", "lowQ2s1_IsHit")
    acc_py.prec = 0.05
    acc_py.bmin = 2e-4
    #acc_py.nev = int(1e4)
    gThetaPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(tmin, 0, tmax, amax)

    #ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, "Acceptance", "Electron polar angle #theta (rad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gThetaQr, rt.kRed)
    gThetaQr.Draw("psame")

    ut.set_graph(gThetaPy, rt.kBlue)
    gThetaPy.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 1", "")
    leg.AddEntry(gThetaPy, "Pythia6", "l")
    leg.AddEntry(gThetaQr, "QR", "l")
    leg.Draw("same")

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
    #acc_qr.nev = int(1e5)
    gThetaQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_theta", "lowQ2s2_IsHit")
    acc_py.prec = 0.03
    acc_py.bmin = 2e-4
    #acc_py.nev = int(1e5)
    gThetaPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(tmin, 0, tmax, amax)

    #ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, "Acceptance", "Electron polar angle #theta (rad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gThetaQr, rt.kRed)
    gThetaQr.Draw("psame")

    ut.set_graph(gThetaPy, rt.kBlue)
    gThetaPy.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 2", "")
    leg.AddEntry(gThetaPy, "Pythia6", "l")
    leg.AddEntry(gThetaQr, "QR", "l")
    leg.Draw("same")

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
    #acc_qr.nev = int(1e5)
    gPhiQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_phi", "lowQ2s1_IsHit")
    acc_py.prec = 0.02
    #acc_py.bmin = 2e-4
    #acc_py.nev = int(1e4)
    gPhiPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(pmin, 0, pmax, amax)

    #ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, "Acceptance", "Electron azimuthal angle #phi (rad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gPhiQr, rt.kRed)
    gPhiQr.Draw("psame")

    ut.set_graph(gPhiPy, rt.kBlue)
    gPhiPy.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.72, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 1", "")
    leg.AddEntry(gPhiPy, "Pythia6", "l")
    leg.AddEntry(gPhiQr, "QR", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
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
    #acc_qr.nev = int(1e5)
    gPhiQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_phi", "lowQ2s2_IsHit")
    acc_py.prec = 0.01
    #acc_py.bmin = 2e-4
    #acc_py.nev = int(1e4)
    gPhiPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(pmin, 0, pmax, amax)

    #ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, "Acceptance", "Electron azimuthal angle #phi (rad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gPhiQr, rt.kRed)
    gPhiQr.Draw("psame")

    ut.set_graph(gPhiPy, rt.kBlue)
    gPhiPy.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.72, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 2", "")
    leg.AddEntry(gPhiPy, "Pythia6", "l")
    leg.AddEntry(gPhiQr, "QR", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
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
    #acc_qr.nev = int(1e5)
    gEnQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_E", "lowQ2s1_IsHit")
    acc_py.prec = 0.05
    acc_py.bmin = 0.1
    #acc_py.nev = int(1e5)
    gEnPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(emin, 0, emax, amax)

    #ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, "Acceptance", "Electron energy #it{E} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gEnQr, rt.kRed)
    gEnQr.Draw("psame")

    ut.set_graph(gEnPy, rt.kBlue)
    gEnPy.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 1", "")
    leg.AddEntry(gEnPy, "Pythia6", "l")
    leg.AddEntry(gEnQr, "QR", "l")
    leg.Draw("same")

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
    #acc_qr.nev = int(1e5)
    gEnQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_E", "lowQ2s2_IsHit")
    acc_py.prec = 0.05
    acc_py.bmin = 0.1
    #acc_py.nev = int(1e4)
    gEnPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(emin, 0, emax, amax)

    #ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, "Acceptance", "Electron energy #it{E} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gEnQr, rt.kRed)
    gEnQr.Draw("psame")

    ut.set_graph(gEnPy, rt.kBlue)
    gEnPy.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 2", "")
    leg.AddEntry(gEnPy, "Pythia6", "l")
    leg.AddEntry(gEnQr, "QR", "l")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en_s2

#_____________________________________________________________________________
def acc_eta_s1():

    #Tagger 1 pseudorapidity

    emin = -17
    emax = -3

    amax = 0.1

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_theta", "lowQ2s1_IsHit")
    acc_qr.modif = 0 # eta from theta
    acc_qr.prec = 0.05
    acc_qr.bmin = 0.1
    #acc_qr.nev = int(1e5)
    gEtaQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_theta", "lowQ2s1_IsHit")
    acc_py.modif = 0
    acc_py.prec = 0.05
    acc_py.bmin = 0.1
    #acc_py.nev = int(1e5)
    gEtaPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(emin, 0, emax, amax)

    #ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, "Acceptance", "Electron pseudorapidity #eta", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gEtaQr, rt.kRed)
    gEtaQr.Draw("psame")

    ut.set_graph(gEtaPy, rt.kBlue)
    gEtaPy.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 1", "")
    leg.AddEntry(gEtaPy, "Pythia6", "l")
    leg.AddEntry(gEtaQr, "QR", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_eta_s1

#_____________________________________________________________________________
def acc_eta_s2():

    #Tagger 2 pseudorapidity

    emin = -17
    emax = -3

    amax = 0.3

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_el_theta", "lowQ2s2_IsHit")
    acc_qr.modif = 0 # eta from theta
    acc_qr.prec = 0.01
    acc_qr.bmin = 0.1
    #acc_qr.nev = int(1e5)
    gEtaQr = acc_qr.get()

    #gprint(gPtQr)

    acc_py = rt.acc_Q2_kine(tree_py, "true_el_theta", "lowQ2s2_IsHit")
    acc_py.modif = 0
    acc_py.prec = 0.01
    acc_py.bmin = 0.1
    #acc_py.nev = int(1e5)
    gEtaPy = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(emin, 0, emax, amax)

    #ytit = "Acceptance / {0:.1f} %".format(acc_qr.prec*100)
    ut.put_yx_tit(frame, "Acceptance", "Electron pseudorapidity #eta", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(gEtaQr, rt.kRed)
    gEtaQr.Draw("psame")

    ut.set_graph(gEtaPy, rt.kBlue)
    gEtaPy.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 2", "")
    leg.AddEntry(gEtaPy, "Pythia6", "l")
    leg.AddEntry(gEtaQr, "QR", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_eta_s2

#_____________________________________________________________________________
def acc_lQ2_s1():

    #Tagger 1 log_10(Q^2)

    lQ2min = -10
    lQ2max = 0

    amax = 0.1

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_Q2", "lowQ2s1_IsHit")
    acc_qr.modif = 1 # log_10(Q^2) from Q2
    acc_qr.prec = 0.05
    acc_qr.bmin = 0.1
    #acc_qr.nev = int(1e5)
    glQ2Qr = acc_qr.get()

    acc_py = rt.acc_Q2_kine(tree_py, "true_Q2", "lowQ2s1_IsHit")
    acc_py.modif = 1
    acc_py.prec = 0.05
    acc_py.bmin = 0.1
    #acc_py.nev = int(1e5)
    glQ2Py = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(lQ2min, 0, lQ2max, amax)
    ut.put_yx_tit(frame, "Acceptance", "Virtuality log_{10}(#it{Q}^{2}) (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(glQ2Qr, rt.kRed)
    glQ2Qr.Draw("psame")

    ut.set_graph(glQ2Py, rt.kBlue)
    glQ2Py.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 1", "")
    leg.AddEntry(glQ2Py, "Pythia6", "l")
    leg.AddEntry(glQ2Qr, "QR", "l")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_lQ2_s1

#_____________________________________________________________________________
def acc_lQ2_s2():

    #Tagger 2 log_10(Q^2)

    lQ2min = -10
    lQ2max = 0

    amax = 0.3

    acc_qr = rt.acc_Q2_kine(tree_qr, "true_Q2", "lowQ2s2_IsHit")
    acc_qr.modif = 1 # log_10(Q^2) from Q2
    acc_qr.prec = 0.05
    acc_qr.bmin = 0.1
    #acc_qr.nev = int(1e5)
    glQ2Qr = acc_qr.get()

    acc_py = rt.acc_Q2_kine(tree_py, "true_Q2", "lowQ2s2_IsHit")
    acc_py.modif = 1
    acc_py.prec = 0.05
    acc_py.bmin = 0.1
    #acc_py.nev = int(1e5)
    glQ2Py = acc_py.get()

    can = ut.box_canvas()

    frame = gPad.DrawFrame(lQ2min, 0, lQ2max, amax)
    ut.put_yx_tit(frame, "Acceptance", "Virtuality log_{10}(#it{Q}^{2}) (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    ut.set_graph(glQ2Qr, rt.kRed)
    glQ2Qr.Draw("psame")

    ut.set_graph(glQ2Py, rt.kBlue)
    glQ2Py.Draw("psame")

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.78, 0.24, 0.16, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(None, "Tagger 2", "")
    leg.AddEntry(glQ2Py, "Pythia6", "l")
    leg.AddEntry(glQ2Qr, "QR", "l")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_lQ2_s2

#_____________________________________________________________________________
def el_pT():

    #electron pT

    xbin = 0.3
    xmin = 0
    xmax = 80

    can = ut.box_canvas()

    hPy = ut.prepare_TH1D("hPy", xbin, xmin, xmax)
    hQr = ut.prepare_TH1D("hQr", xbin, xmin, xmax)

    tree_py.Draw("true_el_pT >> hPy")
    tree_qr.Draw("true_el_pT >> hQr")

    ut.line_h1(hPy, rt.kBlue)
    ut.line_h1(hQr, rt.kRed)

    vmax = hPy.GetMaximum() + 0.4*hPy.GetMaximum()
    frame = gPad.DrawFrame(xmin, 0.5, xmax, vmax)

    ut.put_yx_tit(frame, "Counts", "Electron #it{p}_{T} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    gPad.SetGrid()
    gPad.SetLogy()

    hQr.Draw("same")
    hPy.Draw("same")

    leg = ut.prepare_leg(0.72, 0.8, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hPy, "Pythia6", "l")
    leg.AddEntry(hQr, "QR", "l")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_pT

#_____________________________________________________________________________
def el_theta():

    #electron polar angle theta

    xbin = 5e-2
    xmin = 0
    xmax = TMath.Pi() + 1e-2

    can = ut.box_canvas()

    hPy = ut.prepare_TH1D("hPy", xbin, xmin, xmax)
    hQr = ut.prepare_TH1D("hQr", xbin, xmin, xmax)

    tree_py.Draw("true_el_theta >> hPy")
    tree_qr.Draw("true_el_theta >> hQr")

    ut.line_h1(hPy, rt.kBlue)
    ut.line_h1(hQr, rt.kRed)

    vmax = hPy.GetMaximum() + 0.4*hPy.GetMaximum()
    frame = gPad.DrawFrame(xmin, 0.5, xmax, vmax)

    ut.put_yx_tit(frame, "Counts", "Electron #theta (rad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    gPad.SetGrid()
    gPad.SetLogy()

    hQr.Draw("same")
    hPy.Draw("same")

    leg = ut.prepare_leg(0.72, 0.8, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hPy, "Pythia6", "l")
    leg.AddEntry(hQr, "QR", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_theta

#_____________________________________________________________________________
def el_eta():

    #electron pseudorapidity eta

    xbin = 0.1
    xmin = -20
    xmax = 10

    can = ut.box_canvas()

    hPy = ut.prepare_TH1D("hPy", xbin, xmin, xmax)
    hQr = ut.prepare_TH1D("hQr", xbin, xmin, xmax)

    form = "-TMath::Log(TMath::Tan(true_el_theta/2.))"
    tree_py.Draw(form+" >> hPy")
    tree_qr.Draw(form+" >> hQr")

    ut.line_h1(hPy, rt.kBlue)
    ut.line_h1(hQr, rt.kRed)

    vmax = hPy.GetMaximum() + 0.1*hPy.GetMaximum()
    frame = gPad.DrawFrame(xmin, 0.5, xmax, vmax)

    ut.put_yx_tit(frame, "Counts", "Electron #eta", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.05, 0.02)

    gPad.SetGrid()
    #gPad.SetLogy()

    hQr.Draw("same")
    hPy.Draw("same")

    leg = ut.prepare_leg(0.72, 0.8, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hPy, "Pythia6", "l")
    leg.AddEntry(hQr, "QR", "l")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_eta

#_____________________________________________________________________________
def el_phi():

    #electron azimuthal angle phi

    xbin = 3e-2
    xmin = -TMath.Pi() - 0.3
    xmax = TMath.Pi() + 0.3

    can = ut.box_canvas()

    hPy = ut.prepare_TH1D("hPy", xbin, xmin, xmax)
    hQr = ut.prepare_TH1D("hQr", xbin, xmin, xmax)

    tree_py.Draw("true_el_phi >> hPy")
    tree_qr.Draw("true_el_phi >> hQr")

    ut.line_h1(hPy, rt.kBlue)
    ut.line_h1(hQr, rt.kRed)

    vmax = hPy.GetMaximum() + 0.4*hPy.GetMaximum()
    frame = gPad.DrawFrame(xmin, 0.5, xmax, vmax)

    ut.put_yx_tit(frame, "Counts", "Electron #phi (rad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.05, 0.02)

    gPad.SetGrid()
    #gPad.SetLogy()

    hQr.Draw("same")
    hPy.Draw("same")

    leg = ut.prepare_leg(0.72, 0.8, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hPy, "Pythia6", "l")
    leg.AddEntry(hQr, "QR", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_phi

#_____________________________________________________________________________
def el_E():

    #electron energy E

    xbin = 0.2
    xmin = 0
    xmax = 50

    can = ut.box_canvas()

    hPy = ut.prepare_TH1D("hPy", xbin, xmin, xmax)
    hQr = ut.prepare_TH1D("hQr", xbin, xmin, xmax)

    tree_py.Draw("true_el_E >> hPy")
    tree_qr.Draw("true_el_E >> hQr")

    ut.line_h1(hPy, rt.kBlue)
    ut.line_h1(hQr, rt.kRed)

    vmax = hPy.GetMaximum() + 0.5*hPy.GetMaximum()
    frame = gPad.DrawFrame(xmin, 0.5, xmax, vmax)

    ut.put_yx_tit(frame, "Counts", "Electron energy #it{E} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    gPad.SetGrid()
    gPad.SetLogy()

    hQr.Draw("same")
    hPy.Draw("same")

    leg = ut.prepare_leg(0.72, 0.8, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hPy, "Pythia6", "l")
    leg.AddEntry(hQr, "QR", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_E

#_____________________________________________________________________________
def evt_W():

    #event photon-proton CM energy W

    xbin = 0.1
    xmin = 0
    xmax = 155

    can = ut.box_canvas()

    hPy = ut.prepare_TH1D("hPy", xbin, xmin, xmax)
    hQr = ut.prepare_TH1D("hQr", xbin, xmin, xmax)

    tree_py.Draw("TMath::Sqrt(true_W2) >> hPy")
    tree_qr.Draw("TMath::Sqrt(true_W2) >> hQr")

    ut.line_h1(hPy, rt.kBlue)
    ut.line_h1(hQr, rt.kRed)

    vmax = hQr.GetMaximum()
    vmax += 0.4*vmax
    frame = gPad.DrawFrame(xmin, 100, xmax, vmax)

    ut.put_yx_tit(frame, "Counts", "Photon-proton CM energy #it{W} (GeV)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    gPad.SetGrid()
    gPad.SetLogy()

    hQr.Draw("same")
    hPy.Draw("same")

    leg = ut.prepare_leg(0.72, 0.8, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hPy, "Pythia6", "l")
    leg.AddEntry(hQr, "QR", "l")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#evt_W

#_____________________________________________________________________________
def acc_en_theta(qrpy=0, tag=0, out=False):

    #Tagger acceptance in energy and theta

    #bins in theta
    tbin = 4e-4
    tmin = TMath.Pi() - 2.1e-2
    tmax = TMath.Pi() + 0.5e-2

    #bins in energy
    ebin = 0.3
    emin = 0
    emax = 21

    if qrpy == 0:
        tree = tree_qr
        lab_data = "QR"
    else:
        tree = tree_py
        lab_data = "Pythia6"

    if tag == 0:
        #sel = "lowQ2s1_IsHit==1"
        sel = "s1_IsHit==1"
        lab_sel = "Tagger 1"
    else:
        #sel = "lowQ2s2_IsHit==1"
        sel = "s2_IsHit==1"
        lab_sel = "Tagger 2"

    #name for output
    tnam = ["accTagger1_E_theta", "accTagger2_E_theta"]
    dnam = ["_QR", "_Pythia6"]
    nametit = tnam[tag] + dnam[qrpy]
    print(nametit)

    can = ut.box_canvas()
    if out == True:
        can.SetName(nametit)

    hEnThetaTag = ut.prepare_TH2D("hEnThetaTag", tbin, tmin, tmax, ebin, emin, emax)
    hEnThetaAll = ut.prepare_TH2D("hEnThetaAll", tbin, tmin, tmax, ebin, emin, emax)

    form = "true_el_E:true_el_theta"
    tree.Draw(form+" >> hEnThetaTag", sel)
    tree.Draw(form+" >> hEnThetaAll")

    hEnThetaTag.Divide(hEnThetaAll)

    ytit = "Electron energy #it{E} (GeV)"
    xtit = "Electron polar angle #theta (rad)"
    ut.put_yx_tit(hEnThetaTag, ytit, xtit, 1.4, 1.3)

    hEnThetaTag.SetTitleOffset(1.5, "Z")
    hEnThetaTag.SetZTitle("Acceptance")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hEnThetaTag.SetMinimum(0)
    hEnThetaTag.SetMaximum(1)
    hEnThetaTag.SetContour(300)

    hEnThetaTag.Draw("colz")

    if out == True:
        hEnThetaTag.SetNameTitle(nametit, nametit)
        hEnThetaTag.Write()
        return

    leg = ut.prepare_leg(0.12, 0.2, 0.24, 0.12, 0.04) # x, y, dx, dy, tsiz
    leg.AddEntry("", lab_sel, "")
    leg.AddEntry("", lab_data, "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_en_theta

#_____________________________________________________________________________
def acc_phi_eta():

    #Tagger acceptance in phi and eta

    #bins in phi
    pbin = 3e-2
    pmin = -TMath.Pi() - 0.3
    pmax = TMath.Pi() + 0.3

    #bins in eta
    ebin = 0.1
    emin = -18
    emax = -3

    tree = tree_qr
    lab_data = "QR"
    #tree = tree_py
    #lab_data = "Pythia6"

    #sel = "lowQ2s1_IsHit==1"
    #lab_sel = "Tagger 1"
    sel = "lowQ2s2_IsHit==1"
    lab_sel = "Tagger 2"

    can = ut.box_canvas()

    hPhiEtaTag = ut.prepare_TH2D("hPhiEtaTag", ebin, emin, emax, pbin, pmin, pmax)
    hPhiEtaAll = ut.prepare_TH2D("hPhiEtaAll", ebin, emin, emax, pbin, pmin, pmax)

    form = "true_el_phi:(-TMath::Log(TMath::Tan(true_el_theta/2.)))" # y:x
    tree.Draw(form+" >> hPhiEtaTag", sel)
    tree.Draw(form+" >> hPhiEtaAll")

    hPhiEtaTag.Divide(hPhiEtaAll)

    ytit = "Electron azimuthal angle #phi (rad)"
    xtit = "Electron pseudorapidity #eta"
    ut.put_yx_tit(hPhiEtaTag, ytit, xtit, 1.1, 1.3)

    hPhiEtaTag.SetTitleOffset(1.5, "Z")
    hPhiEtaTag.SetZTitle("Acceptance")

    ut.set_margin_lbtr(gPad, 0.08, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hPhiEtaTag.SetMinimum(0)
    hPhiEtaTag.SetMaximum(0.3)
    hPhiEtaTag.SetContour(300)

    hPhiEtaTag.Draw("colz")

    leg = ut.prepare_leg(0.05, 0.2, 0.24, 0.12, 0.04) # x, y, dx, dy, tsiz
    leg.AddEntry(None, lab_sel, "")
    leg.AddEntry(None, lab_data, "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_phi_eta

#_____________________________________________________________________________
def acc_ly_lx():

    #Tagger acceptance in log_10(y) and log_10(x)

    #bins in log_10(y)
    ybin = 0.04
    ymin = -4
    #ymin = -1
    ymax = 0

    #bins in log_10(x)
    xbin = 0.05 # 2e-2
    xmin = -12
    xmax = 0

    tree = tree_qr
    lab_data = "QR"
    #tree = tree_py
    #lab_data = "Pythia6"

    #sel = "lowQ2s1_IsHit==1"
    #lab_sel = "Tagger 1"
    sel = "lowQ2s2_IsHit==1"
    lab_sel = "Tagger 2"

    can = ut.box_canvas()

    hYXTag = ut.prepare_TH2D("hYXTag", xbin, xmin, xmax, ybin, ymin, ymax)
    hYXAll = ut.prepare_TH2D("hYXAll", xbin, xmin, xmax, ybin, ymin, ymax)

    form = "TMath::Log10(true_y):TMath::Log10(true_x)" # y:x
    tree.Draw(form+" >> hYXTag", sel)
    tree.Draw(form+" >> hYXAll")

    hYXTag.Divide(hYXAll)

    ytit = "log_{10}(#it{y})"
    xtit = "log_{10}(#it{x})"
    ut.put_yx_tit(hYXTag, ytit, xtit, 1.4, 1.3)

    hYXTag.SetTitleOffset(1.5, "Z")
    hYXTag.SetZTitle("Acceptance")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.15)

    #gPad.SetLogz()

    gPad.SetGrid()

    hYXTag.SetMinimum(0)
    hYXTag.SetMaximum(1)
    hYXTag.SetContour(300)

    hYXTag.Draw("colz")

    leg = ut.prepare_leg(0.6, 0.85, 0.24, 0.12, 0.04) # x, y, dx, dy, tsiz
    leg.AddEntry(None, lab_sel, "")
    leg.AddEntry(None, lab_data, "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_ly_lx

#_____________________________________________________________________________
def el_en_theta():

    #electrons energy and theta

    #bins in theta
    tbin = 5e-2
    tmin = 0
    tmax = TMath.Pi() + 1e-2

    #bins in energy
    ebin = 0.6
    emin = 0
    emax = 50

    tree = tree_qr
    lab_data = "QR"
    #tree = tree_py
    #lab_data = "Pythia6"

    can = ut.box_canvas()

    hEnThetaAll = ut.prepare_TH2D("hEnThetaAll", tbin, tmin, tmax, ebin, emin, emax)

    form = "true_el_E:true_el_theta"
    tree.Draw(form+" >> hEnThetaAll")

    ytit = "Electron energy #it{E} (GeV)"
    xtit = "Electron polar angle #theta (rad)"
    ut.put_yx_tit(hEnThetaAll, ytit, xtit, 1.4, 1.3)

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.015, 0.12)

    gPad.SetLogz()

    gPad.SetGrid()

    hEnThetaAll.SetMinimum(0.98)
    hEnThetaAll.SetContour(300)

    hEnThetaAll.Draw("colz")

    leg = ut.prepare_leg(0.6, 0.82, 0.24, 0.12, 0.04) # x, y, dx, dy, tsiz
    leg.AddEntry(None, lab_data, "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_en_theta

#_____________________________________________________________________________
def el_phi_eta():

    #electron phi and eta

    #bins in phi
    pbin = 6e-2
    pmin = -TMath.Pi() - 0.3
    pmax = TMath.Pi() + 0.8

    #bins in eta
    ebin = 0.2
    emin = -18
    emax = 5

    tree = tree_qr
    lab_data = "QR"
    #tree = tree_py
    #lab_data = "Pythia6"

    can = ut.box_canvas()

    hPhiEta = ut.prepare_TH2D("hPhiEta", ebin, emin, emax, pbin, pmin, pmax)

    form = "true_el_phi:(-TMath::Log(TMath::Tan(true_el_theta/2.)))" # y:x
    tree.Draw(form+" >> hPhiEta")

    ytit = "Electron azimuthal angle #phi (rad)"
    xtit = "Electron pseudorapidity #eta"
    ut.put_yx_tit(hPhiEta, ytit, xtit, 1.1, 1.3)

    ut.set_margin_lbtr(gPad, 0.08, 0.1, 0.015, 0.14)

    #gPad.SetLogz()

    gPad.SetGrid()

    hPhiEta.SetMinimum(0.98)
    hPhiEta.SetContour(300)

    hPhiEta.Draw("colz")

    leg = ut.prepare_leg(0.6, 0.9, 0.24, 0.06, 0.04) # x, y, dx, dy, tsiz
    leg.AddEntry(None, lab_data, "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_phi_eta

#_____________________________________________________________________________
def el_theta_beff():

    #electron polar angle theta and effect of angular divergence

    xbin = 5e-5
    #xmin = TMath.Pi() - 2.2e-2
    xmin = 3.13
    xmax = TMath.Pi() + 0.2e-2

    qrpy = 0
    if qrpy == 0:
        tree = tree_qr
        lab_data = "QR"
        col = rt.kBlue
    else:
        tree = tree_py
        lab_data = "Pythia6"
        col = rt.kRed

    can = ut.box_canvas()

    hT = ut.prepare_TH1D("hT", xbin, xmin, xmax)
    hB = ut.prepare_TH1D("hB", xbin, xmin, xmax)

    tree.Draw("true_el_theta >> hT")
    tree.Draw("el_theta >> hB")

    ut.line_h1(hT, col)
    ut.line_h1(hB, rt.kViolet)

    vmax = hT.GetMaximum() + 0.4*hT.GetMaximum()
    frame = gPad.DrawFrame(xmin, 1e3, xmax, vmax)

    ut.put_yx_tit(frame, "Counts", "Electron #theta (rad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.03, 0.02)

    gPad.SetGrid()
    gPad.SetLogy()

    hB.Draw("same")
    hT.Draw("same")

    leg = ut.prepare_leg(0.14, 0.8, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hT, lab_data+", no divergence", "l")
    leg.AddEntry(hB, "Divergence included", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_theta_beff

#_____________________________________________________________________________
def el_eta_beff():

    #electron pseudorapidity eta and angular divergence

    xbin = 0.1
    xmin = -20
    xmax = 10

    qrpy = 0
    if qrpy == 0:
        tree = tree_qr
        lab_data = "QR"
        col = rt.kBlue
    else:
        tree = tree_py
        lab_data = "Pythia6"
        col = rt.kRed

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", xbin, xmin, xmax)
    hB = ut.prepare_TH1D("hB", xbin, xmin, xmax)

    form = "-TMath::Log(TMath::Tan(true_el_theta/2.))"
    form2 = "-TMath::Log(TMath::Tan(el_theta/2.))"
    tree.Draw(form+" >> hE")
    tree.Draw(form2+" >> hB")

    ut.line_h1(hE, col)
    ut.line_h1(hB, rt.kViolet)

    vmax = hB.GetMaximum() + 0.1*hB.GetMaximum()
    frame = gPad.DrawFrame(xmin, 0.5, xmax, vmax)

    ut.put_yx_tit(frame, "Counts", "Electron #eta", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.05, 0.02)

    gPad.SetGrid()
    #gPad.SetLogy()

    hB.Draw("same")
    hE.Draw("same")

    leg = ut.prepare_leg(0.56, 0.8, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hE, lab_data+", no divergence", "l")
    leg.AddEntry(hB, "Divergence included", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_eta_beff

#_____________________________________________________________________________
def el_phi_beff():

    #electron azimuthal angle phi

    xbin = 3e-2
    xmin = -TMath.Pi() - 0.3
    xmax = TMath.Pi() + 0.3

    qrpy = 0
    if qrpy == 0:
        tree = tree_qr
        lab_data = "QR"
        col = rt.kBlue
    else:
        tree = tree_py
        lab_data = "Pythia6"
        col = rt.kRed

    can = ut.box_canvas()

    hP = ut.prepare_TH1D("hP", xbin, xmin, xmax)
    hB = ut.prepare_TH1D("hB", xbin, xmin, xmax)

    tree.Draw("true_el_phi >> hP")
    tree.Draw("el_phi >> hB")

    ut.line_h1(hP, col)
    ut.line_h1(hB, rt.kViolet)

    vmax = hP.GetMaximum() + 0.5*hP.GetMaximum()
    frame = gPad.DrawFrame(xmin, 0.5, xmax, vmax)

    ut.put_yx_tit(frame, "Counts", "Electron #phi (rad)", 1.6, 1.3)

    frame.Draw()

    ut.set_margin_lbtr(gPad, 0.11, 0.1, 0.05, 0.02)

    gPad.SetGrid()
    #gPad.SetLogy()

    hB.Draw("same")
    hP.Draw("same")

    leg = ut.prepare_leg(0.55, 0.8, 0.24, 0.12, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hP, lab_data+", no divergence", "l")
    leg.AddEntry(hB, "Divergence included", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#el_phi_beff

#_____________________________________________________________________________
def export_acc():

    #export acceptance data to output file
    #
    # qrpy: 0 - QR, 1 - Pythia6
    # tag: 0 - Tagger 1, 1 - Tagger 2

    out = TFile.Open("accTagger_Fig21_22_20201027.root", "recreate")

    acc_en_theta(qrpy=1, tag=0, out=True)
    acc_en_theta(qrpy=0, tag=0, out=True)

    acc_en_theta(qrpy=1, tag=1, out=True)
    acc_en_theta(qrpy=0, tag=1, out=True)

    out.Close()

#export_acc

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
        print(fmt)
        gtot += yp*(g.GetErrorXlow(ip) + g.GetErrorXhigh(ip))

    print("gtot:", gtot)

#_____________________________________________________________________________
def get_tree(infile):

    #get tree from input file

    inp = TFile.Open(infile)
    #return inp.Get("DetectorTree"), inp
    return inp.Get("event"), inp

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

