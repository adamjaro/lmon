
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
AnaMapsBasicVis::AnaMapsBasicVis(const char *conf): iev(-1), min_ntrk(0),
    min_ncls(0), min_ncnt(0), min_etrk(0), min_sig_trk(0) {

  //configuration file
  program_options::options_description opt("opt");
  opt.add_options()
    ("main.input", program_options::value<string>(), "Analysis input")
    ("main.geo", program_options::value<string>(), "Geometry configuration")
    ("main.outfile", program_options::value<string>(), "Output from the analysis")
    ("main.max_chi2ndf", program_options::value<double>(), "Maximal tracks Chi2/NDF")
    ("main.min_cls_dist", program_options::value<double>(), "Minimal cluster distance")
    ("main.input_resp", program_options::value<string>(), "Input response for reconstruction")
    ("main.planes_output", program_options::value<bool>(), "Write output for planes")
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

  //input MC particles
  tree->SetBranchAddress("mcp_itrk", &fMCItrk); // track ID for the particle
  tree->SetBranchAddress("mcp_en", &fMCEn); // particle energy, GeV
  tree->SetBranchAddress("mcp_theta", &fMCTheta); // particle polar angle, rad
  tree->SetBranchAddress("mcp_phi", &fMCPhi); // particle azimuthal angle, rad

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

  s1->SetMCParticles(fMCItrk, fMCEn, fMCTheta, fMCPhi);
  s2->SetMCParticles(fMCItrk, fMCEn, fMCTheta, fMCPhi);

  //track selection for tagger stations
  if( opt_map.find("main.max_chi2ndf") != opt_map.end() ) {

    Double_t max_chi2ndf = opt_map["main.max_chi2ndf"].as<double>();
    //cout << "Using Chi2/NDF = " << max_chi2ndf << endl;

    s1->SetMaxChi2Ndf( max_chi2ndf );
    s2->SetMaxChi2Ndf( max_chi2ndf );
  }
  if( opt_map.find("main.min_cls_dist") != opt_map.end() ) {
    Double_t min_cls_dist = opt_map["main.min_cls_dist"].as<double>();
    cout << "Using min_cls_dist = " << min_cls_dist << endl;

    s1->SetClsLimMdist(min_cls_dist);
    s2->SetClsLimMdist(min_cls_dist);
  }

  //reference counters
  cnt_s1 = new RefCounter("cnt_s1", tree, &geo, otree);
  cnt_s2 = new RefCounter("cnt_s2", tree, &geo, otree);

  tag = s1;
  cnt = cnt_s1;

}//AnaMapsBasicVis

//_____________________________________________________________________________
int AnaMapsBasicVis::ProcessEvent(bool *stat) {

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

  //event selection
  if(stat) {

    *stat = true;

    if( GetNumberOfTracks() < min_ntrk ) *stat = false;
    if( tag->GetNumberOfClusters() < min_ncls ) *stat = false;
    if( GetNumberOfRefTracks() < min_ncnt ) *stat = false;
    if( GetNumberOfTracks()-GetNumberOfRefTracks() < min_etrk ) *stat = false;
    if( GetSigTracks() < min_sig_trk ) *stat = false;

  }

  //fill event tree
  otree->Fill();

  return iev;

}//ProcessEvent

//_____________________________________________________________________________
int AnaMapsBasicVis::NextEvent(int di) {

  //load and analyze next event

  //selection loop
  while(true) {

    iev += di;

    bool stat = true;
    ProcessEvent( &stat );

    //range in events
    if( di > 0 and iev >= tree->GetEntries()-1 ) stat = true;
    if( di < 0 and iev <= 0 ) stat = true;

    if(stat) break; // event criteria are satisfied

  }//selection loop

  return iev;

}//NextEvent

//_____________________________________________________________________________
int AnaMapsBasicVis::PreviousEvent() {

  return NextEvent(-1);

}//PreviousEvent

//_____________________________________________________________________________
void AnaMapsBasicVis::SetMaxChi2ndf(double chi2) {

  //set chi^2 limit for both taggers

  s1->SetMaxChi2Ndf(chi2);
  s2->SetMaxChi2Ndf(chi2);

}//SetMaxChi2ndf

//_____________________________________________________________________________
void AnaMapsBasicVis::SetClsLimMdist(double d) {

  //set limit on cluster distance for both taggers

  s1->SetClsLimMdist(d);
  s2->SetClsLimMdist(d);

}//SetClsLimMdist

//_____________________________________________________________________________
int AnaMapsBasicVis::GetNumberOfClusters(int iplane) {

  //number of clusters

  return tag->GetNumberOfClusters(iplane);

}//GetNumberOfClusters

//_____________________________________________________________________________
void AnaMapsBasicVis::GetCluster(int iplane, int icls, double& x, double& y, double& z, double& md) {

  //cluster on a given plane

  tag->GetCluster(iplane, icls, x, y, z, md);

}//GetCluster

