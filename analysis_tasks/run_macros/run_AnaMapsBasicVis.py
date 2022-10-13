#!/usr/bin/python3

import sys
from ctypes import CDLL, c_char_p, c_double, byref

import npyscreen as npy

import ROOT as rt
from ROOT import TEveManager, TEvePointSet, gEve, TEveLine

#_____________________________________________________________________________
class gui(npy.NPSApp):

    #text-mode graphical user interface with npyscreen

    #_____________________________________________________________________________
    def __init__(self, **kws):
        npy.NPSApp.__init__(self, **kws)

        #analysis configuration from command line
        config = get_config()

        #analysis task
        self.lib = CDLL("liblmonAnalysisTasks.so")
        self.task = self.lib.make_AnaMapsBasicVis( c_char_p(bytes(config, "utf-8")) )

        #make the visualization
        TEveManager.Create()

        #current event
        self.iev = 0

    #init

    #_____________________________________________________________________________
    def main(self):

        #main frame for the gui
        frame = npy.Form(name="Tagger event display", lines=19, columns=80)

        #event
        nav_x = 2
        nav_y = 2
        frame.add(npy.BoxBasic, name="Event navigation", editable=False, relx=nav_x, rely=nav_y, width=36, height=6)
        frame.add(npy.ButtonPress, name="Next", when_pressed_function=self.next_event, relx=nav_x+1, rely=nav_y+1)
        frame.add(npy.ButtonPress, name="Previous", when_pressed_function=self.previous_event, relx=nav_x+1, rely=nav_y+2)
        self.set_evt = frame.add(npy.TitleText, name="Set event", relx=nav_x+3, rely=nav_y+3, max_width=20)
        self.set_evt.value = "0"
        self.set_apply = frame.add(npy.ButtonPress, name="Apply", when_pressed_function=self.set_event, relx=nav_x+23, rely=nav_y+3)

        #clear and start
        npy.blank_terminal()
        frame.edit()

    #main

    #_____________________________________________________________________________
    def set_event(self):

        self.lib.task_AnaMapsBasicVis_set_event(self.task, int(self.set_evt.value))
        self.next_event()

    #set_event

    #_____________________________________________________________________________
    def next_event(self):

        self.iev = self.lib.task_AnaMapsBasicVis_next_event(self.task)
        self.draw_event()

    #_____________________________________________________________________________
    def previous_event(self):

        self.iev = self.lib.task_AnaMapsBasicVis_prev_event(self.task)
        self.draw_event()

    #_____________________________________________________________________________
    def draw_event(self):

        #scene
        gEve.GetGlobalScene().DestroyElements()
        draw_markers()

        #clusters
        ncls0 = self.lib.task_AnaMapsBasicVis_ncls(self.task, 0)
        ncls_planes = [self.lib.task_AnaMapsBasicVis_ncls(self.task, i) for i in range(4)]
        #print("Next event ", ncls0)
        #ncls = ncls0
        ncls = sum(ncls_planes)
        x = c_double(0)
        y = c_double(0)
        z = c_double(0)
        clusters = TEvePointSet(ncls)
        icls = 0
        clusters.SetName("Clusters")
        clusters.SetMarkerColor(rt.kYellow)
        clusters.SetMarkerStyle(3)
        for iplane in range(4):
            for i in range(ncls_planes[iplane]):
                self.lib.task_AnaMapsBasicVis_cluster(self.task, iplane, i, byref(x), byref(y), byref(z))
                #print(x.value, y.value, z.value)
                clusters.SetPoint(icls, x.value, y.value, z.value)
                icls += 1

        gEve.AddGlobalElement(clusters)

        #tracks
        #print(self.lib.task_AnaMapsBasicVis_ntrk(self.task))
        for i in range( self.lib.task_AnaMapsBasicVis_ntrk(self.task) ):

            #load the track
            x0 = c_double(0)
            y0 = c_double(0)
            slope_x = c_double(0)
            slope_y = c_double(0)
            self.lib.task_AnaMapsBasicVis_track(self.task, i, byref(x0), byref(y0), byref(slope_x), byref(slope_y))

            #print(x0.value, y0.value, slope_x.value, slope_y.value)

            #track line
            zmax = 500. # mm
            xpos = x0.value + zmax*slope_x.value
            ypos = y0.value + zmax*slope_y.value
            xneg = x0.value - zmax*slope_x.value
            yneg = y0.value - zmax*slope_y.value
            track_lin = TEveLine("track_"+str(i), 2)
            track_lin.SetPoint(0, xneg, yneg, -zmax)
            track_lin.SetPoint(1, xpos, ypos, zmax)

            track_lin.SetLineColor(rt.kRed)

            gEve.AddGlobalElement(track_lin)

        #status bar
        stat_str = "Event number: "+str(self.iev)

        gEve.GetStatusBar().SetParts(1)
        gEve.GetStatusBar().AddText(stat_str)
        gEve.GetStatusBar().SetHeight(30)

        gEve.FullRedraw3D(rt.kTRUE)

    #draw_event

#gui

#_____________________________________________________________________________
def draw_markers():

    #tagger station size with overlap
    zmax = 500. # mm
    xmax = 80. # mm

    marker = TEvePointSet(8)
    marker.SetName("Origin marker")
    marker.SetMarkerColor(rt.kGreen)
    marker.SetMarkerStyle(3)
    marker.SetPoint(0, -xmax, -xmax, zmax) # x, y, z
    marker.SetPoint(1, xmax, -xmax, zmax)
    marker.SetPoint(2, xmax, xmax, zmax)
    marker.SetPoint(3, -xmax, xmax, zmax)
    marker.SetPoint(4, -xmax, -xmax, -zmax) # x, y, z
    marker.SetPoint(5, xmax, -xmax, -zmax)
    marker.SetPoint(6, xmax, xmax, -zmax)
    marker.SetPoint(7, -xmax, xmax, -zmax)

    gEve.AddGlobalElement(marker)

#draw_markers

#_____________________________________________________________________________
def get_config():

    #command line options
    args = sys.argv
    if len(args) < 2:
        print("No configuration specified.")
        quit()
    args.pop(0)

    return args.pop(0)

#get_config

#_____________________________________________________________________________
if __name__ == "__main__":

    #gui instance and call to main
    gui = gui()
    gui.run()






















