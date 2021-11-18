
from ctypes import c_double

import ROOT as rt
from ROOT import TVector2, TGraph, TLatex

#_____________________________________________________________________________
class segment:
    #_____________________________________________________________________________
    def __init__(self, nam, geo):

        self.dx = geo.GetD(nam, "dx") # mm
        self.dy = geo.GetD(nam, "dy") # mm
        self.dz = geo.GetD(nam, "dz") # mm

        xpos = c_double(0)
        ypos = c_double(0)
        geo.GetOptD(nam, "xpos", xpos) # mm
        geo.GetOptD(nam, "ypos", ypos) # mm
        self.xpos = xpos.value
        self.ypos = ypos.value
        self.zpos = geo.GetD(nam, "zpos") # mm

        theta = c_double(0)
        geo.GetOptD(nam, "theta", theta) # rad
        self.theta = theta.value

        self.fill_style = 1000
        self.line_col = rt.kRed
        self.fill_col = rt.kCyan+1
        self.line_width = 1

        self.label = ""

        #draw as projection in x or y
        self.y_project = False

    #_____________________________________________________________________________
    def draw(self):

        #horizontal and vertical 1/2 size
        hsiz = self.dz/2.
        if not self.y_project:
            vsiz = self.dx/2. # vertical is x
        else:
            vsiz = self.dy/2. # vertical is y

        #horizontal and vertical center
        hcen = self.zpos
        if not self.y_project:
            vcen = self.xpos # vertical is x
        else:
            vcen = self.ypos # vertical is y

        #print(hsiz, vsiz, hcen, vcen)

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
        self.gbox.SetLineWidth(self.line_width)
        self.gbox.SetFillStyle(self.fill_style)
        self.gbox.SetFillColor(self.fill_col)

        for i in range(len(points)):
            self.gbox.SetPoint(i, points[i].X(), points[i].Y())

        self.gbox.Draw("lfsame")

        #label
        if self.label == "": return

        #label below the segment
        if vcen < -1.:
            align = 32
            vlab = (vcen-vsiz)*1.1

        #label above the segment
        else:
            align = 12
            vlab = (vcen+vsiz)*1.1

        self.glabel = TLatex(hcen, vlab, self.label)
        self.glabel.SetTextSize(0.03)
        #self.glabel.SetTextSize(0.02)
        self.glabel.SetTextAngle(90)
        self.glabel.SetTextAlign(align)
        self.glabel.Draw("same")
























