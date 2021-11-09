
# ParticleCounter hits collection

from ctypes import c_double, c_bool, c_int

from ROOT import std, TVector3, TTree

#_____________________________________________________________________________
class ParticleCounterHits:
    #_____________________________________________________________________________
    def __init__(self, name, tree):

        #hit representation in the tree
        self.pdg = std.vector(int)()
        self.en = std.vector(float)()
        self.hx = std.vector(float)()
        self.hy = std.vector(float)()
        self.hz = std.vector(float)()

        tree.SetBranchAddress(name+"_HitPdg", self.pdg)
        tree.SetBranchAddress(name+"_HitEn", self.en)
        tree.SetBranchAddress(name+"_HitX", self.hx)
        tree.SetBranchAddress(name+"_HitY", self.hy)
        tree.SetBranchAddress(name+"_HitZ", self.hz)

        #interface to the hit
        self.hit = self.Hit(self)

        #counter position for transformation to local coordinates
        self.xpos = 0.
        self.ypos = 0.
        self.zpos = 0.
        self.theta = 0.

    #_____________________________________________________________________________
    def GetHit(self, ihit):

        #get the hit at 'ihit'

        self.hit.pdg = self.pdg.at(ihit)
        self.hit.en = self.en.at(ihit)
        self.hit.x = self.hx.at(ihit)
        self.hit.y = self.hy.at(ihit)
        self.hit.z = self.hz.at(ihit)

        return self.hit

    #_____________________________________________________________________________
    class Hit:
        #implementation for the hit interface
        #_____________________________________________________________________________
        def __init__(self, hits):
            self.pdg = 0 # PDG
            self.en = 0. # GeV
            self.x = 0. # mm
            self.y = 0. # mm
            self.z = 0. # mm

            self.hits = hits

        #_____________________________________________________________________________
        def GlobalToLocal(self):

            #local detector coordinates with rotation theta in x-z plane
            pos = TVector3(self.x-self.hits.xpos, self.y-self.hits.ypos, self.z-self.hits.zpos)
            pos.RotateY(-self.hits.theta)

            self.x = pos.X()
            self.y = pos.Y()
            self.z = pos.Z()

        #_____________________________________________________________________________
        def LocalY(self):

            #local coordinates for the hit with translation only in y

            self.y = self.y - self.hits.ypos

    #_____________________________________________________________________________
    def GetN(self):

        #number of hits in event, all vectors are of the same size

        return self.pdg.size()

    #_____________________________________________________________________________
    def CreateOutput(self, nam):

        #create tree output associated with the hits

        self.otree = TTree(nam, nam)
        self.out_en = c_double(0)
        self.out_x = c_double(0)
        self.out_y = c_double(0)
        self.out_z = c_double(0)
        self.out_pdg = c_int(0)
        self.otree.Branch("en", self.out_en, "en/D")
        self.otree.Branch("x", self.out_x, "x/D")
        self.otree.Branch("y", self.out_y, "y/D")
        self.otree.Branch("z", self.out_z, "z/D")
        self.otree.Branch("pdg", self.out_pdg, "pdg/I")

    #_____________________________________________________________________________
    def FillOutput(self):

        #fill the output tree for the current hit

        self.out_en.value = self.hit.en
        self.out_x.value = self.hit.x
        self.out_y.value = self.hit.y
        self.out_z.value = self.hit.z
        self.out_pdg.value = self.hit.pdg

        self.otree.Fill()

    #direct access:
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