//_____________________________________________________________________________
int AnaMapsBasicVis::GetNumberOfTracks() {

  //number of reconstructed tracks

  return tag->GetTracks().size();

}//GetNumberOfTracks

//_____________________________________________________________________________
int AnaMapsBasicVis::GetSigTracks() {

  //number of signal tracks having itrk == 1

  int nsig = 0;

  for(const auto& i: tag->GetTracks()) {
    if( i.itrk == 1 ) nsig++;
  }

  return nsig;

}//GetSigTracks

//_____________________________________________________________________________
void AnaMapsBasicVis::GetTrack(int i, double& x0, double& y0, double& slope_x, double& slope_y, double& chi2, int& itrk) {

  const vector<TagMapsBasic::Track>& tracks = tag->GetTracks();

  x0 = tracks[i].x;
  y0 = tracks[i].y;

  slope_x = tracks[i].slope_x;
  slope_y = tracks[i].slope_y;

  chi2 = tracks[i].chi2_xy;

  itrk = tracks[i].itrk;

}//GetTrack

//_____________________________________________________________________________
int AnaMapsBasicVis::GetNumberOfRefTracks() {

  //number of reference tracks

  return cnt->GetTracks().size();

}//GetNumberOfRefTracks

//_____________________________________________________________________________
void AnaMapsBasicVis::SetDet(int i) {

  //select the active tagger detector
  if(i == 0) {
    tag = s1;
    cnt = cnt_s1;
  }
  if(i == 1) {
    tag = s2;
    cnt = cnt_s2;
  }

}//SetDet

//_____________________________________________________________________________
extern "C" {

  //make the instance
  AnaMapsBasicVis* make_AnaMapsBasicVis(const char *c) { return new AnaMapsBasicVis(c); }

  //detector station
  const char* task_AnaMapsBasicVis_det_nam(AnaMapsBasicVis& t) { return t.GetDetName().c_str(); }
  void task_AnaMapsBasicVis_set_det(AnaMapsBasicVis& t, int i) { t.SetDet(i); }

  //event navigation
  int task_AnaMapsBasicVis_next_event(AnaMapsBasicVis& t) { return t.NextEvent(); }
  int task_AnaMapsBasicVis_prev_event(AnaMapsBasicVis& t) { return t.PreviousEvent(); }
  void task_AnaMapsBasicVis_set_event(AnaMapsBasicVis& t, int i) { t.SetEvent(i); }
  int task_AnaMapsBasicVis_process_event(AnaMapsBasicVis& t) { return t.ProcessEvent(); }

  //clusters
  int task_AnaMapsBasicVis_ncls(AnaMapsBasicVis& t, int i) { return t.GetNumberOfClusters(i); }
  void task_AnaMapsBasicVis_cluster(AnaMapsBasicVis& t, int iplane, int icls, double& x, double& y, double& z, double& md) {
    return t.GetCluster(iplane, icls, x, y, z, md);
  }

  //tracks
  int task_AnaMapsBasicVis_ntrk(AnaMapsBasicVis& t) { return t.GetNumberOfTracks(); }
  void task_AnaMapsBasicVis_track(AnaMapsBasicVis& t, int i, double& x0, double& y0, double& slope_x, double& slope_y,
    double& chi2, int& itrk) {
    return t.GetTrack(i, x0, y0, slope_x, slope_y, chi2, itrk);
  }
  void task_AnaMapsBasicVis_set_max_chi2(AnaMapsBasicVis& t, double c) { return t.SetMaxChi2ndf(c); }
  double task_AnaMapsBasicVis_get_max_chi2(AnaMapsBasicVis& t) { return t.GetMaxChi2ndf(); }
  void task_AnaMapsBasicVis_set_lim_mdist(AnaMapsBasicVis& t, double d) { t.SetClsLimMdist(d); }
  double task_AnaMapsBasicVis_get_lim_mdist(AnaMapsBasicVis& t) { return t.GetClsLimMdist(); }
  int task_AnaMapsBasicVis_ntrk_ref(AnaMapsBasicVis& t) { return t.GetNumberOfRefTracks(); }

  //event selection
  void task_AnaMapsBasicVis_set_min_ntrk(AnaMapsBasicVis& t, int n) { t.SetMinNtrk(n); }
  void task_AnaMapsBasicVis_set_min_ncls(AnaMapsBasicVis& t, int n) { t.SetMinNcls(n); }
  void task_AnaMapsBasicVis_set_min_ncnt(AnaMapsBasicVis& t, int n) { t.SetMinNcnt(n); }
  void task_AnaMapsBasicVis_set_min_etrk(AnaMapsBasicVis& t, int n) { t.SetMinEtrk(n); }
  void task_AnaMapsBasicVis_set_min_sig_trk(AnaMapsBasicVis& t, int n) { t.SetMinSigTrk(n); }

}





















