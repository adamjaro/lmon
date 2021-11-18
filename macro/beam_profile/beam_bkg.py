#!/usr/bin/python3

import sys
sys.path.append('../')

import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from scipy.interpolate import CubicHermiteSpline, interp1d

import plot_utils as ut

#_____________________________________________________________________________
def main():

    iplot = 0

    func = {}
    func[0] = rate
    func[1] = interp_sigma
    func[2] = interp_divergence
    func[3] = interp_pressure

    func[iplot]()

#_____________________________________________________________________________
def rate():

    # p = nRT

    #range in z (m), None for all
    zmin = None
    #zmin = 5.
    zmax = None

    #cross section in mb
    #sigma = 150.969 # mb
    sigma = 537.583 # mb, E_gamma > 100 keV

    #beam current in Amps
    beam_current = 2.5 # A

    #spacing in z
    zbin = 0.2 # m
    #zbin = 0.05 # m

    #temperature
    T = 293.15 # K

    #Boltzmann constant
    Rb = 1.38064852e-23 # m^2 kg s^-2 K^-1

    #electron charge in Coulomb
    charge = 1.60218e-19 # C

    #current in electrons per second
    I = beam_current/charge

    #input pressure data
    xls = load_pressure()

    #invert to detector coordinates
    xls[1] = -1.*xls[1]

    #linear interpolation for the pressure, in mbar
    pressure = interp1d(xls[1], xls[2], kind="linear")

    #intervals along z
    if zmin is None:
        zmin = xls[1][ xls[1].index[0] ]
    if zmax is None:
        zmax = xls[1][ xls[1].index[-1] ]
    print("Range:", zmin, zmax)

    hz = ut.prepare_TH1D("hz", zbin, zmin, zmax)

    #calculate the rate, ignoring last bin which might reach past the data
    xz_plot = []
    rate_plot = []
    total_rate = 0.;
    for ibin in range(1,hz.GetNbinsX()):

        #surface density in m^-2
        dens = hz.GetBinWidth(ibin)*proton_density( Rb, T, pressure(hz.GetBinCenter(ibin)) )

        #sigma to barn and to m^-2
        R = 1e-3*1e-28*sigma*I*dens

        #position in m
        #xz.append( hz.GetBinCenter(ibin) )
        xz_plot.append( hz.GetBinLowEdge(ibin) )
        xz_plot.append( hz.GetBinLowEdge(ibin) + hz.GetBinWidth(ibin) )

        #rate in kHz
        rate_plot.append( R*1e-3 )
        rate_plot.append( R*1e-3 )
        total_rate += R*1e-3

    print("Total rate (kHz):", total_rate)

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    plt.plot(xz_plot, rate_plot, "-", color="blue", lw=1)

    ax.set_xlabel("$z$ (m)")
    ax.set_ylabel("Event rate in 20 cm length along $z$ (kHz)")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#rate

#_____________________________________________________________________________
def interp_sigma():

    #beam emittance
    eps_x = 20e-9 # m
    eps_y = 1.3e-9 # m

    df = load_esr()

    #range with pressure data
    df = df.query("s>-15 and s<10")

    interp_x = CubicHermiteSpline(df["s"], df["beta_x"], -2*df["alpha_x"])
    interp_y = CubicHermiteSpline(df["s"], df["beta_y"], -2*df["alpha_y"])

    xs = np.linspace(df["s"][ df["s"].index[0] ], df["s"][ df["s"].index[-1] ], 300)

    print("range:", xs[0], xs[-1])

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    #plot data
    sigma_x = []
    sigma_y = []
    for i in xs:
        sigma_x.append( get_beam_sigma(eps_x, interp_x(i)) )
        sigma_y.append( get_beam_sigma(eps_y, interp_y(i)) )

    #plot in detector coordinates
    plt.plot(-1*df["s"], get_beam_sigma(eps_x, df["beta_x"]), "o", markersize=4, color="blue", lw=1)
    plt.plot(-1*xs, sigma_x, "-", color="blue", lw=1)

    plt.plot(-1*df["s"], get_beam_sigma(eps_y, df["beta_y"]), "o", markersize=4, color="red", lw=1)
    plt.plot(-1*xs, sigma_y, "-", color="red", lw=1)

    leg = legend()
    leg.add_entry(leg_txt(), "$E_e$ = 10 GeV")
    leg.add_entry(leg_lin("blue"), "$\sigma_x$")
    leg.add_entry(leg_lin("red"), "$\sigma_y$")
    leg.draw(plt, col)

    ax.set_xlabel("$z$ (m)")
    ax.set_ylabel("Beam $\sigma$ (mm)")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#interp_sigma

