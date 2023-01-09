
//C++
#include <iostream>
#include <string>
#include "glob.h"
#include <new>

//Boost
#include <boost/program_options.hpp>

//ROOT
#include "TChain.h"
#include "TTree.h"
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
#include "AnaMapsBasic.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
void AnaMapsBasic::Run(const char *conf) {

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
  cout << "Input: " << input << endl;
  glob_t glob_inputs;
  glob(input.c_str(), GLOB_TILDE, NULL, &glob_inputs);

  //input tree
  TChain tree("DetectorTree");
  for(size_t i=0; i<glob_inputs.gl_pathc; i++) {
    cout << "Adding input: " << glob_inputs.gl_pathv[i] << endl;
    tree.Add( glob_inputs.gl_pathv[i] );
  }

  //input true kinematics
  Double_t true_el_E, true_el_theta, true_el_phi, true_Q2, true_x, true_y;
  tree.SetBranchAddress("true_el_E", &true_el_E);
  tree.SetBranchAddress("true_el_theta", &true_el_theta);
  tree.SetBranchAddress("true_el_phi", &true_el_phi);
  tree.SetBranchAddress("true_Q2", &true_Q2);
  tree.SetBranchAddress("true_x", &true_x);
  tree.SetBranchAddress("true_y", &true_y);

  //beam energy
  beam_en = 18; //GeV

  //geometry
  string geo_nam = GetStr(opt_map, "main.geo");
  cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

  //input response for electron reconstruction
  EThetaPhiReco *s1_rec = 0x0;
  EThetaPhiReco *s2_rec = 0x0;
  if( opt_map.find("main.input_resp") != opt_map.end() ) {
    string input_resp = GetStr(opt_map, "main.input_resp");
    cout << "Response input: " << input_resp << endl;

    //create the response for both taggers
    s1_rec = new EThetaPhiReco("s1");
    s2_rec = new EThetaPhiReco("s2");

    //initialize the response from trained input
    TFile in_resp(input_resp.c_str(), "read");
    s1_rec->Import(&in_resp);
    s2_rec->Import(&in_resp);
  }

  //outputs
  string outfile = GetStr(opt_map, "main.outfile");
  cout << "Output: " << outfile << endl;
  TFile out(outfile.c_str(), "recreate");

  //interaction (event) output tree
  TTree otree("event", "event");
  otree.Branch("true_el_E", &true_el_E, "true_el_E/D");
  otree.Branch("true_el_theta", &true_el_theta, "true_el_theta/D");
  otree.Branch("true_el_phi", &true_el_phi, "true_el_phi/D");
  otree.Branch("true_Q2", &true_Q2, "true_Q2/D");
  otree.Branch("true_x", &true_x, "true_x/D");
  otree.Branch("true_y", &true_y, "true_y/D");

  //tagger stations
  TagMapsBasic s1("s1", &tree, &geo, &otree);
  TagMapsBasic s2("s2", &tree, &geo, &otree);
  bool planes_output = true;
  if( opt_map.find("main.planes_output") != opt_map.end() ) {
    planes_output = opt_map["main.planes_output"].as<bool>();
  }
  s1.CreateOutput(planes_output);
  s2.CreateOutput(planes_output);

  s1.AddTrackBranch("true_el_E", &true_el_E);
  s1.AddTrackBranch("true_el_theta", &true_el_theta);
  s1.AddTrackBranch("true_el_phi", &true_el_phi);
  s1.AddTrackBranch("true_Q2", &true_Q2);
  s2.AddTrackBranch("true_el_E", &true_el_E);
  s2.AddTrackBranch("true_el_theta", &true_el_theta);
  s2.AddTrackBranch("true_el_phi", &true_el_phi);
  s2.AddTrackBranch("true_Q2", &true_Q2);

  //track selection for tagger stations
  if( opt_map.find("main.max_chi2ndf") != opt_map.end() ) {

    Double_t max_chi2ndf = opt_map["main.max_chi2ndf"].as<double>();
    cout << "Using Chi2/NDF = " << max_chi2ndf << endl;

    s1.SetMaxChi2Ndf( max_chi2ndf );
    s2.SetMaxChi2Ndf( max_chi2ndf );
  }
  if( opt_map.find("main.min_cls_dist") != opt_map.end() ) {
    Double_t min_cls_dist = opt_map["main.min_cls_dist"].as<double>();
    cout << "Using min_cls_dist = " << min_cls_dist << endl;

    s1.SetClsLimMdist(min_cls_dist);
    s2.SetClsLimMdist(min_cls_dist);
  }

  //reference counters
  RefCounter cnt_s1("cnt_s1", &tree, &geo, &otree);
  RefCounter cnt_s2("cnt_s2", &tree, &geo, &otree);

  //event loop
  Long64_t nev = tree.GetEntries();
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    //process the event for both taggers
    s1.ProcessEvent();
    s2.ProcessEvent();

    cnt_s1.ProcessEvent();
    cnt_s2.ProcessEvent();

    AssociateMC(s1, cnt_s1);
    AssociateMC(s2, cnt_s2);

    //run electron reconstruction
    ElectronRec(s1, cnt_s1, s1_rec);
    ElectronRec(s2, cnt_s2, s2_rec);

    s1.FinishEvent();
    s2.FinishEvent();

    cnt_s1.FinishEvent();
    cnt_s2.FinishEvent();

    //fill event tree
    otree.Fill();

  }//event loop

  s1.WriteOutputs();
  s2.WriteOutputs();

  cnt_s1.WriteOutputs();
  cnt_s2.WriteOutputs();

  otree.Write();

  out.Close();

}//Run

