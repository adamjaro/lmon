#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TH3D

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    basedir = "/home/jaroslav/sim/lgen/data"

    #infile = "lgen_18x275_qr_Qd_beff2_10p2Mevt.root"
    #infile = "lgen_18x275_qr_Qd_beff2_5Mevt.root"
    infile = "lgen_18x275_qr_Qe_beff2_5Mevt.root"
    #infile = "lgen_10x100_qr_5Mevt.root"
    #infile = "lgen_5x41_qr_5Mevt.root"
    #infile = "lgen_py_18x275_Q2all_5Mevt.root"
    #infile = "lgen_py_5x41_Q2all_5Mevt.root"
    #infile = "lgen_py_10x100_Q2all_5Mevt.root"

    iplot = 23
    funclist = []
    funclist.append( gen_xy ) # 0
    funclist.append( gen_Q2 ) # 1
    funclist.append( gen_Log10_Q2 ) # 2
    funclist.append( gen_E ) # 3
    funclist.append( gen_theta ) # 4
    funclist.append( gen_Q2_theta ) # 5
    funclist.append( gen_Log10x_y ) # 6
    funclist.append( gen_Q2_theta_E ) # 7
    funclist.append( gen_run_qr ) # 8
    funclist.append( gen_Log10x_Log10y ) # 9
    funclist.append( gen_lx_ly_lQ2 ) # 10
    funclist.append( rel_gen_Q2_el_Q2 ) # 11
    funclist.append( gen_phi ) # 12
    funclist.append( rel_gen_Q2_beff_el_Q2 ) # 13
    funclist.append( gen_ys ) # 14
    funclist.append( gamma_p_ys ) # 15
    funclist.append( gamma_p_sqrt_ys ) # 16
    funclist.append( gen_true_lx_ly ) # 17
    funclist.append( gen_true_lx ) # 18
    funclist.append( gen_true_ly ) # 19
    funclist.append( gen_true_W ) # 20
    funclist.append( gen_el_en_log10_theta ) # 21
    funclist.append( gen_el_en_log10_theta_lQ2 ) # 22
    funclist.append( gen_eta ) # 23

    inp = TFile.Open(basedir+"/"+infile)
    global tree
    tree = inp.Get("ltree")

    funclist[iplot]()

#main

#_____________________________________________________________________________
def gen_xy():

    #distribution of x and y

    xbin = 2e-9
    xmin = 8e-14
    xmax = 2e-4

    ybin = 1e-2
    ymin = 0.06
    ymax = 1.1

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    tree.Draw("gen_y:gen_x >> hXY")

    can = ut.box_canvas()

    ut.put_yx_tit(hXY, "#it{y}", "#it{x}", 1.4, 1.2)

    hXY.Draw()

    gPad.SetLogx()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_xy

#_____________________________________________________________________________
def gen_Q2():

    #plot the Q^2

    qbin = 1e-3
    qmin = 1e-4
    qmax = 1

    hQ2 = ut.prepare_TH1D("hQ2", qbin, qmin, qmax)

    tree.Draw("true_Q2 >> hQ2")

    can = ut.box_canvas()

    ut.put_yx_tit(hQ2, "Events", "#it{Q}^{2}", 1.4, 1.2)

    hQ2.Draw()

    gPad.SetLogx()
    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Q2

#_____________________________________________________________________________
def gen_Log10_Q2():

    #plot the log_10(Q^2)

    lqbin = 0.02
    lqmin = -11
    lqmax = 6

    hLog10Q2 = ut.prepare_TH1D("hLog10Q2", lqbin, lqmin, lqmax)

    tree.Draw("TMath::Log10(true_Q2) >> hLog10Q2")
    #tree.Draw("TMath::Log10(gen_el_Q2) >> hLog10Q2")

    can = ut.box_canvas()

    gPad.SetGrid()

    ut.put_yx_tit(hLog10Q2, "Events", "log_{10}(#it{Q}^{2})", 1.4, 1.2)

    gPad.SetLogy()

    hLog10Q2.Draw()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Log10_Q2