#_____________________________________________________________________________
def interp_divergence():

    #beam emittance
    eps_x = 20e-9 # m
    eps_y = 1.3e-9 # m

    df = load_esr()

    #range with pressure data
    df = df.query("s>-15 and s<10")

    interp_x = interp1d(df["s"], get_divergence(eps_x, df["alpha_x"], df["beta_x"]), kind="linear")
    interp_y = interp1d(df["s"], get_divergence(eps_y, df["alpha_y"], df["beta_y"]), kind="linear")

    xs = np.linspace(df["s"][ df["s"].index[0] ], df["s"][ df["s"].index[-1] ], 300)

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    #plot data
    div_x = [interp_x(i) for i in xs]
    div_y = [interp_y(i) for i in xs]

    #plot in detector cordinates
    plt.plot(-1*df["s"], get_divergence(eps_x, df["alpha_x"], df["beta_x"]), "o", markersize=4, color="blue", lw=1)
    plt.plot(-1*df["s"], get_divergence(eps_y, df["alpha_y"], df["beta_y"]), "o", markersize=4, color="red", lw=1)
    plt.plot(-1*xs, div_x, "-", color="blue", lw=1)
    plt.plot(-1*xs, div_y, "-", color="red", lw=1)

    leg = legend()
    leg.add_entry(leg_txt(), "$E_e$ = 10 GeV")
    leg.add_entry(leg_lin("blue"), r"$\sigma_{\theta x}$")
    leg.add_entry(leg_lin("red"), r"$\sigma_{\theta y}$")
    leg.draw(plt, col)

    ax.set_xlabel("$z$ (m)")
    ax.set_ylabel(r"Angular divergence $\sigma_\theta$ ($\mu$rad)")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#interp_divergence

#_____________________________________________________________________________
def interp_pressure():

    xls = load_pressure()

    xs = np.linspace(xls[1][ xls[1].index[0] ], xls[1][ xls[1].index[-1] ], 300)

    interp = interp1d(xls[1], xls[2], kind="linear")

    #plt.style.use("dark_background")
    #col = "lime"
    col = "black"

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    set_axes_color(ax, col)
    set_grid(plt, col)

    #plot data
    pressure = [interp(i) for i in xs]

    #plot in detector coordinates
    plt.plot(-1*xls[1], xls[2], "o", markersize=3, color="blue", lw=1)
    plt.plot(-1*xs, pressure, "-", color="blue", lw=1)

    ax.set_xlabel("$z$ (m)")
    ax.set_ylabel("Pressure (mbar)")

    fig.savefig("01fig.pdf", bbox_inches = "tight")
    plt.close()

#interp_pressure

#_____________________________________________________________________________
def proton_density(Rb, T, p):

    #proton density as number per m^3 at a given temperature T, pressure p
    #and Boltzmann constant Rb

    #multiply by 2 for two protons in hydrogen molecule
    #pressure in mbar, convert to Pa
    return 2.*1e2*p/(Rb*T)

#proton_density

#_____________________________________________________________________________
def get_beam_sigma(eps, beta):

    #beam sigma in mm

    return 1e3*np.sqrt(eps*beta)

#get_3sigma

#_____________________________________________________________________________
def get_divergence(eps, alpha, beta):

    #angular divergence in micro rad

    return 1e6*np.sqrt( eps*( (1. + alpha**2)/beta ) )

#get_3sigma

#_____________________________________________________________________________
def load_esr():

    #input lattice
    #inp = open("/home/jaroslav/sim/lattice/esr/esr-ir6-275-18.txt", "r")
    inp = open("/home/jaroslav/sim/lattice/esr/esr-ir6-100-10.txt", "r")

    #lattice dataframe
    col = ["name", "key", "s", "length", "angle", "x_pitch", "magnet_x", "magnet_z", "magnet_theta",\
        "orbit_x", "orbit_z", "orbit_theta", "dispersion", "dispersion_derivative", "beta_x", "alpha_x",\
        "beta_y", "alpha_y", "field", "gradient"]
    val = []

    #skip file header
    for i in range(3): inp.readline()

    #load the lattice
    while(True):
        line = inp.readline()
        if(len(line) == 0): break

        lin = line.split()

        #IP6 marker is identical to the drift before
        if lin[0] == "IP6": continue

        #name and key as string, values as float
        for i in range(len(lin)):
            if i < 2:
                lin[i] = str(lin[i])
            else:
                lin[i] = float(lin[i])

        val.append( lin )

    df = DataFrame(val, columns=col)

    return df

#load_esr

#_____________________________________________________________________________
def load_pressure():

    xls = pd.read_excel("/home/jaroslav/sim/lattice/chamber/Detector_chamber_210813.xlsx", sheet_name="H2 only, 10000Ahrs"\
        , usecols="B,C", skiprows=12, nrows=100, index_col=None, header=None)

    return xls

#load_pressure

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

    main()


