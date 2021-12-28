
#angles as mlt at positions in 'j' and 'k' for a given 'i'
#
# mlt = T = -log_10(pi-true_el_theta)

from ROOT import TH2D, TH3D, TMath, TH1D

#_____________________________________________________________________________
class tjk:
    #_____________________________________________________________________________
    def __init__(self, i, cf=None, inp=None):

        #names for h2 and h3
        self.namXYT = "hXYTjk_"+str(i)
        self.namT = "hTjk_"+str(i)

        if cf is not None:
            self.init_create(cf)

        if inp is not None:
            self.init_load(inp)

    #__init__

    #_____________________________________________________________________________
    def init_create(self, cf):

        #create the 'j' and 'k' components at a given 'i'

        #bins in x, y and mlt
        nx, xmax = self.get_nbins(cf("xybin"), cf("xmin"), cf("xmax"))
        ny, ymax = self.get_nbins(cf("xybin"), cf("ymin"), cf("ymax"))
        nt, tmax = self.get_nbins(cf("tbin"), cf("tmin"), cf("tmax"))
        xmin = cf("xmin")
        ymin = cf("ymin")
        tmin = cf("tmin")

        #mlt in x and y at 'j' and 'k'
        self.hXYTjk = TH3D(self.namXYT, self.namXYT, nx, xmin, xmax, ny, ymin, ymax, nt, tmin, tmax)

        #mean of mlt in x and y at 'j' and 'k'
        self.hTjk = TH2D(self.namT, self.namT, nx, xmin, xmax, ny, ymin, ymax)

        #underflow and overflow in x, y and mlt
        self.hX = TH1D("hX_"+self.namXYT, "hX", nx, xmin, xmax)
        self.hY = TH1D("hY_"+self.namXYT, "hY", ny, ymin, ymax)
        self.hT = TH1D("hT_"+self.namXYT, "hT", nt, tmin, tmax)

    #init_create

    #_____________________________________________________________________________
    def fill(self, x, y, mlt):

        #fill entry for a given x, y and mlt

        self.hXYTjk.Fill(x, y, mlt)

        self.hX.Fill(x)
        self.hY.Fill(y)
        self.hT.Fill(mlt)


    #_____________________________________________________________________________
    def make_proj(self):

        #projection for mean mlt at each 'j' and 'k'

        for j in range(1, self.hXYTjk.GetNbinsX()+1):
            for k in range(1, self.hXYTjk.GetNbinsY()+1):

                pnam = "projXYT_"+str(j)+"_"+str(k)
                hproj = self.hXYTjk.ProjectionZ(pnam, j, j, k, k)

                #print("  ", j, k, hproj.GetMean())

                self.hTjk.SetBinContent(j, k, hproj.GetMean())
                self.hTjk.SetBinError(j, k, hproj.GetMeanError())

    #make_proj

    #_____________________________________________________________________________
    def get_nbins(self, binsiz, xmin, xmax):

        #number of bins for a given bin size

        nbins = int(TMath.Ceil( (xmax-xmin)/binsiz )) #round-up value
        xmax = xmin + float(binsiz*nbins) # move max up to pass the bins

        return nbins, xmax

    #get_nbins

    #_____________________________________________________________________________
    def print_uo(self):

        #underflow and overflow

        print("  X_"+self.namT+":", self.hX.GetEntries(), self.hX.GetBinContent(0), self.hX.GetBinContent(self.hX.GetNbinsX()+1))
        print("  Y_"+self.namT+":", self.hY.GetEntries(), self.hY.GetBinContent(0), self.hY.GetBinContent(self.hY.GetNbinsX()+1))
        print("  T_"+self.namT+":", self.hT.GetEntries(), self.hT.GetBinContent(0), self.hT.GetBinContent(self.hT.GetNbinsX()+1))

    #_____________________________________________________________________________
    def write(self):

        #write the individual components

        self.hXYTjk.Write()
        self.hTjk.Write()

        self.hX.Write()
        self.hY.Write()
        self.hT.Write()


    #_____________________________________________________________________________
    def init_load(self, inp):

        #load the 'j' and 'k' components at a given 'i' from input

        self.hXYTjk = inp.Get(self.namXYT)
        self.hTjk = inp.Get(self.namT)

    #init_load









