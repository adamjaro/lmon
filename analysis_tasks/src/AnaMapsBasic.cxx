
//C++
#include <iostream>
#include <string>
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
  Double_t true_el_E, true_el_theta, true_el_phi, true_Q2;
  tree.SetBranchAddress("true_el_E", &true_el_E);
  tree.SetBranchAddress("true_el_theta", &true_el_theta);
  tree.SetBranchAddress("true_el_phi", &true_el_phi);
  tree.SetBranchAddress("true_Q2", &true_Q2);

  //geometry
  string geo_nam = GetStr(opt_map, "main.geo");
  cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

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

  //tagger stations
  TagMapsBasic s1("s1", &tree, &geo, &otree);
  TagMapsBasic s2("s2", &tree, &geo, &otree);
  s1.CreateOutput();
  s2.CreateOutput();
  s1.AddTrackBranch("true_el_E", &true_el_E);
  s1.AddTrackBranch("true_el_theta", &true_el_theta);
  s1.AddTrackBranch("true_el_phi", &true_el_phi);
  s1.AddTrackBranch("true_Q2", &true_Q2);
  s2.AddTrackBranch("true_el_E", &true_el_E);
  s2.AddTrackBranch("true_el_theta", &true_el_theta);
  s2.AddTrackBranch("true_el_phi", &true_el_phi);
  s2.AddTrackBranch("true_Q2", &true_Q2);

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

    s1.FinishEvent();
    s2.FinishEvent();

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
  const vector<RefCounter::Track>& ref_cnt = cnt.GetTracks();

  //tracks loop
  for(auto it = tracks.begin(); it != tracks.end(); it++) {

    //measured track
    TagMapsBasic::Track& trk = *it;

    //test for reference track using defined index to MC particle
    if( trk.itrk < 0 ) continue;

    //reference tracks loop
    for(auto ir = ref_cnt.begin(); ir != ref_cnt.end(); ir++) {

      //reference track
      const RefCounter::Track& ref = *ir;

      //associate measured track with reference track
      if( ref.itrk != trk.itrk ) continue;

      //measured track is associated
      trk.is_associate = true;

      //reference values for track position and angles
      trk.ref_x = ref.x;
      trk.ref_y = ref.y;
      trk.ref_theta_x = ref.theta_x;
      trk.ref_theta_y = ref.theta_y;

    }//reference tracks loop
  }//tracks loop

}//AssociateMC

//_____________________________________________________________________________
string AnaMapsBasic::GetStr(program_options::variables_map& opt_map, std::string par) {

  string res = opt_map[par].as<string>();
  res.erase(remove(res.begin(), res.end(), '\"'), res.end());

  return res;

}//GetStr



































