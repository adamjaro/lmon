#!/usr/bin/python3

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math as ma

import ROOT as rt
from ROOT import gPad, gROOT, gStyle, TFile, gSystem, TMath

import sys
sys.path.append("../")
import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 3

    func = {}
    func[0] = en
    func[1] = pitheta
    func[2] = phi
    func[3] = lQ2
    func[4] = rec_lQ2
    func[5] = compare_lQ2

    func[iplot]()

#_____________________________________________________________________________
def en():

    #GeV
    ebin = 0.1
    emin = 3
    emax = 19

    #inp = "../../analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v6.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx6/maps_basic_v1.root"

    det = "s1_tracks"
    #det = "s2_tracks"

    sel = "is_rec==1 && itrk==1"

    infile = TFile.Open(inp)
    #tree = infile.Get(det+"_rec")
    tree = infile.Get(det)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", ebin, emin, emax, ebin, emin, emax)

    tree.Draw("rec_en:true_el_E >> hxy", sel)
    #tree.Draw("rec_en:true_el_E >> hxy", "is_rec==1")

    ytit = "Reconstructed energy #it{E_{e}} (GeV)"
    xtit = "Generated true energy #it{E_{e,gen}} (GeV)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.4, 1.3)

    ut.set_margin_lbtr(gPad, 0.11, 0.11, 0.02, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#en

#_____________________________________________________________________________
def pitheta():

    #mrad
    tbin = 0.1
    tmin = 0
    tmax = 11

    #inp = "../../analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v6.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx6/maps_basic_v1.root"

    det = "s1_tracks"
    #det = "s2_tracks"

    sel = "is_rec==1 && itrk==1"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", tbin, tmin, tmax, tbin, tmin, tmax)

    tree.Draw("(TMath::Pi()-rec_theta)*1e3:(TMath::Pi()-true_el_theta)*1e3 >> hxy", sel)
    #tree.Draw("(TMath::Pi()-rec_theta)*1e3:(TMath::Pi()-true_el_theta)*1e3 >> hxy", "is_rec==1")

    ytit = "Reconstructed #it{#pi-#theta_{e}} (mrad)"
    xtit = "Generated true #it{#pi-#theta_{e,gen}} (mrad)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.9, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.12, 0.03, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#pitheta

#_____________________________________________________________________________
def phi():

    #GeV
    pbin = 0.1
    pmin = -TMath.Pi()-0.1
    pmax = TMath.Pi()+0.1

    #inp = "../../analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v6.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx6/maps_basic_v1.root"

    det = "s1_tracks"
    #det = "s2_tracks"

    sel = "is_rec==1 && itrk==1"
    sel += "&&(TMath::Pi()-rec_theta)>1e-3"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", pbin, pmin, pmax, pbin, pmin, pmax)

    #tree.Draw("rec_el_phi:true_el_phi >> hxy", sel)
    tree.Draw("rec_phi:true_el_phi >> hxy", sel)

    ytit = "Reconstructed #it{#phi_{e}} (rad)"
    xtit = "Generated true #it{#phi_{e,gen}} (rad)"
    ut.put_yx_tit(hxy, ytit, xtit, 1.9, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.03, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.85, 0.24, 0.1, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", "#pi-#theta_{#it{e},rec} > 1 mrad", "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#phi

#_____________________________________________________________________________
def lQ2():

    #GeV^2
    qbin = 0.1
    qmin = -8
    qmax = -1

    #inp = "../../analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v6.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx6/maps_basic_v1.root"

    det = "s1_tracks"
    lab = "Tagger 1"

    #det = "s2_tracks"
    #lab = "Tagger 2"

    sel = "is_rec==1 && itrk==1"
    #sel = "(TMath::Pi()-rec_theta)>1e-3"

    infile = TFile.Open(inp)
    tree = infile.Get(det)

    can = ut.box_canvas()

    hxy = ut.prepare_TH2D("hxy", qbin, qmin, qmax, qbin, qmin, qmax)

    #rec_Q2 = "(2.*18*rec_E*(1.-TMath::Cos(TMath::Pi()-rec_theta)))"
    #tree.Draw("TMath::Log10("+rec_Q2+"):TMath::Log10(true_Q2) >> hxy", sel)
    #tree.Draw("TMath::Log10(rec_Q2):TMath::Log10(true_Q2) >> hxy", "is_rec==1")
    tree.Draw("TMath::Log10(rec_Q2):TMath::Log10(true_Q2) >> hxy", sel)

    ytit = "Reconstructed electron  log_{10}(Q^{2})"
    xtit = "Generated true  log_{10}(Q^{2})"
    ut.put_yx_tit(hxy, ytit, xtit, 1.9, 1.3)

    ut.set_margin_lbtr(gPad, 0.14, 0.1, 0.03, 0.11)

    hxy.SetMinimum(0.98)
    hxy.SetContour(300)

    gPad.SetLogz()

    gPad.SetGrid()

    leg = ut.prepare_leg(0.15, 0.85, 0.24, 0.1, 0.035) # x, y, dx, dy, tsiz
    leg.AddEntry("", lab, "")
    leg.Draw("same")

    #ut.invert_col(rt.gPad)
    can.SaveAs("01fig.pdf")

#lQ2

#_____________________________________________________________________________
def rec_lQ2():

    #GeV^2
    qbin = 0.1
    qmin = -11
    qmax = -1

    #inp = "../../analysis_tasks/ini/ana.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx3/maps_basic_v10.root"
    #inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx4/maps_basic_v6.root"
    inp = "/home/jaroslav/sim/lmon/data/taggers/tag5dx6/maps_basic_v1.root"

    sel = "itrk==1"
    #sel = "itrk!=1"

    hx1 = make_h1(inp, "s1_tracks", "TMath::Log10(rec_Q2)", qbin, qmin, qmax, sel)
    hx2 = make_h1(inp, "s2_tracks", "TMath::Log10(rec_Q2)", qbin, qmin, qmax, sel)

    #plot
    plt.style.use("dark_background")
    col = "lime"
    #col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(hx1[0], hx1[1], "-", color="orange", lw=1)
    plt.plot(hx2[0], hx2[1], "-", color="red", lw=1)

    ax.set_xlabel("log10(Q2) (GeV2)")
    ax.set_ylabel("Normalized counts")

    ax.set_yscale("log")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#rec_lQ2

#_____________________________________________________________________________
def compare_lQ2():

    prefix = "/home/jaroslav/sim/lmon/data/taggers/"

    #input, color, rate in MHz by taggers/hit_rate.py
    #Tagger 1
    inp_s1 = [\
        {"in": "tag4ax2/tag_rec_pass5.root", "col": "red", "rate": 19.1405, "lab": "Bremsstrahlung", "tree": "s1_rec"}, \
        {"in": "tag4a/tag_rec_pass5.root", "col": "blue", "rate": 0.002905, "lab": "Quasi-real", "tree": "s1_rec"}, \
        {"in": "tag4ax3/tag_rec_pass5.root", "col": "orange", "rate": 0.004053, "lab": "Pythia6", "tree": "s1_rec"} \
    ]
    #Tagger 2
    inp_s2 = [\
        {"in": "tag4ax2/tag_rec_pass5.root", "col": "red", "rate": 22.0011, "lab": "Bremsstrahlung", "tree": "s2_rec"}, \
        {"in": "tag4a/tag_rec_pass5.root", "col": "blue", "rate": 0.005642, "lab": "Quasi-real", "tree": "s2_rec"}, \
        {"in": "tag4ax3/tag_rec_pass5.root", "col": "orange", "rate": 0.008656, "lab": "Pythia6", "tree": "s2_rec"} \
    ]

    #tnam = "Tagger 1"
    #inp = inp_s1

    tnam = "Tagger 2"
    inp = inp_s2

    #range along x in log_10(Q^2) (GeV^2)
    xmin = -10
    xmax = -1
    xbin = 0.1

    sel = ""
    #sel = "(TMath::Pi()-rec_theta)>1e-3"

    #plot
    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    fig.set_size_inches(5, 5)
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    leg = legend()
    leg.add_entry(leg_txt(), tnam)

    #Q^2 formula
    rec_Q2 = "(2.*18*rec_E*(1.-TMath::Cos(TMath::Pi()-rec_theta)))"

    #inputs loop
    for i in inp:

        infile = TFile.Open(prefix+i["in"])
        tree = infile.Get(i["tree"])

        hx = ut.prepare_TH1D("hx_"+i["col"], xbin, xmin, xmax)
        tree.Draw("TMath::Log10("+rec_Q2+") >> hx_"+i["col"], sel)
        ut.norm_to_integral(hx, i["rate"])

        xp, yp = ut.h1_to_arrays(hx)
        leg.add_entry(leg_lin(i["col"]), i["lab"])

        plt.plot(xp, yp, "-", color=i["col"], lw=1)

    ax.set_xlabel("Reconstructed log$_{10}(Q^2)$ (GeV$^2$)")
    ax.set_ylabel("Counts normalized to event rate in MHz")

    ax.set_yscale("log")

    #plt.xticks(ax.get_xticks()[1:-1], ["$10^{"+"{0:.0f}".format(i+6)+"}$" for i in ax.get_xticks()[1:-1]])

    leg.draw(plt, col)

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#compare_lQ2

#_____________________________________________________________________________
def make_h1(infile, tnam, val, xbin, xmin, xmax, sel=""):

    inp = TFile.Open(infile)
    tree = inp.Get(tnam)

    #tree.Print()

    hx = ut.prepare_TH1D("hx", xbin, xmin, xmax)
    tree.Draw(val+" >> hx", sel)
    #ut.norm_to_integral(hx, 1.)

    return ut.h1_to_arrays(hx)

#make_h1

#_____________________________________________________________________________
def set_axes_color(ax, col):

    ax.xaxis.label.set_color(col)
    ax.yaxis.label.set_color(col)
    ax.tick_params(which = "both", colors = col)
    ax.spines["bottom"].set_color(col)
    ax.spines["left"].set_color(col)
    ax.spines["top"].set_color(col)
    ax.spines["right"].set_color(col)

#set_axes_color

#_____________________________________________________________________________
def set_grid(px, col="lime"):

    px.grid(True, color = col, linewidth = 0.5, linestyle = "--")

#set_grid

#_____________________________________________________________________________
class legend:
    def __init__(self):
        self.items = []
        self.data = []
    def add_entry(self, i, d):
        self.items.append(i)
        self.data.append(d)
    def draw(self, px, col=None, **kw):
        leg = px.legend(self.items, self.data, **kw)
        if col != None:
            px.setp(leg.get_texts(), color=col)
            if col != "black":
                leg.get_frame().set_edgecolor("orange")
        return leg

#_____________________________________________________________________________
def leg_lin(col, sty="-"):
    return Line2D([0], [0], lw=2, ls=sty, color=col)

#_____________________________________________________________________________
def leg_txt():
    return Line2D([0], [0], lw=0)

#_____________________________________________________________________________
def leg_dot(fig, col, siz=8):
    return Line2D([0], [0], marker="o", color=fig.get_facecolor(), markerfacecolor=col, markersize=siz)

#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()