#_____________________________________________________________________________
def gen_E():

    #electron energy

    ebin = 0.01
    emin = 0
    emax = 20

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    #tree.Draw("gen_E >> hE")
    tree.Draw("el_en >> hE")

    can = ut.box_canvas()

    ut.put_yx_tit(hE, "Events", "#it{E'}", 1.4, 1.2)

    hE.Draw()

    gPad.SetLogy()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_E

#_____________________________________________________________________________
def gen_theta():

    #electron polar angle theta

    #theta range, rad
    tbin = 1e-3
    tmin = 0
    tmax = 0.2

    hTheta = ut.prepare_TH1D("hTheta", tbin, tmin, tmax)

    tree.Draw("TMath::Pi()-gen_theta >> hTheta")

    can = ut.box_canvas()

    ut.put_yx_tit(hTheta, "Events", "#theta (rad)", 1.4, 1.2)

    hTheta.Draw()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_theta

#_____________________________________________________________________________
def gen_Q2_theta():

    #Q^2 relative to theta

    qbin = 1e-3
    #qmin = 1e-5
    qmin = 0
    qmax = 0.45

    tbin = 5e-4
    tmin = 0
    tmax = 0.04

    hQ2theta = ut.prepare_TH2D("hQ2theta", tbin, tmin, tmax, qbin, qmin, qmax)

    tree.Draw("true_Q2:gen_theta >> hQ2theta")

    can = ut.box_canvas()

    ut.put_yx_tit(hQ2theta, "#it{Q}^{2}", "#theta (rad)", 1.4, 1.2)

    hQ2theta.Draw()

    #gPad.SetLogx()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Q2_theta

#_____________________________________________________________________________
def gen_Log10x_y():

    #distribution of log_10(x) and y

    xbin = 0.01
    xmin = -13.5
    xmax = -3.5

    ybin = 5e-5
    #ymin = 0.06
    ymin = 0
    ymax = 1.1

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    can = ut.box_canvas()

    tree.Draw("gen_y:TMath::Log10(gen_x) >> hXY")
    #tree.Draw("gen_y:gen_u >> hXY")

    ytit = "#it{y}"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(x)"+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hXY.Draw()

    gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Log10x_y

#_____________________________________________________________________________
def gen_Q2_theta_E():

    #Q^2 relative to theta and energy

    qbin = 0.035
    qmin = 0
    qmax = 3.2

    tbin = 1.5e-3
    tmin = 0
    tmax = 0.1

    ebin = 0.1
    emin = 0.1
    emax = 18

    hQtE = ut.prepare_TH3D("hQtE", tbin, tmin, tmax, qbin, qmin, qmax, ebin, emin, emax)

    can = ut.box_canvas()

    tree.Draw("gen_E:true_Q2:(TMath::Pi()-gen_theta) >> hQtE")

    profile = hQtE.Project3DProfile("yx")

    profile.SetXTitle("Electron scattering angle #theta (rad)")
    profile.SetYTitle("#it{Q}^{2} (GeV^{2})")
    profile.SetZTitle("Electron energy E_{e^{-}} (GeV)")
    profile.SetTitle("")

    profile.SetTitleOffset(1.3, "X")
    profile.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.03, 0.15)

    profile.SetContour(300)

    profile.Draw("colz")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Q2_theta_E

#_____________________________________________________________________________
def gen_run_qr():

    #run a testing sample with the quasi-real generator

    from gen_quasi_real import gen_quasi_real
    from gen_quasi_real_v2 import gen_quasi_real_v2
    import ConfigParser

    parse = ConfigParser.RawConfigParser()
    parse.read("lgen_quasireal_18x275.ini")

    #gen = gen_quasi_real(parse, None)
    gen = gen_quasi_real_v2(parse, None)

    for i in xrange(12):

        u = rt.Double(0)
        y = rt.Double(0)
        gen.eq.GetRandom2(u, y)

        print u, y

