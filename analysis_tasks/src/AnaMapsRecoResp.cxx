
//C++
#include <iostream>
#include "glob.h"

//Boost
#include <boost/program_options.hpp>

//ROOT
#include "TChain.h"
#include "TFile.h"
#include "TMath.h"

//Geant
#include "G4Step.hh"
#include "G4String.hh"

//local classes
#include "TagMapsBasic.h"
#include "GeoParser.h"
#include "RefCounter.h"
#include "EThetaPhiReco.h"
#include "AnaMapsRecoResp.h"

using namespace std;
using namespace boost;
using namespace boost::program_options;

//_____________________________________________________________________________
AnaMapsRecoResp::AnaMapsRecoResp(const char *conf) {

  //configuration file
  options_description opt("opt");
  opt.add_options()
    ("main.input", program_options::value<string>(), "Analysis input")
    ("main.geo", program_options::value<string>(), "Geometry configuration")
    ("main.outfile", program_options::value<string>(), "Output from the analysis")
    ("main.max_chi2ndf", program_options::value<double>(), "Maximal tracks Chi2/NDF")
    ("main.min_cls_dist", program_options::value<double>(), "Minimal cluster distance")
  ;

  //reconstruction for tagger stations
  EThetaPhiReco s1_rec("s1", &opt);
  EThetaPhiReco s2_rec("s2", &opt);

  //quantities measured by the taggers
  s1_rec.MakeQuantity("x"); // x position, mm
  s1_rec.MakeQuantity("y"); // y position, mm
  s1_rec.MakeQuantity("tx", 1e-3); // theta_x angle, range set in mrad, conversion to rad
  s1_rec.MakeQuantity("ty", 1e-3); // theta_y angle, mrad conversion to rad
  s2_rec.MakeQuantity("x");
  s2_rec.MakeQuantity("y");
  s2_rec.MakeQuantity("tx", 1e-3);
  s2_rec.MakeQuantity("ty", 1e-3);

  //load the configuration file
  variables_map opt_map;
  store(parse_config_file(conf, opt), opt_map);

  //inputs
  string input = GetStr(opt_map, "main.input");
  cout << "Input: " << input << endl;
  glob_t glob_inputs;
  glob(input.c_str(), GLOB_TILDE, NULL, &glob_inputs);

  //input tree
  TChain tree("DetectorTree");
  for(size_t i=0; i<glob_inputs.gl_pathc; i++) {
    tree.Add( glob_inputs.gl_pathv[i] );
  }

  //input true kinematics
  tree.SetBranchAddress("true_el_E", &true_el_E);
  tree.SetBranchAddress("true_el_theta", &true_el_theta);
  tree.SetBranchAddress("true_el_phi", &true_el_phi);

  //geometry
  GeoParser geo(GetStr(opt_map, "main.geo"));

  //initialize the reconstruction
  s1_rec.Initialize(&opt_map);
  s2_rec.Initialize(&opt_map);

  //output file
  TFile out(GetStr(opt_map, "main.outfile").c_str(), "recreate");

  //interaction tree
  TTree otree("event", "event");

  //tagger stations
  TagMapsBasic s1("s1", &tree, &geo, &otree);
  TagMapsBasic s2("s2", &tree, &geo, &otree);
  s1.CreateOutput(false); // no output from planes
  s2.CreateOutput(false);

  //selection criteria
  if( opt_map.find("main.max_chi2ndf") != opt_map.end() ) {
    Double_t x = opt_map["main.max_chi2ndf"].as<double>();
    s1.SetMaxChi2Ndf(x);
    s2.SetMaxChi2Ndf(x);
  }
  if( opt_map.find("main.min_cls_dist") != opt_map.end() ) {
    Double_t x = opt_map["main.min_cls_dist"].as<double>();
    s1.SetClsLimMdist(x);
    s2.SetClsLimMdist(x);
  }

  //reference counters
  RefCounter cnt_s1("cnt_s1", &tree, &geo, &otree);
  RefCounter cnt_s2("cnt_s2", &tree, &geo, &otree);

  //event loop
  Long64_t nev = tree.GetEntries();
  //nev = 220;
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    //run for both taggers
    ProcessEvent(s1, cnt_s1, s1_rec);
    ProcessEvent(s2, cnt_s2, s2_rec);

    //fill the output tree
    otree.Fill();

  }//event loop

  WriteOutputs(s1, cnt_s1);
  WriteOutputs(s2, cnt_s2);

  otree.Write();

  s1_rec.Export();
  s2_rec.Export();

  out.Close();

}//AnaMapsRecoResp

//_____________________________________________________________________________
void AnaMapsRecoResp::ProcessEvent(TagMapsBasic& tag, RefCounter& cnt, EThetaPhiReco& rec) {

  tag.ProcessEvent();
  cnt.ProcessEvent();

  //from AnaMapsBasic
  AssociateMC(tag, cnt);

  tag.FinishEvent();
  cnt.FinishEvent();

  //tracks in event
  vector<TagMapsBasic::Track>& tracks = tag.GetTracks();

  //tracks loop
  for(const auto& trk: tracks) {

    //primary track
    if( !trk.is_prim ) continue;

    //associated track with reference counter
    if( !trk.is_associate ) continue;

    //tolerance in x and y position, mm
    if( TMath::Abs(trk.x-trk.ref_x) > 0.1 ) continue;
    if( TMath::Abs(trk.y-trk.ref_y) > 0.1 ) continue;

    //tolerance in theta_x and theta_y, mrad
    if( 1e3*TMath::Abs(trk.theta_x-trk.ref_theta_x) > 0.15 ) continue;
    if( 1e3*TMath::Abs(trk.theta_y-trk.ref_theta_y) > 0.15 ) continue;

    //cout << 1e3*trk.theta_x << " " << 1e3*trk.ref_theta_x << " " << 1e3*TMath::Abs(trk.theta_x-trk.ref_theta_x) << endl;

    //add input for reconstruction
    Double_t quant[4]{trk.x, trk.y, trk.theta_x, trk.theta_y};
    rec.AddInput(quant, true_el_E, true_el_theta, true_el_phi);

  }//tracks loop

}//ProcessEvent

//_____________________________________________________________________________
void AnaMapsRecoResp::WriteOutputs(TagMapsBasic& tag, RefCounter& cnt) {

  tag.WriteOutputs();
  cnt.WriteOutputs();

}//WriteOutputs

//_____________________________________________________________________________
extern "C" {

  //make the instance
  AnaMapsRecoResp* make_AnaMapsRecoResp(const char *c) { return new AnaMapsRecoResp(c); }

}


