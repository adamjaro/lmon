
#spectrometer acceptance

from ROOT import TF1

#_____________________________________________________________________________
class spec_acc:
    #_____________________________________________________________________________
    def __init__(self, l=8550., field=0.25, ymin=42., ymax=252.):

        #magnet and spectrometer
        self.field = field # T, magnet field
        self.mlen = 0.6 # m, magnet length along z
        self.length = l # mm, distance from magnet to spectrometer detectors

        pT = 0.3*self.field*self.mlen # GeV

        #detector positions, mm
        self.y_min = ymin
        self.y_max = ymax

        #range for functions
        self.func_min = 2
        self.func_max = 21

        #up acceptance
        self.eq_12_up_min = TF1("eq_12_up_min", "[0]*[1]/([2]*x)", self.func_min, self.func_max, 3)
        self.eq_12_up_min.SetParameter(0, self.length)
        self.eq_12_up_min.SetParameter(1, pT)
        self.eq_12_up_min.SetParameter(2, self.y_min)

        self.eq_12_up_max = TF1("eq_12_up_max", "[0]*[1]/([2]*x)", self.func_min, self.func_max, 3)
        self.eq_12_up_max.SetParameter(0, self.length)
        self.eq_12_up_max.SetParameter(1, pT)
        self.eq_12_up_max.SetParameter(2, self.y_max)

        #down acceptance
        self.eq_12_down_max = TF1("eq_12_down_max", "1-[0]*[1]/(x*[2])", self.func_min, self.func_max, 3)
        self.eq_12_down_max.SetParameter(0, self.length)
        self.eq_12_down_max.SetParameter(1, pT)
        self.eq_12_down_max.SetParameter(2, self.y_min)

        self.eq_12_down_min = TF1("eq_12_down_min", "1-[0]*[1]/(x*[2])", self.func_min, self.func_max, 3)
        self.eq_12_down_min.SetParameter(0, self.length)
        self.eq_12_down_min.SetParameter(1, pT)
        self.eq_12_down_min.SetParameter(2, self.y_max)

        #acceptance parametrization
        self.scale = 1. # scale for conversion probability and possible energy threshold
        self.acc_func = TF1("acc_func", self.acc_calc, self.func_min, self.func_max)
        self.acc_func.SetNpx(300)

    #_____________________________________________________________________________
    def acc_calc(self, par):

        #acceptance function
        Eg = par[0]

        lower1 = self.eq_12_up_max.Eval(Eg)
        lower2 = self.eq_12_down_max.Eval(Eg)

        #lower and upper limit for the acceptance
        if lower1 > lower2:
            lower = lower1
        else:
            lower = lower2

        upper1 = self.eq_12_down_min.Eval(Eg)
        upper2 = self.eq_12_up_min.Eval(Eg)

        if upper1 < upper2:
            upper = upper1
        else:
            upper = upper2

        if upper < lower: return 0

        return (upper - lower)*self.scale