#gen_run_qr

#_____________________________________________________________________________
def gen_Log10x_Log10y():

    #distribution of log_10(x) and log_10(y)

    xbin = 0.05 # 2e-2
    xmin = -12
    xmax = 0

    ybin = 0.02
    ymin = -4.5
    ymax = 0

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    can = ut.box_canvas()

    #tree.Draw("TMath::Log10(gen_y):TMath::Log10(gen_x) >> hXY")
    tree.Draw("gen_v:gen_u >> hXY")

    ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hXY.Draw()

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    gPad.SetGrid()

    #gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_Log10x_Log10y

#_____________________________________________________________________________
def gen_lx_ly_lQ2():

    #distribution of log_10(x), log_10(y) and log_10(Q^2)

    xbin = 0.05
    xmin = -12
    xmax = 0

    ybin = 0.02
    ymin = -4.5
    ymax = 0

    lqbin = 0.1
    lqmin = -9
    lqmax = 4.3

    hXYQ2 = ut.prepare_TH3D("hXYQ2", xbin, xmin, xmax, ybin, ymin, ymax, lqbin, lqmin, lqmax)

    can = ut.box_canvas()

    tree.Draw("TMath::Log10(true_Q2):gen_v:gen_u >> hXYQ2")

    pXYQ2 = hXYQ2.Project3DProfile("yx")

    ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    pXYQ2.SetXTitle(xtit)
    pXYQ2.SetYTitle(ytit)
    pXYQ2.SetZTitle("log_{10}(#it{Q}^{2} (GeV^{2}))")
    pXYQ2.SetTitle("")

    pXYQ2.SetTitleOffset(1.3, "X")
    pXYQ2.SetTitleOffset(1.4, "Z")

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.03, 0.16)

    gPad.SetGrid()

    pXYQ2.SetContour(300)
    pXYQ2.SetMinimum(lqmin)
    pXYQ2.SetMaximum(lqmax)

    pXYQ2.Draw("colz")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_lx_ly_lQ2

#_____________________________________________________________________________
def rel_gen_Q2_el_Q2():

    #relative difference in true Q^2 and generated electron Q^2

    dbin = 1e-5
    dmin = -1e-2
    dmax = 1e-2

    lqbin = 0.1
    lqmin = -12
    lqmax = 3

    hRQ2 = ut.prepare_TH2D("hRQ2", lqbin, lqmin, lqmax, dbin, dmin, dmax)

    can = ut.box_canvas()

    tree.Draw("(gen_Q2-gen_el_Q2)/gen_Q2:TMath::Log10(gen_Q2) >> hRQ2")

    #ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    #xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    #ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    #ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hRQ2.Draw()

    hRQ2.SetMinimum(0.98)
    hRQ2.SetContour(300)

    gPad.SetGrid()

    #gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rel_gen_Q2_el_Q2

#_____________________________________________________________________________
def rel_gen_Q2_beff_el_Q2():

    #relative difference in Q^2 between plain generator and electron after beam effects

    dbin = 0.1
    dmin = -1
    dmax = 1

    lqbin = 0.1
    lqmin = -12
    lqmax = 3

    hRQ2 = ut.prepare_TH2D("hRQ2", lqbin, lqmin, lqmax, dbin, dmin, dmax)

    can = ut.box_canvas()

    tree.Draw("(gen_Q2-gen_el_Q2)/gen_Q2:TMath::Log10(gen_Q2) >> hRQ2")

    #ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    #xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    #ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    #ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hRQ2.Draw()

    hRQ2.SetMinimum(0.98)
    hRQ2.SetContour(300)

    gPad.SetGrid()

    #gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rel_gen_Q2_beff_el_Q2

