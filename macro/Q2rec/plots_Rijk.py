#!/usr/bin/python

from ROOT import gROOT, gStyle, TFile, gPad, TH1D, TPad, TCanvas
from ROOT import TLatex

from rmat import rmat

import sys
sys.path.append('../')
import plot_utils as ut

#_____________________________________________________________________________
def main():

    #infile = "rmat_s1.root"
    #infile = "rmat_s2.root"
    #infile = "../../data/qr/rmat_s1_qr_18x275_Qf_beff2_100Mevt.root"
    #infile = "../../data/qr/rmat_s2_qr_18x275_Qf_beff2_100Mevt.root"
    #infile = "../../data/qr/rmat_s1_qr_18x275_Qf_beff2_xy5_100Mevt.root"
    #infile = "../../data/qr/rmat_s2_qr_18x275_Qf_beff2_xy5_100Mevt.root"
    #infile = "../../data/uni/rmat_s1_uni_el_e2p1_18p2_mlt1p7_5p3_beff2_5Mevt.root"
    #infile = "../../data/uni/rmat_s2_uni_el_e2p1_18p2_mlt1p7_5p3_beff2_5Mevt.root"
    #infile = "../../data/uni/rmat_s1_uni_el_e2p1_18p2_mlt1p7_5p3_beff2_200Mevt.root"
    infile = "../../data/uni/rmat_s2_uni_el_e2p1_18p2_mlt1p7_5p3_beff2_200Mevt.root"

    #Rijk reconstruction matrix
    mat = rmat(infile=infile)

    #print mat.hEi

    plot_mlt(mat)

#_____________________________________________________________________________
def plot_mlt(mat):

    can = TCanvas("can", "can", 768, 768)
    gStyle.SetOptStat("")
    gStyle.SetPalette(1)
    gStyle.SetLineWidth(2)
    gStyle.SetPadTickY(1)

    nx = 3
    ny = 4

    #nx = 2
    #ny = 2

    theta_min = 1.8
    #theta_max = 4.9
    #theta_max = 5.2
    theta_max = 4.3

    #theta_min = 2+1e-3
    #theta_max = 4.5-1e-3
    #theta_max = 4-1e-3

    lmgg = 0.17
    rmgg = 0.21
    bmgg = 0.17
    tmgg = 0.03

    tsiz = 0.07

    ytit = "Vertical #it{y} (mm)"
    yofs = 1.2

    xtit = "Horizontal #it{x} (mm)"
    xofs = 1.2

    ztit = "Mean polar angle as  -log_{10}(#theta_{e})"
    zofs = 1.1

    ijmap = {}
    ii = 1
    dx = 1./nx
    dy = 1./ny
    pads = []
    for i in xrange(ny):
        for j in xrange(nx):

            ijmap[ii] = (i, j)

            print ii, i, j

            pnam = "pad_"+str(ii)
            pads.append(TPad(pnam, pnam, j*dx, 1-(i+1)*dy, (j+1)*dx, 1-i*dy))
            pads[len(pads)-1].Draw()

            ii += 1

    for i in xrange(1,nx*ny+1):

        pads[i-1].cd()

        hx = mat.tjks[i].hTjk

        hx.SetTitle("")

        ut.set_H1_text_size(hx, tsiz)
        hx.SetTitleSize(tsiz, "Z")
        hx.SetLabelSize(tsiz, "Z")

        hx.SetMinimum(theta_min)
        hx.SetMaximum(theta_max)

        lmg = lmgg
        bmg = bmgg
        tmg = tmgg
        rmg = rmgg

        ip = ijmap[i][1]
        jp = ijmap[i][0]

        if ip < nx-1:
            hx.GetZaxis().SetTickLength(0)

        if ip == 0 and jp == 0:
            hx.SetYTitle(ytit)
            hx.SetTitleOffset(yofs, "Y")

        if jp == ny-1 and ip == nx-1:
            hx.SetXTitle(xtit)
            hx.SetTitleOffset(xofs, "X")

        if ip == nx-1 and jp == 0:
            hx.SetZTitle(ztit)
            hx.SetTitleOffset(zofs, "Z")

        if ip == 0: rmg = 0

        if ip > 0 and ip < nx-1:
            lmg = 0
            rmg = 0

        if ip == nx-1: lmg = 0

        if jp == 0: bmg = 0
        if jp == ny-1: tmg = 0
        if jp > 0 and jp < ny-1:
            bmg = 0
            tmg = 0

        ut.set_margin_lbtr(gPad, lmg, bmg, tmg, rmg)

        #gPad.SetLogz()

        gPad.SetGrid()

        hx.SetContour(300)
        #hx.SetContour(100)
        hx.Draw("colz")

        #energy label
        hEn = mat.hEi
        emin = hEn.GetBinLowEdge(i)
        emax = hEn.GetBinLowEdge(i)+hEn.GetBinWidth(i)
        eminf = "{0:.2f}".format(emin)
        emaxf = "{0:.2f}".format(emax)
        desc = TLatex()
        desc.SetTextSize(0.075) # tsiz
        etit = "#it{i}: "+str(i)+",  "+eminf+" < #it{E}_{e} < "+emaxf+" GeV"
        etit = "#color[2]{"+etit+"}"
        #desc.DrawLatex(380, 80, etit)
        desc.DrawLatex(-180, 150, etit)
        #desc.DrawLatex(-140, 80, etit)

        ut.invert_col(gPad)


    can.SaveAs("01fig.pdf")

#plot_mlt



#_____________________________________________________________________________
if __name__ == "__main__":

    gROOT.SetBatch()
    gStyle.SetPadTickX(1)
    gStyle.SetFrameLineWidth(2)

    main()













