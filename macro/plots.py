#!/usr/bin/python

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem

import plot_utils as ut

#_____________________________________________________________________________
def phot_gen_en():

    #energy deposited in photon detector relative to generated photon energy

    ebin = 5e-5
    emin = 0
    emax = 5e-3

    can = ut.box_canvas()

    hE = ut.prepare_TH2D("hE", ebin, emin, emax, ebin, emin, emax)

    tree.Draw("phot_en:phot_gen >> hE", "phot_gen<0.003")
    #tree.Draw("phot_en >> hE", "lowQ2s1_IsHit == 1")
    #tree.Draw("phot_gen >> hE", "lowQ2s1_IsHit == 1")
    #tree.Draw("phot_gen >> hE", "lowQ2s2_IsHit == 1")
    #tree.Draw("phot_gen >> hE", "lowQ2s1_en > 1")
    #tree.Draw("phot_gen >> hE", "lowQ2s2_en > 1")

    #hE.SetYTitle("Events / ({0:.3f}".format(ebin)+" GeV)")
    #hE.SetXTitle("#it{E}_{#gamma} (GeV)")

    #hE.SetTitleOffset(1.5, "Y")
    #hE.SetTitleOffset(1.3, "X")

    #gPad.SetTopMargin(0.01)
    #gPad.SetRightMargin(0.02)
    #gPad.SetBottomMargin(0.1)
    #gPad.SetLeftMargin(0.11)

    #hE.GetYaxis().SetMoreLogLabels()

    hE.SetMinimum(0.98)
    hE.SetContour(300)

    hE.Draw()

    gPad.SetLogz()

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#phot_gen_en

#_____________________________________________________________________________
def phot_hits_xy():

    xbin = 1
    xmin = -120
    xmax = 120

    can = ut.box_canvas()

    hX = ut.prepare_TH2D("hX", xbin, xmin, xmax, xbin, xmin, xmax)

    from BoxCalV2Hits import BoxCalV2Hits
    hits = BoxCalV2Hits("phot", tree)

    nevt = tree.GetEntries()
    #nevt = 12

    for ievt in xrange(nevt):

        tree.GetEntry(ievt)

        #if hits.GetN() <= 1: continue
        #print hits.GetN()

        for ihit in xrange(hits.GetN()):

            #if hits.GetPdg(ihit) == 22: continue
            #if hits.GetPdg(ihit) != 22: continue

            #if hits.GetEn(ihit) > 0.1: continue
            if hits.GetEn(ihit) < 0.1: continue

            hX.Fill(hits.GetX(ihit), hits.GetY(ihit))

            #print " ", hits.GetPdg(ihit), hits.GetX(ihit), hits.GetY(ihit), hits.GetZ(ihit), hits.GetEn(ihit)

    print "Entries:", hX.GetEntries()

    hX.SetMinimum(0.98)
    hX.SetContour(300)

    hX.Draw()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def plot_spec_acc():

    #acceptance parametrization
    from spec_acc import spec_acc
    acc0 = spec_acc()
    acc = spec_acc(8200, 0.26, 42, 242)

    #acc.length = 8200

    can = ut.box_canvas()

    frame = gPad.DrawFrame(1, 0, 22, 1)
    frame.Draw()

    acc0.acc_func.Draw("same")
    acc0.acc_func.SetLineStyle(rt.kDashed)
    acc.acc_func.Draw("same")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def acc_from_tmp():

    #spectrometer acceptance from temporary file

    tmp = TFile.Open("tmp/hacc.root")
    hAcc = tmp.Get("divide_hSel_by_hAll")

    can = ut.box_canvas()

    hAcc.Draw("AP")

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.01, 0.02)

    en = rt.Double(0)
    av = rt.Double(0)
    iacc = 0.
    for i in xrange(hAcc.GetN()):
        hAcc.GetPoint(i, en, av)

        iacc += av*(hAcc.GetErrorXhigh(i)+hAcc.GetErrorXlow(i))

    print "iacc:", iacc

    #acceptance parametrization
    from spec_acc import spec_acc
    acc = spec_acc()
    acc.scale = iacc/acc.acc_func.Integral(2, 21)

    print "int_func:", acc.acc_func.Integral(2, 21)

    acc.acc_func.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acc_from_tmp

