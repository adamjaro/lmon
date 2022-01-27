
from ctypes import c_double

import ROOT as rt
from ROOT import TVector2, TGraph, TLatex

#_____________________________________________________________________________
class magnet:
    #_____________________________________________________________________________
    def __init__(self, nam, geo):

        r1 = c_double(0)
        geo.GetOptD(nam, "inner_r", r1) # mm
        geo.GetOptD(nam, "r1", r1) # mm
        self.r1 = r1.value

        r2 = c_double(0)
        r2.value = r1.value
        geo.GetOptD(nam, "r2", r2) # mm
        self.r2 = r2.value

        length = c_double(0)
        geo.GetOptD(nam, "length", length) # mm
        geo.GetOptD(nam, "dz", length) # mm

        self.dz = length.value

        xpos = c_double(0)
        geo.GetOptD(nam, "xpos", xpos) # mm
        self.xpos = xpos.value
        self.zpos = geo.GetD(nam, "zpos") # mm

        theta = c_double(0)
        geo.GetOptD(nam, "theta", theta) # rad
        self.theta = theta.value

        self.fill_style = 1000
        self.line_col = rt.kAzure
        self.fill_col = rt.kOrange
        self.line_width = 2

        self.label = ""

    #_____________________________________________________________________________
    def draw(self):

        #edge points around a closed contour
        points = []
        points.append(TVector2(-self.dz/2., -self.r2))
        points.append(TVector2(-self.dz/2., self.r2))
        points.append(TVector2(self.dz/2., self.r1))
        points.append(TVector2(self.dz/2., -self.r1))
        points.append(TVector2(-self.dz/2., -self.r2))

        #rotate and move to center
        pcen = TVector2(self.zpos, self.xpos)
        for i in range(len(points)):
            points[i] = points[i].Rotate(self.theta) + pcen

        #export points to the graph
        self.gbox = TGraph(len(points))
        self.gbox.SetLineColor(self.line_col)
        self.gbox.SetLineWidth(self.line_width)
        self.gbox.SetFillStyle(self.fill_style)
        self.gbox.SetFillColor(self.fill_col)

        for i in range(len(points)):
            self.gbox.SetPoint(i, points[i].X(), points[i].Y())

        self.gbox.Draw("lfsame")

        #label
        if self.label == "": return

        #label below the magnet
        if self.xpos < -1.:
            align = 32
            vlab = (self.xpos-self.r2)*1.1

        #label above the magnet
        else:
            align = 12
            vlab = (self.xpos+self.r2)*1.1

        self.glabel = TLatex(self.zpos, vlab, self.label)
        self.glabel.SetTextSize(0.03)
        self.glabel.SetTextAngle(90)
        self.glabel.SetTextAlign(align)
        self.glabel.Draw("same")




















