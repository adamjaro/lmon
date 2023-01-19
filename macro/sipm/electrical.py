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

    infile = "/home/jaroslav/sim/lmon/data/sipm/test/m30035.csv"

    inp = read_csv(infile)

    #print(inp)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(0, 0.3, 29, 1.8)
    frame.Draw()

    gc = TGraph(len(inp))
    gr = TGraph(len(inp))

    rmax = -1
    for i in range(len(inp)):

        gc.SetPoint(i, inp["Vb_V"][i], inp["Cp_nF"][i])
        gr.SetPoint(i, inp["Vb_V"][i], inp["Rp_MOhm"][i])

        if inp["Rp_MOhm"][i] > rmax: rmax = inp["Rp_MOhm"][i]

    rmax *= 1.1
    gr.Scale(gPad.GetUymax()/rmax)

    gc.SetLineColor(rt.kBlue)
    gr.SetLineColor(rt.kRed)
    gr.SetLineStyle(rt.kDashed)

    gc.Draw("lsame")
    gr.Draw("lsame")

    xtit = "#it{V}_{bias} (V)"
    ytit = "Cp (nF)"
    ut.put_yx_tit(frame, ytit, xtit, 1.4, 1.3)

    raxis = TGaxis(gPad.GetUxmax(), gPad.GetUymin(), gPad.GetUxmax(), gPad.GetUymax(), 0, rmax, 510, "+L")
    ut.set_axis(raxis)
    raxis.SetTitle("Rp (M#Omega)")
    raxis.SetTitleOffset(1.2)

    raxis.Draw()

    ut.set_margin_lbtr(gPad, 0.1, 0.1, 0.02, 0.09)

    leg = ut.prepare_leg(0.24, 0.86, 0.28, 0.1, 0.035)
    leg.AddEntry(gc, "Cp", "l")
    leg.AddEntry(gr, "Rp", "l")
    leg.Draw("same")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#cprp

#_____________________________________________________________________________
def idc():

    infile = "/home/jaroslav/sim/lmon/data/sipm/test/m30035.csv"

    inp = read_csv(infile)

    can = ut.box_canvas()
    frame = gPad.DrawFrame(0, -40, 29, 460)
    frame.Draw()

    gi = TGraph(len(inp))
    gr = TGraph(len(inp))

    rmax = -1
    for i in range(len(inp)):

        gi.SetPoint(i, inp["Vb_V"][i], inp["IDC_nA"][i])
        gr.SetPoint(i, inp["Vb_V"][i], inp["Rp_MOhm"][i])

        if inp["Rp_MOhm"][i] > rmax: rmax = inp["Rp_MOhm"][i]

    rmax *= 1.1
    gr.Scale(gPad.GetUymax()/rmax)

    gi.SetLineColor(rt.kBlue)
    gr.SetLineStyle(rt.kDashed)
    gr.SetLineColor(rt.kRed)

    gi.Draw("lsame")
    gr.Draw("lsame")

    xtit = "#it{V}_{bias} (V)"
    ytit = "#it{I}_{DC} (nA)"
    ut.put_yx_tit(frame, ytit, xtit, 1.6, 1.3)

    ut.set_margin_lbtr(gPad, 0.12, 0.1, 0.02, 0.09)

    raxis = TGaxis(gPad.GetUxmax(), gPad.GetUymin(), gPad.GetUxmax(), gPad.GetUymax(), 0, rmax, 510, "+L")
    ut.set_axis(raxis)
    raxis.SetTitle("Rp (M#Omega)")
    raxis.SetTitleOffset(1.2)

    raxis.Draw()

    leg = ut.prepare_leg(0.26, 0.87, 0.28, 0.1, 0.035)
    leg.AddEntry(gi, "#it{I}_{DC}", "l")
    leg.AddEntry(gr, "Rp", "l")
    leg.Draw("same")

    gPad.SetGrid()

    ut.invert_col(rt.gPad)
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