#_____________________________________________________________________________
def acceptance_autobin():

    #spectrometer acceptance as a function of generated photon energy,
    #size of bins is given by the desired precision

    emin = 1
    emax = 20

    edet = 1

    prec = 0.07
    #prec = 0.02
    delt = 1e-2

    sel = "up_en>"+str(edet*1e3)+" && down_en>"+str(edet*1e3)

    can = ut.box_canvas()

    gROOT.LoadMacro("get_acc.C")
    hAcc = rt.get_acc(tree, "phot_gen", sel, prec, delt)

    #ut.set_graph(hAcc, rt.kBlue)
    ut.set_graph(hAcc)

    #hAcc.GetYaxis().SetTitle("Spectrometer acceptance / "+str(prec*1e2)+" %")
    hAcc.GetYaxis().SetTitle("Spectrometer acceptance")
    hAcc.GetXaxis().SetTitle("Generated #it{E}_{#gamma} (GeV)")
    hAcc.SetTitle("")

    hAcc.GetYaxis().SetTitleOffset(2)
    hAcc.GetXaxis().SetTitleOffset(1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.01, 0.02)

    hAcc.Draw("AP")

    #save the acceptance to a temporary file
    #tmp = TFile.Open("tmp/hacc.root", "recreate")
    #hAcc.Write()
    #tmp.Write()
    #tmp.Close()

    #integrate the acceptance to scale the parametrization
    en = rt.Double(0)
    av = rt.Double(0)
    iacc = 0.
    for i in xrange(hAcc.GetN()):
        hAcc.GetPoint(i, en, av)
        iacc += av*(hAcc.GetErrorXhigh(i)+hAcc.GetErrorXlow(i))

    #acceptance parametrization
    from spec_acc import spec_acc
    #acc = spec_acc()
    acc = spec_acc(8200, 0.26, 42, 242)
    acc.scale = iacc/acc.acc_func.Integral(2, 21)

    acc.acc_func.Draw("same")

    leg = ut.prepare_leg(0.63, 0.86, 0.12, 0.1)#, 0.027) # x, y, dx, dy, tsiz
    #leg.AddEntry(hAcc, "#frac{#it{N}(#it{E}_{up}>1 #bf{and} #it{E}_{down}>1 GeV)}{#it{N}_{all}}", "lp")
    leg.AddEntry(hAcc, "Geant4", "lp")
    leg.AddEntry(acc.acc_func, "Geometry model", "l")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#acceptance_autobin

#_____________________________________________________________________________
def up_down_corrected():

    #energy in spectrometer corrected for the acceptance
    ebin = 0.5
    emin = 1
    emax = 20

    edet = 1

    sel = "up_en>"+str(edet*1e3)+" && down_en>"+str(edet*1e3)

    can = ut.box_canvas()

    #sum energy from up and down detectors
    hSum = ut.prepare_TH1D("hSum", ebin, emin, emax)
    tree.Draw("(up_en+down_en)/1000. >> hSum", sel)

    #calculate the acceptance
    hRec = ut.prepare_TH1D("hRec", ebin, emin, emax)
    hGen = ut.prepare_TH1D("hGen", ebin, emin, emax)

    tree.Draw("phot_gen/1000 >> hRec", sel)
    tree.Draw("phot_gen/1000 >> hGen")

    hAcc = hRec.Clone()
    hAcc.Sumw2()
    hAcc.Divide(hGen)

    #apply the acceptance
    hSum.Sumw2()
    for i in xrange(hAcc.GetNbinsX()+1):
        acc = hAcc.GetBinContent(i)
        if acc > 0.:
            hSum.SetBinContent(i, hSum.GetBinContent(i)/acc )
        else:
            hSum.SetBinContent(i, 0)

    hSum.Draw()

    #cross section parametrization
    sys.path.append('/home/jaroslav/sim/lgen/')
    from gen_zeus import gen_zeus
    gen = gen_zeus(18, 275, emin)
    sig = gen.dSigDe
    sig.SetNpx(300)
    sig.SetLineWidth(3)

    #scale the cross section to the plot
    norm = ebin * hSum.Integral() / sig.Integral(emin, gen.Ee)
    gen.ar2 = norm * gen.ar2

    sig.Draw("same")

    gPad.SetLogy()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#up_down_corrected