#_____________________________________________________________________________
def gen_phi():

    #electron azimuthal angle phi

    #phi range, rad
    pbin = 0.1
    pmin = -7
    pmax = 7

    hPhi = ut.prepare_TH1D("hPhi", pbin, pmin, pmax)

    tree.Draw("gen_phi >> hPhi")

    can = ut.box_canvas()

    ut.put_yx_tit(hPhi, "Events", "#phi (rad)", 1.4, 1.2)

    hPhi.Draw()

    #gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_phi

#_____________________________________________________________________________
def rel_gen_Q2_beff_el_Q2():

    #relative difference in Q^2 between plain generator and electron after beam effects

    dbin = 0.05
    dmin = -10
    dmax = 2

    lqbin = 0.05
    lqmin = -11
    lqmax = 3

    hRQ2 = ut.prepare_TH2D("hRQ2", lqbin, lqmin, lqmax, dbin, dmin, dmax)

    can = ut.box_canvas()

    Q2form = "(2*18*el_en*(1-TMath::Cos(TMath::Pi()-el_theta)))"

    #tree.Draw("(gen_el_Q2-"+Q2form+")/gen_el_Q2:TMath::Log10(gen_el_Q2) >> hRQ2")

    tree.Draw("(gen_Q2-"+Q2form+")/gen_Q2:TMath::Log10(gen_Q2) >> hRQ2")


    #ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    #xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    #ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    #ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hRQ2.Draw()

    hRQ2.SetMinimum(0.98)
    hRQ2.SetContour(300)

    gPad.SetGrid()

    #gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#rel_gen_Q2_beff_el_Q2

#_____________________________________________________________________________
def gen_ys():

    #CM energy s * generated y as input to gamma-p total cross section

    sqrt_s = 28.6 # GeV

    #ys range
    ysbin = 0.1
    ysmin = 0
    ysmax = 30

    hYS = ut.prepare_TH1D("hYS", ysbin, ysmin, ysmax)

    tree.Draw("true_y*"+str(sqrt_s)+" >> hYS")

    can = ut.box_canvas()

    ut.put_yx_tit(hYS, "Events", "#ys (GeV^{2})", 1.4, 1.2)

    hYS.Draw()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_ys

#_____________________________________________________________________________
def gamma_p_ys():

    #distribution of total gamma-proton cross section over a given CM energy s and generated y

    sqrt_s = 28.6 # GeV

    #gamma-p range
    gpbin = 0.01
    gpmin = 0
    gpmax = 1

    hGP = ut.prepare_TH1D("hGP", gpbin, gpmin, gpmax)

    scm = sqrt_s**2
    form = "0.0677*TMath::Power((true_y*"+str(scm)+"), 0.0808)"
    form += "+0.129*TMath::Power((true_y*"+str(scm)+"), -0.4525)"

    #print form

    tree.Draw(form+" >> hGP")

    can = ut.box_canvas()

    ut.put_yx_tit(hGP, "Events", "#sigma(#gamma p) (mb)", 1.4, 1.2)

    hGP.Draw()

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gamma_p_ys

#_____________________________________________________________________________
def gamma_p_sqrt_ys():

    #total gamma-proton cross section as a function of sqrt(sy), the CM energy s and generated y

    sqrt_s = 140.7 # GeV, 18x275
    #sqrt_s = 63.3 # GeV, 10x100
    #sqrt_s = 28.6 # GeV, 5x41

    #sqrt(sy) range
    sybin = 0.1
    symin = 0
    symax = 160

    #cross section range
    sigbin = 0.01
    sigmin = 0
    sigmax = 0.5

    hGPys = ut.prepare_TH2D("hGPys", sybin, symin, symax, sigbin, sigmin, sigmax)

    #cross section formula
    scm = sqrt_s**2
    sig_form = "0.0677*TMath::Power((true_y*"+str(scm)+"), 0.0808)"
    sig_form += "+0.129*TMath::Power((true_y*"+str(scm)+"), -0.4525)"

    #sqrt(sy) formula
    syform = "TMath::Sqrt(true_y*"+str(scm)+")"

    #print sig_form
    #print syform

    tree.Draw("("+sig_form+"):("+syform+") >> hGPys")

    can = ut.box_canvas()

    ut.put_yx_tit(hGPys, "#sigma(#gamma p) (mb)", "#sqrt{ys}", 1.4, 1.2)

    hGPys.Draw()

    gPad.SetGrid()

    gPad.SetLogx()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gamma_p_sqrt_ys

