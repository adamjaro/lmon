#!/usr/bin/python3

from pandas import read_csv

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TGraph, TGaxis

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 1

    func = {}
    func[0] = cprp
    func[1] = idc

    func[iplot]()

#main

#_____________________________________________________________________________
def cprp():

    #infile = "/home/jaroslav/sim/lmon/data/sipm/test/m30035.csv"
    infile = "/home/jaroslav/sim/lmon/data/sipm/test/m30035_12avg.csv"

    inp = read_csv(infile)

    #print(inp)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(0, 0.3, 29, 1.8)
    #frame = gPad.DrawFrame(25, 0.3, 29, 1.8)
    frame.Draw()

    gc = TGraph(len(inp))
    gr = TGraph(len(inp))

    gr_err = TGraph(2*len(inp))

    rmax = -1
    for i in range(len(inp)):

        gc.SetPoint(i, inp["Vb_V"][i], inp["Cp_F"][i]*1e9) # to nF
        rp = inp["Rp_Ohm"][i]*1e-6 # to MOhm
        rp_err = inp["Rp_err"][i]*1e-6
        gr.SetPoint(i, inp["Vb_V"][i], rp)

        gr_err.SetPoint(i, inp["Vb_V"][i], rp-rp_err)
        gr_err.SetPoint(2*len(inp)-1-i, inp["Vb_V"][i], rp+rp_err)

        if rp > rmax: rmax = rp

    rmax *= 1.1
    gr.Scale(gPad.GetUymax()/rmax)
    gr_err.Scale(gPad.GetUymax()/rmax)

    gc.SetLineColor(rt.kBlue)
    gr.SetLineColor(rt.kRed)
    gr.SetLineStyle(rt.kDashed)

    gr_err.SetFillColor(rt.kRed)
    gr_err.SetLineColor(rt.kRed)
    gr_err.SetFillStyle(3207)

    gc.Draw("lsame")
    gr.Draw("lsame")

    #gr_err.Draw("lfsame")

    xtit = "Bias voltage #it{V}_{bias} (V)"
    ytit = "Capacitance Cp (nF)"
    ut.put_yx_tit(frame, ytit, xtit, 1.4, 1.3)

    raxis = TGaxis(gPad.GetUxmax(), gPad.GetUymin(), gPad.GetUxmax(), gPad.GetUymax(), 0, rmax, 510, "+L")
    ut.set_axis(raxis)
    raxis.SetTitle("Resistance Rp (M#Omega)")
    raxis.SetTitleOffset(1.2)

    raxis.Draw()

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.02, 0.09)

    leg = ut.prepare_leg(0.24, 0.86, 0.28, 0.1, 0.035)
    leg.AddEntry(gc, "Capacitance Cp", "l")
    leg.AddEntry(gr, "Resistance Rp", "l")
    leg.Draw("same")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#cprp

#_____________________________________________________________________________
def idc():

    #infile = "/home/jaroslav/sim/lmon/data/sipm/test/m30035.csv"
    infile = "/home/jaroslav/sim/lmon/data/sipm/test/m30035_12avg.csv"

    inp = read_csv(infile)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(0, -40, 29, 460)
    frame.Draw()

    gi = TGraph(len(inp))
    gr = TGraph(len(inp))

    gi_err = TGraph(2*len(inp))

    rmax = -1
    for i in range(len(inp)):

        gi.SetPoint(i, inp["Vb_V"][i], inp["Idc_A"][i]*1e9) # to nA
        rp = inp["Rp_Ohm"][i]*1e-6 # to MOhm
        gr.SetPoint(i, inp["Vb_V"][i], rp)

        gi_err.SetPoint(i, inp["Vb_V"][i], (inp["Idc_A"][i]-inp["Idc_err"][i])*1e9)
        gi_err.SetPoint(2*len(inp)-1-i, inp["Vb_V"][i], (inp["Idc_A"][i]+inp["Idc_err"][i])*1e9)

        if rp > rmax: rmax = rp

    rmax *= 1.1
    gr.Scale(gPad.GetUymax()/rmax)

    gi.SetLineColor(rt.kBlue)
    gr.SetLineStyle(rt.kDashed)
    gr.SetLineColor(rt.kRed)

    gi_err.SetFillColor(rt.kBlue)
    gi_err.SetLineColor(rt.kBlue)
    gi_err.SetFillStyle(3207)

    gi.Draw("lsame")
    gr.Draw("lsame")

    #gi_err.Draw("fsame")

    xtit = "Bias voltage #it{V}_{bias} (V)"
    ytit = "Leakage current #it{I}_{DC} (nA)"
    ut.put_yx_tit(frame, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.02, 0.09)

    raxis = TGaxis(gPad.GetUxmax(), gPad.GetUymin(), gPad.GetUxmax(), gPad.GetUymax(), 0, rmax, 510, "+L")
    ut.set_axis(raxis)
    raxis.SetTitle("Resistance Rp (M#Omega)")
    raxis.SetTitleOffset(1.2)

    raxis.Draw()

    leg = ut.prepare_leg(0.26, 0.86, 0.28, 0.1, 0.035)
    leg.AddEntry(gi, "Leakage current #it{I}_{DC}", "l")
    leg.AddEntry(gr, "Resistance Rp", "l")
    leg.Draw("same")

    gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#idc

#_____________________________________________________________________________
def convert_from_txt():

    out = open("/home/jaroslav/sim/lmon/data/sipm/test/m30035.csv", "w")

    for i in open("/home/jaroslav/sim/lmon/data/sipm/test/m30035.txt"):
        l = i.split()
        if len(l) <=0: continue

        for ll in l:
            out.write(ll+",")

        out.write("\n")

#convert_from_txt

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()