#_____________________________________________________________________________
def acceptance():

    #spectrometer acceptance as a function of generated photon energy

    #ebin = 1.5
    ebin = 0.5
    emin = 1
    emax = 20

    edet = 1

    can = ut.box_canvas()

    hRec = ut.prepare_TH1D("hRec", ebin, emin, emax)
    hGen = ut.prepare_TH1D("hGen", ebin, emin, emax)

    #sel = "up_en>"+str(edet*1e3)+" && down_en>"+str(edet*1e3)
    sel = "up_en>"+str(edet)+" && down_en>"+str(edet)

    #tree.Draw("phot_gen/1000 >> hRec", sel)
    #tree.Draw("phot_gen/1000 >> hGen")
    tree.Draw("phot_gen >> hRec", sel)
    tree.Draw("phot_gen >> hGen")

    print "Rec entries:", hRec.GetEntries()
    print "Gen entries:", hGen.GetEntries()

    hAcc = hRec.Clone()
    hAcc.Sumw2()
    hAcc.Divide(hGen)

    #print "Integrated acceptance:", hAcc.Integral()

    hAcc.SetYTitle("Spectrometer acceptance / ({0:.3f}".format(ebin)+" GeV)")
    hAcc.SetXTitle("Generated #it{E}_{#gamma} (GeV)")

    hAcc.SetTitleOffset(1.8, "Y")
    hAcc.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.02)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.12)

    #hRec.Draw()
    #hGen.Draw()
    hAcc.Draw()

    #acceptance parametrization
    from spec_acc import spec_acc
    acc = spec_acc()
    #acc.scale = 0.081*0.7

    acc.scale = hAcc.GetBinWidth(1)*hAcc.Integral()/acc.acc_func.Integral(2, 21)
    #acc.scale = hAcc.Integral("w")/acc.acc_func.Integral(2, 21)

    print
    #print "scale:", acc.scale

    print "int_hacc:", hAcc.Integral()*hAcc.GetBinWidth(1)
    #print "binw:", hAcc.GetBinWidth(1)
    print "int_func:", acc.acc_func.Integral(2, 21)

    #ih = scale*if   scale = ih/if

    acc.acc_func.Draw("same")

    leg = ut.prepare_leg(0.64, 0.84, 0.15, 0.15, 0.027) # x, y, dx, dy, tsiz
    leg.AddEntry(hAcc, "#frac{#it{N}(#it{E}_{up}>1 #bf{and} #it{E}_{down}>1 GeV)}{#it{N}_{all}}", "lp")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def up_down_en():

    #up and down spectrometers energy sum

    ebin = 0.1
    emin = 0
    emax = 20

    edet = 1

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    sel = "up_en>"+str(edet*1e3)+" && down_en>"+str(edet*1e3)

    #tree.Draw("(up_en+down_en)/1000. >> hE", sel)
    #tree.Draw("up_en/1000. >> hE")#, sel)
    #tree.Draw("down_en/1000. >> hE")
    #tree.Draw("up_en >> hE")#, sel)
    tree.Draw("down_en >> hE")

    print "Entries:", hE.GetEntries()

    hE.SetYTitle("Events / ({0:.3f}".format(ebin)+" GeV)")
    hE.SetXTitle("#it{E}_{#gamma} = #it{E}_{up} + #it{E}_{down} (GeV)")

    hE.SetTitleOffset(1.4, "Y")
    hE.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.02)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.1)

    #hE.GetYaxis().SetMoreLogLabels()

    hE.Draw()

    gPad.SetLogy()

    leg = ut.prepare_leg(0.58, 0.8, 0.2, 0.15, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hE, "#it{E}_{up} + #it{E}_{down}", "lp")
    leg.AddEntry(None, "#it{E}_{up}>1 #bf{and} #it{E}_{down}>1 GeV", "")
    leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def down_xy():

    #down spectrometer first point in xy

    xbin = 0.1

    xmin = -12
    xmax = 12

    ymin = -25
    ymax = -3

    emin = 0.7

    can = ut.box_canvas()

    hX = ut.prepare_TH2D("hX", xbin, xmin, xmax, xbin, ymin, ymax)

    sel = "down_en>"+str(emin*1e3)

    #tree.Draw("down_y/10:down_x/10 >> hX", sel)
    tree.Draw("down_hy/10:down_hx/10 >> hX")

    hX.SetXTitle("Horizontal #it{x} (cm)")
    hX.SetYTitle("Vertical #it{y} (cm)")

    hX.GetXaxis().CenterTitle()
    hX.GetYaxis().CenterTitle()

    hX.SetTitleOffset(1.2, "Y")
    hX.SetTitleOffset(1.2, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.12)
    gPad.SetBottomMargin(0.09)
    gPad.SetLeftMargin(0.09)

    hX.Draw()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def up_xy():

    #up spectrometer first point in xy

    xbin = 0.1

    xmin = -12
    xmax = 12

    ymin = 3
    ymax = 25

    emin = 0.7

    can = ut.box_canvas()

    hX = ut.prepare_TH2D("hX", xbin, xmin, xmax, xbin, ymin, ymax)

    sel = "up_en>"+str(emin*1e3)

    #tree.Draw("up_y/10:up_x/10 >> hX", sel)
    tree.Draw("up_hy/10:up_hx/10 >> hX")

    hX.SetXTitle("Horizontal #it{x} (cm)")
    hX.SetYTitle("Vertical #it{y} (cm)")

    hX.GetXaxis().CenterTitle()
    hX.GetYaxis().CenterTitle()

    hX.SetTitleOffset(1.2, "Y")
    hX.SetTitleOffset(1.2, "X")

    gPad.SetTopMargin(0.02)
    gPad.SetRightMargin(0.11)
    gPad.SetBottomMargin(0.09)
    gPad.SetLeftMargin(0.09)

    hX.Draw()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def phot_xy():

    #photon detector first point in xy

    xbin = 0.1
    xmin = -12
    xmax = 12

    can = ut.box_canvas()

    hX = ut.prepare_TH2D("hX", xbin, xmin, xmax, xbin, xmin, xmax)

    #tree.Draw("phot_y/10:phot_x/10 >> hX")#, "phot_en<1000")
    tree.Draw("phot_hy/10:phot_hx/10 >> hX")#, "phot_en<1000")

    hX.SetXTitle("Horizontal #it{x} (cm)")
    hX.SetYTitle("Vertical #it{y} (cm)")

    hX.GetXaxis().CenterTitle()
    hX.GetYaxis().CenterTitle()

    hX.SetTitleOffset(1.2, "Y")
    hX.SetTitleOffset(1.2, "X")

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.11)
    gPad.SetBottomMargin(0.09)
    gPad.SetLeftMargin(0.09)

    hX.Draw()

    gPad.SetLogz()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#_____________________________________________________________________________