#_____________________________________________________________________________
def gen_true_lx_ly():

    #generator true log_10(y) and log_10(x)

    xbin = 0.05 # 2e-2
    xmin = -12
    xmax = 0

    ybin = 0.02
    ymin = -4.5
    ymax = 0

    hXY = ut.prepare_TH2D("hXY", xbin, xmin, xmax, ybin, ymin, ymax)

    can = ut.box_canvas()

    tree.Draw("TMath::Log10(true_y):TMath::Log10(true_x) >> hXY")

    ytit = "log_{10}(#it{y})"+" / {0:.3f}".format(ybin)
    xtit = "log_{10}(#it{x})"+" / {0:.3f}".format(xbin)
    ut.put_yx_tit(hXY, ytit, xtit, 1.4, 1.4)

    ut.set_margin_lbtr(gPad, 0.1, 0.11, 0.03, 0.12)

    hXY.Draw()

    hXY.SetMinimum(0.98)
    hXY.SetContour(300)

    gPad.SetGrid()

    #gPad.SetLogy()
    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_true_lx_ly

#_____________________________________________________________________________
def gen_true_lx():

    #generator true log_10(x)

    #lx range
    xbin = 0.1
    xmin = -12
    xmax = 0

    hX = ut.prepare_TH1D("hX", xbin, xmin, xmax)

    tree.Draw("TMath::Log10(true_x) >> hX")

    can = ut.box_canvas()

    ut.put_yx_tit(hX, "Events", "x", 1.4, 1.2)

    hX.Draw()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_true_lx

#_____________________________________________________________________________
def gen_true_ly():

    #generator true log_10(y)

    #ly range
    ybin = 0.05
    ymin = -5
    ymax = 0

    hY = ut.prepare_TH1D("hY", ybin, ymin, ymax)

    tree.Draw("TMath::Log10(true_y) >> hY")

    can = ut.box_canvas()

    ut.put_yx_tit(hY, "Events", "y", 1.4, 1.2)

    hY.Draw()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_true_ly

#_____________________________________________________________________________
def gen_true_W():

    #generator true W = sqrt( ys(1-x) ) with true x and y

    # GeV^2
    #scm = 19800.8 # 18x275
    scm = 820.8 # 5x41

    #W range
    wbin = 0.1
    wmin = 0
    wmax = 150

    hW = ut.prepare_TH1D("hW", wbin, wmin, wmax)
    hW2 = ut.prepare_TH1D("hW2", wbin, wmin, wmax)

    form = "TMath::Sqrt(true_y*"+str(scm)+"*(1.-true_x))"
    form2 = "TMath::Sqrt(true_y*"+str(scm)+")"

    tree.Draw(form+" >> hW")
    tree.Draw(form2+" >> hW2")

    can = ut.box_canvas()

    ut.put_yx_tit(hW, "Events", "W (GeV)", 1.4, 1.2)

    #ut.set_H1D_col(hW2, rt.kRed)
    ut.line_h1(hW)
    ut.line_h1(hW2, rt.kRed)


    hW.Draw()
    hW2.Draw("e1same")

    gPad.SetGrid()
    gPad.SetLogy()
    gPad.SetLogx()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_true_W

