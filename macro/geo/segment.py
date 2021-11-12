
from ctypes import c_double

import ROOT as rt
from ROOT import TVector2, TGraph

#_____________________________________________________________________________
class segment:
    #_____________________________________________________________________________
    def __init__(self, nam, geo):

        self.dx = geo.GetD(nam, "dx") # mm
        self.dy = geo.GetD(nam, "dy") # mm
        self.dz = geo.GetD(nam, "dz") # mm

        xpos = c_double(0)
        geo.GetOptD(nam, "xpos", xpos) # mm
        self.xpos = xpos.value
        self.zpos = geo.GetD(nam, "zpos") # mm

        theta = c_double(0)
        geo.GetOptD(nam, "theta", theta) # rad
        self.theta = theta.value

        self.fill_style = 1000
        self.line_col = rt.kBlue
        self.fill_col = rt.kGreen-2

    #_____________________________________________________________________________
    def draw(self):

        #horizontal and vertical 1/2 size
        hsiz = self.dz/2.
        vsiz = self.dx/2.

        #horizontal and vertical center
        hcen = self.zpos
        vcen = self.xpos

        print(hsiz, vsiz, hcen, vcen)

        #edge points around closed contour
        points = []
        points.append(TVector2(-hsiz, -vsiz))
        points.append(TVector2(-hsiz, vsiz))
        points.append(TVector2(hsiz, vsiz))
        points.append(TVector2(hsiz, -vsiz))
        points.append(TVector2(-hsiz, -vsiz))

        #rotate and move to center
        pcen = TVector2(hcen, vcen)
        for i in range(len(points)):
            points[i] = points[i].Rotate(self.theta) + pcen

        #export points to the graph
        self.gbox = TGraph(len(points))
        self.gbox.SetLineColor(self.line_col)
        self.gbox.SetLineWidth(2)
        self.gbox.SetFillStyle(self.fill_style)
        self.gbox.SetFillColor(self.fill_col)

        for i in range(len(points)):
            self.gbox.SetPoint(i, points[i].X(), points[i].Y())

        self.gbox.Draw("lfsame")

