def phot_en():

    #energy deposited in photon detector

    #ebin = 1e-4
    ebin = 0.1
    emin = 0
    #emax = 0.11
    emax = 19

    can = ut.box_canvas()

    hE = ut.prepare_TH1D("hE", ebin, emin, emax)

    tree.Draw("phot_en >> hE")
    #tree.Draw("phot_gen >> hE")
    #tree.Draw("phot_gen >> hE", "phot_IsHit == 1")
    #tree.Draw("phot_en >> hE", "lowQ2s1_IsHit == 1")
    #tree.Draw("phot_gen >> hE", "lowQ2s1_IsHit == 1")
    #tree.Draw("phot_gen >> hE", "lowQ2s2_IsHit == 1")
    #tree.Draw("phot_gen >> hE", "lowQ2s1_en > 1")
    #tree.Draw("phot_gen >> hE", "lowQ2s2_en > 1")

    #cross section parametrization
    import ConfigParser
    parse = ConfigParser.RawConfigParser()
    parse.add_section("lgen")
    #parse.set("lgen", "emin", emin)
    parse.set("lgen", "emin", "0.05")
    import sys
    sys.path.append('/home/jaroslav/sim/eic-lgen/')
    from gen_zeus import gen_zeus
    gen = gen_zeus(18, 275, parse)
    gen.dSigDe.SetNpx(300)
    gen.dSigDe.SetLineWidth(3)

    #scale the cross section to the plot
    #norm = ebin * hE.Integral() / gen.dSigDe.Integral(emin, gen.Ee)
    #gen.ar2 = norm * gen.ar2

    hE.SetYTitle("Events / ({0:.3f}".format(ebin)+" GeV)")
    hE.SetXTitle("#it{E}_{#gamma} (GeV)")

    hE.SetTitleOffset(1.5, "Y")
    hE.SetTitleOffset(1.3, "X")

    gPad.SetTopMargin(0.01)
    gPad.SetRightMargin(0.02)
    gPad.SetBottomMargin(0.1)
    gPad.SetLeftMargin(0.11)

    #hE.GetYaxis().SetMoreLogLabels()

    hE.Draw()

    print "Entries:", hE.GetEntries()

    #gen.dSigDe.Draw("same")

    gPad.SetLogy()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.53, 0.77, 0.24, 0.15, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry(hE, "Geant model", "lp")
    leg.AddEntry(gen.dSigDe, "Bethe-Heitler cross section", "l")
    #leg.Draw("same")

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#phot_en

