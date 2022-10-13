
//C++
#include <iostream>
#include "glob.h"

//Boost
#include <boost/program_options.hpp>

//ROOT
#include "TChain.h"
#include "TTree.h"
#include "TFile.h"

//Geant
#include "G4Step.hh"
#include "G4String.hh"

//local classes
#include "TagMapsBasic.h"
#include "GeoParser.h"
#include "RefCounter.h"
#include "AnaMapsBasicVis.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
AnaMapsBasicVis::AnaMapsBasicVis(const char *conf): iev(0) {

  //configuration file
  program_options::options_description opt("opt");
  opt.add_options()
    ("main.input", program_options::value<string>(), "Analysis input")
    ("main.geo", program_options::value<string>(), "Geometry configuration")
    ("main.outfile", program_options::value<string>(), "Output from the analysis")
    ("main.max_chi2ndf", program_options::value<double>(), "Maximal tracks Chi2/NDF")
  ;

  //load the configuration file
  ifstream config(conf);
  program_options::variables_map opt_map;
  program_options::store(program_options::parse_config_file(config, opt), opt_map);

  //inputs
  string input = GetStr(opt_map, "main.input");
  glob_t glob_inputs;
  glob(input.c_str(), GLOB_TILDE, NULL, &glob_inputs);

  //input tree
  tree = new TChain("DetectorTree");
  for(size_t i=0; i<glob_inputs.gl_pathc; i++) {
    //cout << "Adding input: " << glob_inputs.gl_pathv[i] << endl;
    tree->Add( glob_inputs.gl_pathv[i] );
  }

  //geometry
  string geo_nam = GetStr(opt_map, "main.geo");
  //cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

  //outputs
  string outfile = GetStr(opt_map, "main.outfile");
  //cout << "Output: " << outfile << endl;
  out = new TFile(outfile.c_str(), "recreate");

  //interaction (event) output tree
  otree = new TTree("event", "event");

  //tagger stations
  s1 = new TagMapsBasic("s1", tree, &geo, otree);
  s2 = new TagMapsBasic("s2", tree, &geo, otree);
  s1->CreateOutput();
  s2->CreateOutput();

  //track selection for tagger stations
  if( opt_map.find("main.max_chi2ndf") != opt_map.end() ) {

    Double_t max_chi2ndf = opt_map["main.max_chi2ndf"].as<double>();
    //cout << "Using Chi2/NDF = " << max_chi2ndf << endl;

    s1->SetMaxChi2Ndf( max_chi2ndf );
    s2->SetMaxChi2Ndf( max_chi2ndf );
  }

  //reference counters
  cnt_s1 = new RefCounter("cnt_s1", tree, &geo, otree);
  cnt_s2 = new RefCounter("cnt_s2", tree, &geo, otree);

  tag = s1;

}//AnaMapsBasicVis

//_____________________________________________________________________________
int AnaMapsBasicVis::NextEvent() {

  //load and analyze next event

  if( iev < 0 ) iev = 0;
  if( iev >= tree->GetEntries() ) iev = tree->GetEntries()-1;

  tree->GetEntry(iev);

  //process the event for both taggers
  s1->ProcessEvent();
  s2->ProcessEvent();

  cnt_s1->ProcessEvent();
  cnt_s2->ProcessEvent();

  AssociateMC(*s1, *cnt_s1);
  AssociateMC(*s2, *cnt_s2);

  s1->FinishEvent();
  s2->FinishEvent();

  //fill event tree
  otree->Fill();

  iev++;

  return iev-1;

}//NextEvent

//_____________________________________________________________________________
int AnaMapsBasicVis::PreviousEvent() {

  iev -= 2;
  return NextEvent();

}//PreviousEvent

//_____________________________________________________________________________
int AnaMapsBasicVis::GetNumberOfClusters(int iplane) {

  return tag->GetNumberOfClusters(iplane);

}//GetNumberOfClusters

//_____________________________________________________________________________
void AnaMapsBasicVis::GetCluster(int iplane, int icls, double& x, double& y, double& z) {

  tag->GetCluster(iplane, icls, x, y, z);

}//GetCluster

//_____________________________________________________________________________
int AnaMapsBasicVis::GetNumberOfTracks() {

  return tag->GetTracks().size();

}//GetNumberOfTracks

//_____________________________________________________________________________
void AnaMapsBasicVis::GetTrack(int i, double& x0, double& y0, double& slope_x, double& slope_y) {

  const vector<TagMapsBasic::Track>& tracks = tag->GetTracks();

  x0 = tracks[i].x;
  y0 = tracks[i].y;

  slope_x = tracks[i].slope_x;
  slope_y = tracks[i].slope_y;

}//GetTrack

//_____________________________________________________________________________
extern "C" {

  //make the instance
  AnaMapsBasicVis* make_AnaMapsBasicVis(const char *c) { return new AnaMapsBasicVis(c); }

  //event
  int task_AnaMapsBasicVis_next_event(AnaMapsBasicVis& t) { return t.NextEvent(); }
  int task_AnaMapsBasicVis_prev_event(AnaMapsBasicVis& t) { return t.PreviousEvent(); }
  void task_AnaMapsBasicVis_set_event(AnaMapsBasicVis& t, int i) { t.SetEvent(i); }

  //clusters
  int task_AnaMapsBasicVis_ncls(AnaMapsBasicVis& t, int i) { return t.GetNumberOfClusters(i); }
  void task_AnaMapsBasicVis_cluster(AnaMapsBasicVis& t, int iplane, int icls, double& x, double& y, double& z) {
    return t.GetCluster(iplane, icls, x, y, z);
  }

  //tracks
  int task_AnaMapsBasicVis_ntrk(AnaMapsBasicVis& t) { return t.GetNumberOfTracks(); }
  void task_AnaMapsBasicVis_track(AnaMapsBasicVis& t, int i, double& x0, double& y0, double& slope_x, double& slope_y) {
    return t.GetTrack(i, x0, y0, slope_x, slope_y);
  }

}





















