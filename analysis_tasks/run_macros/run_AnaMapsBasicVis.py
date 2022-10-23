#!/usr/bin/python3

import sys
from ctypes import CDLL, c_char_p, c_double, byref
from math import sqrt

import npyscreen as npy

import ROOT as rt
from ROOT import TEveManager, TEvePointSet, gEve, TEveLine
from ROOT import gStyle, gPad, TLatex

sys.path.append("/home/jaroslav/sim/lmon/macro/")
import plot_utils as ut

#_____________________________________________________________________________
class gui(npy.NPSApp):

    #text-mode graphical user interface with npyscreen

    #_____________________________________________________________________________
    def __init__(self, **kws):
        npy.NPSApp.__init__(self, **kws)

        #analysis configuration from command line
        config = get_config()

        #analysis task
        self.lib = CDLL("liblmonAnalysisTasks.so") # load the library
        self.lib.task_AnaMapsBasicVis_det_nam.restype = c_char_p # to return a string
        self.lib.task_AnaMapsBasicVis_get_max_chi2.restype = c_double # double return type
        self.task = self.lib.make_AnaMapsBasicVis( c_char_p(bytes(config, "utf-8")) ) # task instance

        #make the visualization
        TEveManager.Create()

        #event plots
        gStyle.SetOptStat("")
        gStyle.SetPalette(1)
        gStyle.SetLineWidth(2)
        gStyle.SetPadTickX(1)
        gStyle.SetFrameLineWidth(2)

        #tracks chi^2 and cluster distances
        self.plots_evt = gEve.AddCanvasTab("Event")
        self.plots_evt.Divide(2, 2)

        self.evt_frame = ut.prepare_TH1D("evt_frame", 1, 0, 1)
        self.evt_frame.SetYTitle("")
        self.tracks_chi2 = ut.prepare_TH1D("tracks_chi2", 0.01, 0, 0.5)
        ut.put_yx_tit(self.tracks_chi2, "Counts", "Track #chi^{2}/ndf", 1.2, 1.3)
        self.cluster_dist = [ut.prepare_TH1D("cluster_dist_"+str(i), 1, 0, 75) for i in range(4)]
        self.cluster_dist_col = [rt.kYellow, rt.kBlue, rt.kGreen, rt.kRed]
        self.cluster_dist_sty = [rt.kSolid, rt.kDashed, rt.kDotted, rt.kDashDotted]

        #cluster position
        self.plots_cls = gEve.AddCanvasTab("Planes")
        self.plots_cls.Divide(2, 2)
        self.plots_cls_pos = [ut.prepare_TH2D("cls_"+str(i), 2, -75, 75, 2, -75, 75) for i in range(4)]
        for i in self.plots_cls_pos: ut.put_yx_tit(i, "Cluster #it{y} (mm)", "Cluster #it{x} (mm)", 1.2, 1.2)



        #current event
        self.iev = 0

    #init

    #_____________________________________________________________________________
    def main(self):

        #main frame for the gui
        frame = npy.Form(name="Low-Q2 tagger event display", lines=25, columns=80)

        #event navigation
        nav_x = 2
        nav_y = 2
        frame.add(npy.BoxBasic, name="Event navigation", editable=False, relx=nav_x, rely=nav_y, width=36, height=7)
        frame.add(npy.ButtonPress, name="Next", when_pressed_function=self.next_event, relx=nav_x+1, rely=nav_y+1)
        frame.add(npy.ButtonPress, name="Previous", when_pressed_function=self.previous_event, relx=nav_x+1, rely=nav_y+2)
        self.set_evt = frame.add(npy.TitleText, name="Set event", relx=nav_x+3, rely=nav_y+3, max_width=25)
        self.set_evt.value = "0"
        self.set_apply = frame.add(npy.ButtonPress, name="Apply", when_pressed_function=self.set_event, relx=nav_x+26, rely=nav_y+3)
        frame.add(npy.ButtonPress, name="Re-run current event", when_pressed_function=self.proc_event, relx=nav_x+1, rely=nav_y+4)

        #track criteria
        track_sel_x = 2
        track_sel_y = 10
        frame.add(npy.BoxBasic, name="Track criteria", editable=False, relx=track_sel_x, rely=track_sel_y, width=36, height=4)
        self.set_chi2 = frame.add(npy.TitleText, name="Max chi2ndf:", relx=track_sel_x+3, rely=track_sel_y+1, max_width=25)
        self.set_chi2.value = "0.5"
        self.set_chi2_apply = frame.add(npy.ButtonPress, name="Set", when_pressed_function=self.set_chiSq,
            relx=track_sel_x+28, rely=track_sel_y+1)

        #tagger selection
        tag_x = 2
        tag_y = 15
        frame.add(npy.BoxBasic, name="Tagger selection", editable=False, relx=tag_x, rely=tag_y, width=36, height=6)
        self.tag_sel = frame.add(npy.TitleSelectOne, max_height=2, max_width=32, values = ["Tagger 1", "Tagger 2"],
            name="Select:", relx=tag_x+1, rely=tag_y+1, scroll_exit=True)
        self.tag_sel.value = 0
        self.tag_apply = frame.add(npy.ButtonPress, name="Apply", when_pressed_function=self.set_tag, relx=tag_x+15, rely=tag_y+3)

        #event criteria
        evt_sel_x = 40
        evt_sel_y = 2
        frame.add(npy.BoxBasic, name="Event criteria", editable=False, relx=evt_sel_x, rely=evt_sel_y, width=30, height=7)
        self.set_min_ncls = frame.add(npy.TitleText, name="Min clusters:", relx=evt_sel_x+2, rely=evt_sel_y+1, max_width=25)
        self.set_min_ncls.value = "0"
        self.set_min_ntrk = frame.add(npy.TitleText, name="Min rec trk:", relx=evt_sel_x+2, rely=evt_sel_y+2, max_width=25)
        self.set_min_ntrk.value = "0"
        self.set_min_ncnt = frame.add(npy.TitleText, name="Min cnt trk:", relx=evt_sel_x+2, rely=evt_sel_y+3, max_width=25)
        self.set_min_ncnt.value = "0"
        self.evt_sel_apply = frame.add(npy.ButtonPress, name="Set", when_pressed_function=self.set_evt_sel,
            relx=evt_sel_x+16, rely=evt_sel_y+4)

        #clear and start
        npy.blank_terminal()
        frame.edit()

    #main

    #_____________________________________________________________________________
    def set_event(self):

        self.lib.task_AnaMapsBasicVis_set_event(self.task, int(self.set_evt.value))
        self.proc_event()

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
    def proc_event(self):

        self.iev = self.lib.task_AnaMapsBasicVis_process_event(self.task)
        self.draw_event()

    #_____________________________________________________________________________
    def draw_event(self):

        #plots
        self.tracks_chi2.Reset()
        for i in self.cluster_dist: i.Reset()
        for i in self.plots_cls_pos: i.Reset()

        #scene
        gEve.GetGlobalScene().DestroyElements()
        draw_markers()

        #clusters
        ncls_planes = [self.lib.task_AnaMapsBasicVis_ncls(self.task, i) for i in range(4)] # number of clusters in each plane
        ncls = sum(ncls_planes) # number of all clusters

        #cluster points
        clusters = TEvePointSet(ncls)
        clusters.SetName("Clusters")
        clusters.SetMarkerColor(rt.kYellow)
        clusters.SetMarkerStyle(3)
        icls = 0
        cls_xy = [[] for i in range(4)]
        for iplane in range(4):
            for i in range(ncls_planes[iplane]):
                x = c_double(0)
                y = c_double(0)
                z = c_double(0)
                self.lib.task_AnaMapsBasicVis_cluster(self.task, iplane, i, byref(x), byref(y), byref(z))
                clusters.SetPoint(icls, x.value, y.value, z.value)
                icls += 1
                cls_xy[iplane].append( (x.value, y.value) )

        gEve.AddGlobalElement(clusters)

        #tracks
        ntrk = self.lib.task_AnaMapsBasicVis_ntrk(self.task)
        for i in range(ntrk):

            #load the track
            x0 = c_double(0)
            y0 = c_double(0)
            slope_x = c_double(0)
            slope_y = c_double(0)
            chi2 = c_double(0)
            self.lib.task_AnaMapsBasicVis_track(self.task, i, byref(x0), byref(y0), byref(slope_x), byref(slope_y), byref(chi2))

            self.tracks_chi2.Fill( chi2.value/4. ) # 4 degrees of freedom

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
        stat_str += ", station: " + self.lib.task_AnaMapsBasicVis_det_nam(self.task).decode("utf-8")
        stat_str += ", max_chi2ndf: "+str( self.lib.task_AnaMapsBasicVis_get_max_chi2(self.task) )
        stat_str += ", clusters: "+str(ncls)+", reconstructed tracks: "+str(ntrk)
        stat_str += ", true tracks: "+str( self.lib.task_AnaMapsBasicVis_ntrk_ref(self.task) )

        gEve.GetStatusBar().SetParts(1)
        gEve.GetStatusBar().AddText(stat_str)
        gEve.GetStatusBar().SetHeight(30)

        #event plots

        #event data
        self.plots_evt.cd(1)#.Clear()
        #self.evt_frame.Reset()
        self.evt_frame.Draw()
        #evt_desc_frame = self.plots_evt.cd(1).DrawFrame(0, 0, 1, 1)
        #leg_evt = ut.prepare_leg(0.2, 0.2, 0.24, 0.4, 0.035)
        #leg_evt.AddEntry("", "Event number: "+str(self.iev), "")
        #leg_evt.AddEntry("", "Event number: ", "")
        #leg_evt.Draw("same")

        #evt_desc = pdesc(evt_desc_frame, 0.15, 0.78, 0.045)
        #evt_desc = pdesc(self.evt_frame, 0.2, 0.9, 0.045)
        #evt_desc.item("Event number", str(self.iev), rt.kGreen)
        #evt_desc.item("Clusters", str(ncls), rt.kGreen)
        #evt_desc.item("Tagger", self.lib.task_AnaMapsBasicVis_det_nam(self.task).decode("utf-8"), rt.kGreen)
        #evt_desc.draw()

        evt_desc = TLatex()
        evt_desc.SetTextColor(rt.kGreen)
        evt_desc_start = 0.95
        evt_desc_delt = 0.1
        evt_desc.DrawLatex(0.1, evt_desc_start, "Event number:  "+str(self.iev))
        evt_desc.DrawLatex(0.1, evt_desc_start - evt_desc_delt, "Tagger:  "+self.lib.task_AnaMapsBasicVis_det_nam(self.task).decode("utf-8"))
        evt_desc.DrawLatex(0.1, evt_desc_start - 2*evt_desc_delt, "Max_chi2ndf:  "+str(self.lib.task_AnaMapsBasicVis_get_max_chi2(self.task)))
        evt_desc.DrawLatex(0.1, evt_desc_start - 3*evt_desc_delt, "Clusters:  "+str(ncls))
        evt_desc.DrawLatex(0.1, evt_desc_start - 4*evt_desc_delt, "Reco tracks:  "+str(ntrk))
        evt_desc.DrawLatex(0.1, evt_desc_start - 5*evt_desc_delt, "True tracks:  "+str( self.lib.task_AnaMapsBasicVis_ntrk_ref(self.task) ))

        #tracks chi^2/ndf
        self.plots_evt.cd(2).SetGrid()
        ut.line_h1(self.tracks_chi2, rt.kBlue, 2)
        self.tracks_chi2.Draw()

        #cluster mutual distances
        self.plots_evt.cd(4).SetGrid()
        cls_dist_max = []
        for iplane in range(4):
            cls = cls_xy[iplane]
            for i in range(len(cls)):
                for j in range(i+1, len(cls)):
                    self.cluster_dist[iplane].Fill(sqrt( (cls[j][0]-cls[i][0])**2 + (cls[j][1]-cls[i][1])**2 ))
            ut.line_h1(self.cluster_dist[iplane], self.cluster_dist_col[iplane], 2)
            cls_dist_max.append( self.cluster_dist[iplane].GetMaximum() )

        frame_cls_dist = gPad.DrawFrame(0, 0, 75, 1.1*max(cls_dist_max)) # xmin, ymin, xmax, ymax
        ut.put_yx_tit(frame_cls_dist, "Counts", "Cluster mutual distances (mm)", 1.2, 1.3)
        frame_cls_dist.Draw()
        leg = ut.prepare_leg(0.7, 0.65, 0.24, 0.2, 0.035) # x, y, dx, dy, tsiz
        iplane = 1
        for i in self.cluster_dist:
            i.SetLineStyle(self.cluster_dist_sty[iplane-1])
            i.Draw("same")
            leg.AddEntry(i, "Plane_"+str(iplane), "l")
            iplane += 1
        leg.Draw("same")


        #cluster position
        for iplane in range(4):
            for cls in cls_xy[iplane]:
                self.plots_cls_pos[iplane].Fill(cls[0], cls[1])

        leg_planes = []
        for iplane in range(4):
            self.plots_cls.cd(iplane+1).SetGrid()
            self.plots_cls_pos[iplane].Draw("colz")
            leg_planes.append( ut.prepare_leg(0.67, 0.8, 0.24, 0.1, 0.035) )
            l = leg_planes[len(leg_planes)-1]
            l.AddEntry("", "Plane_"+str(iplane+1), "")
            l.Draw("same")

        ut.invert_col_can(self.plots_evt)
        ut.invert_col_can(self.plots_cls)

        self.plots_evt.Update()
        self.plots_cls.Update()

        gEve.FullRedraw3D(rt.kTRUE)

    #draw_event

    #_____________________________________________________________________________
    def set_tag(self):

        self.lib.task_AnaMapsBasicVis_set_det(self.task, self.tag_sel.value[0])

    #set_tag

    #_____________________________________________________________________________
    def set_chiSq(self):

        self.lib.task_AnaMapsBasicVis_set_max_chi2(self.task, c_double(float(self.set_chi2.value)))

    #set_chiSq

    #_____________________________________________________________________________
    def set_evt_sel(self):

        #self.set_min_ncls.value = "0"

        self.lib.task_AnaMapsBasicVis_set_min_ntrk(self.task, int(self.set_min_ntrk.value))

        #self.set_min_ncnt.value = "0"

    #set_evt_sel

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






