#_____________________________________________________________________________
def gen_el_en_log10_theta():

    #electron energy and scattering angle

    #bins in log_10(theta)
    ltbin = 0.2
    ltmin = -8
    #ltmax = -1.2
    ltmax = 1

    #bins in energy
    ebin = 0.4
    emin = 0
    emax = 21

    can = ut.box_canvas()

    hEnTheta = ut.prepare_TH2D("hEnTheta", ltbin, ltmin, ltmax, ebin, emin, emax)

    form = "el_en:TMath::Log10(TMath::Pi()-el_theta)"
    tree.Draw(form+" >> hEnTheta")

    ytit = "Electron energy #it{E}_{e} / "+"{0:.1f} GeV".format(ebin)
    xtit = "Scattering angle log_{10}(#theta_{e}) / "+"{0:.2f} rad".format(ltbin)
    ut.put_yx_tit(hEnTheta, ytit, xtit, 1.4, 1.3)

    hEnTheta.SetTitleOffset(1.5, "Z")
    hEnTheta.SetZTitle("Event counts")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.01, 0.15)

    gPad.SetLogz()
    gPad.SetGrid()

    hEnTheta.SetMinimum(0.98)
    hEnTheta.SetContour(300)

    hEnTheta.Draw("colz")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_el_en_log10_theta

#_____________________________________________________________________________
def gen_el_en_log10_theta_lQ2():

    #electron energy, scattering angle and log10(Q^2)

    #bins in log_10(theta)
    ltbin = 0.2
    ltmin = -8
    ltmax = 1

    #bins in energy
    ebin = 0.4
    emin = 0
    emax = 21

    #bins in Q2
    lqbin = 0.1
    lqmin = -9
    lqmax = 2.5

    can = ut.box_canvas()

    hEnThetaQ2 = ut.prepare_TH3D("hEnThetaQ2", ltbin, ltmin, ltmax, ebin, emin, emax, lqbin, lqmin, lqmax)

    #form = "TMath::Log10(true_Q2):el_en:TMath::Log10(TMath::Pi()-el_theta)"
    form = "TMath::Log10(true_Q2):gen_E:TMath::Log10(TMath::Pi()-gen_theta)"
    tree.Draw(form+" >> hEnThetaQ2")

    pEnThetaQ2 = hEnThetaQ2.Project3DProfile("yx")

    ytit = "Electron energy #it{E}_{e} / "+"{0:.1f} GeV".format(ebin)
    xtit = "Scattering angle log_{10}(#theta_{e}) / "+"{0:.2f} rad".format(ltbin)
    ut.put_yx_tit(pEnThetaQ2, ytit, xtit, 1.4, 1.3)

    pEnThetaQ2.SetTitleOffset(1.3, "Z")
    pEnThetaQ2.SetZTitle("log_{10}(#it{Q}^{2} (GeV^{2}))")
    pEnThetaQ2.SetTitle("")

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.01, 0.15)

    #gPad.SetLogz()
    gPad.SetGrid()

    pEnThetaQ2.SetMinimum(lqmin)
    pEnThetaQ2.SetMaximum(lqmax)
    pEnThetaQ2.SetContour(300)

    pEnThetaQ2.Draw("colz")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_el_en_log10_theta_lQ2

#_____________________________________________________________________________
def gen_eta():

    #electron pseudorapidity

    #eta range
    etabin = 0.3
    etamin = -20
    etamax = 10

    hEta = ut.prepare_TH1D("hEta", etabin, etamin, etamax)

    form = "-TMath::Log(TMath::Tan(gen_theta/2.))"
    #form = "-TMath::Log(TMath::Tan(el_theta/2.))"
    tree.Draw(form+" >> hEta")

    can = ut.box_canvas()

    ut.put_yx_tit(hEta, "Events", "#eta", 1.4, 1.2)

    hEta.Draw()

    gPad.SetLogy()
    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#gen_eta

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

    #beep when done
    gSystem.Exec("mplayer ../computerbeep_1.mp3 > /dev/null 2>&1")









