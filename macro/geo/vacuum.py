
import ROOT as rt
from ROOT import TVector2, TGraph

#_____________________________________________________________________________
class vacuum:
    #_____________________________________________________________________________
    def __init__(self, geo):

        self.geo = geo
        self.points = []

        self.fill_style = 3207
        self.line_col = rt.kBlue
        self.fill_col = rt.kGreen-2
        self.line_width = 1

    #_____________________________________________________________________________
    def add_point(self, nam, hnam, vnam, mult2=1.):

        self.points.append( TVector2(self.geo.GetD(nam, hnam), mult2*self.geo.GetD(nam, vnam)) )

    #_____________________________________________________________________________
    def add_point_2(self, hnam, vnam):

        hnam = hnam.split(".")
        vnam = vnam.split(".")

        self.points.append( TVector2(self.geo.GetD(hnam[0], hnam[1]), self.geo.GetD(vnam[0], vnam[1])) )

    #_____________________________________________________________________________
    def draw(self):

        #last point same as the first
        self.points.append( self.points[0] )

        #export points to the graph
        self.gbox = TGraph(len(self.points))
        self.gbox.SetLineColor(self.line_col)
        self.gbox.SetLineWidth(self.line_width)
        self.gbox.SetFillStyle(self.fill_style)
        self.gbox.SetFillColor(self.fill_col)

        for i in range(len(self.points)):
            self.gbox.SetPoint(i, self.points[i].X(), self.points[i].Y())

        self.gbox.Draw("lfsame")














