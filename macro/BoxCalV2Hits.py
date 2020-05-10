
from ROOT import std

#_____________________________________________________________________________
class BoxCalV2Hits:
    #_____________________________________________________________________________
    def __init__(self, name, tree):

        self.pdg = std.vector(int)()
        self.en = std.vector(float)()
        self.hx = std.vector(float)()
        self.hy = std.vector(float)()
        self.hz = std.vector(float)()

        self.tree = tree

        self.tree.SetBranchAddress(name+"_HitPdg", self.pdg)
        self.tree.SetBranchAddress(name+"_HitEn", self.en)
        self.tree.SetBranchAddress(name+"_HitX", self.hx)
        self.tree.SetBranchAddress(name+"_HitY", self.hy)
        self.tree.SetBranchAddress(name+"_HitZ", self.hz)

    #_____________________________________________________________________________
    def GetPdg(self, ihit):
        return self.pdg.at(ihit)

    #_____________________________________________________________________________
    def GetX(self, ihit):
        return self.hx.at(ihit)

    #_____________________________________________________________________________
    def GetY(self, ihit):
        return self.hy.at(ihit)

    #_____________________________________________________________________________
    def GetZ(self, ihit):
        return self.hz.at(ihit)

    #_____________________________________________________________________________
    def GetEn(self, ihit):
        return self.en.at(ihit)

    #_____________________________________________________________________________
    def GetN(self):
        return self.pdg.size()

    #_____________________________________________________________________________
    def read(self, i):

        self.tree.GetEntry(i)