//_____________________________________________________________________________
void AnaMapsBasic::AssociateMC(TagMapsBasic& tag, RefCounter& cnt) {

  //associate tagger tracks with MC particles in reference counter

  vector<TagMapsBasic::Track>& tracks = tag.GetTracks();
  vector<RefCounter::Track>& ref_cnt = cnt.GetTracks();

  //tracks loop
  for(auto it = tracks.begin(); it != tracks.end(); it++) {

    //measured track
    TagMapsBasic::Track& trk = *it;

    //test for reference track using defined index to MC particle
    if( trk.itrk < 0 ) continue;

    //reference tracks loop
    for(auto ir = ref_cnt.begin(); ir != ref_cnt.end(); ir++) {

      //reference track
      RefCounter::Track& ref = *ir;

      //associate measured track with reference track
      if( ref.itrk != trk.itrk ) continue;

      //measured track is associated
      trk.is_associate = true;

      //reference values for track position and angles
      trk.ref_x = ref.x;
      trk.ref_y = ref.y;
      trk.ref_theta_x = ref.theta_x;
      trk.ref_theta_y = ref.theta_y;

      //mark the reference track as having measured track
      ref.is_rec = true;

    }//reference tracks loop
  }//tracks loop

}//AssociateMC

//_____________________________________________________________________________
void AnaMapsBasic::ElectronRec(TagMapsBasic& tag, RefCounter&, EThetaPhiReco *rec) {

  //run electron reconstruction with the response
  if( !rec ) return;

  //tracks loop
  for(TagMapsBasic::Track& trk: tag.GetTracks()) {

    //reconstruction for the track
    Double_t quant[4]{trk.x, trk.y, trk.theta_x, trk.theta_y}; // input tagger quantity
    Double_t rec_en=0, rec_theta=0, rec_phi=0; // reconstructed electron by reference
    Bool_t stat = rec->Reconstruct(quant, rec_en, rec_theta, rec_phi); // perform the reconstruction
    if( !stat ) continue;

    //original electron corresponding to the track is reconstructed, set the track parameters 
    trk.is_rec = kTRUE;
    trk.rec_en = rec_en;
    trk.rec_theta = rec_theta;
    trk.rec_phi = rec_phi;

    //reconstructed electron Q^2 by beam energy, electron energy and polar angle
    trk.rec_Q2 = 2*beam_en*trk.rec_en*(1-TMath::Cos(TMath::Pi()-trk.rec_theta));

  }//tracks loop

}//ElectronRec

//_____________________________________________________________________________
string AnaMapsBasic::GetStr(program_options::variables_map& opt_map, std::string par) {

  string res = opt_map[par].as<string>();
  res.erase(remove(res.begin(), res.end(), '\"'), res.end());

  return res;

}//GetStr

//_____________________________________________________________________________
extern "C" {

  //AnaMapsBasic* make_AnaMapsBasic() { return new AnaMapsBasic(); }
  void* make_AnaMapsBasic() { return new(nothrow) AnaMapsBasic(); }

  //void run_AnaMapsBasic(AnaMapsBasic& t, const char *c) { t.Run(c); }

  void run_AnaMapsBasic(void *t, const char *c) {

    AnaMapsBasic *task = reinterpret_cast<AnaMapsBasic*>(t);

    task->Run(c);
  }

}
