#_____________________________________________________________________________
if __name__ == "__main__":

    #infile = "../data/test/lmon.root"
    #infile = "/home/jaroslav/sim/pdet/data/pdet_18x275_zeus_compcal_0p25T_1Mevt.daq.root"
    #infile = "../data/lmon_18x275_all_0p25T_100kevt.root"
    #infile = "../data/lmon_18x275_all_0p25T_1Mevt.root"
    #infile = "../data/lmon_18x275_beff2_1Mevt_v2.root"
    infile = "../data/lmon_18x275_beff2_1Mevt_v3.root"
    #infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_1Mevt.root"
    #infile = "../data/lmon_18x275_zeus_0p1GeV_beff2_NoFilter_1Mevt.root"
    #infile = "../data/lmon_18x275_uni_1keV_0p1GeV_phot_5Mevt.root"
    #infile = "../data/lumi1a/lmon_18x275_gamma_1Mevt.root"

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    iplot = 7
    funclist = []
    funclist.append( phot_en ) # 0
    funclist.append( phot_xy ) # 1
    funclist.append( up_xy ) # 2
    funclist.append( down_xy ) # 3
    funclist.append( up_down_en ) # 4
    funclist.append( acceptance ) # 5
    funclist.append( up_down_corrected ) # 6
    funclist.append( acceptance_autobin ) # 7
    funclist.append( acc_from_tmp ) # 8
    funclist.append( plot_spec_acc ) # 9
    funclist.append( phot_hits_xy ) # 10
    funclist.append( phot_gen_en ) # 11

    #open the input
    inp = TFile.Open(infile)
    tree = inp.Get("DetectorTree")
    #tree = inp.Get("ltree")

    #call the plot function
    funclist[iplot]()

















