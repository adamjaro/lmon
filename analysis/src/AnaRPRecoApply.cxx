
//C++
#include <iostream>
#include "glob.h"
#include <fstream>
#include <algorithm>

//Boost
#include <boost/program_options.hpp>

//ROOT
#include "TChain.h"
#include "TTree.h"
#include "TFile.h"
#include "TMath.h"

//Geant
#include "G4String.hh"

//local classes
#include "GeoParser.h"
#include "EThetaPhiReco.h"
#include "TagCounter.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
int main(int argc, char* argv[]) {

  //configuration file
  program_options::options_description opt("opt");
  opt.add_options()
    ("main.input_rec", program_options::value<string>(), "Input for reconstruction")
    ("main.output", program_options::value<string>(), "Output from reconstruction")
    ("main.geo", program_options::value<string>(), "Geometry configuration")
    ("main.input_resp", program_options::value<string>(), "Response input for reconstruction")
  ;

  //load the configuration file
  if(argc < 2) {
    cout << "No configuration specified." << endl;
    return -1;
  }
  ifstream config(argv[1]);
  program_options::variables_map opt_map;
  program_options::store(program_options::parse_config_file(config, opt), opt_map);

  //inputs
  string input = opt_map["main.input_rec"].as<string>();
  input.erase(remove(input.begin(), input.end(), '\"'), input.end());
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

  //reconstruction for tagger stations
  EThetaPhiReco s1_rec("s1");
  EThetaPhiReco s2_rec("s2");

  //import the response for reconstruction
  string input_resp = opt_map["main.input_resp"].as<string>();
  input_resp.erase(remove(input_resp.begin(), input_resp.end(), '\"'), input_resp.end());
  cout << "Response input: " << input_resp << endl;
  TFile in_resp(input_resp.c_str(), "read");
  s1_rec.Import(&in_resp);
  s2_rec.Import(&in_resp);

  //geometry
  string geo_nam = opt_map["main.geo"].as<string>();
  geo_nam.erase(remove(geo_nam.begin(), geo_nam.end(), '\"'), geo_nam.end());
  cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

  //output from the reconstruction
  string outfile = opt_map["main.output"].as<string>();
  outfile.erase(remove(outfile.begin(), outfile.end(), '\"'), outfile.end());
  cout << "Output: " << outfile << endl;
  TFile out(outfile.c_str(), "recreate");

  s1_rec.CreateRecoOutput();
  s2_rec.CreateRecoOutput();

  s1_rec.AddOutputBranch("true_el_E", &true_el_E);
  s1_rec.AddOutputBranch("true_el_theta", &true_el_theta);
  s1_rec.AddOutputBranch("true_el_phi", &true_el_phi);
  s1_rec.AddOutputBranch("true_Q2", &true_Q2);

  s2_rec.AddOutputBranch("true_el_E", &true_el_E);
  s2_rec.AddOutputBranch("true_el_theta", &true_el_theta);
  s2_rec.AddOutputBranch("true_el_phi", &true_el_phi);
  s2_rec.AddOutputBranch("true_Q2", &true_Q2);

  //interaction tree
  TTree otree("event", "event");

  //tagger stations
  TagCounter tag_s1("s1", &tree, &otree, &geo);
  TagCounter tag_s2("s2", &tree, &otree, &geo);

  //kinematics and reconstruction flags in interaction tree
  otree.Branch("true_el_E", &true_el_E, "true_el_E/D");
  otree.Branch("true_el_theta", &true_el_theta, "true_el_theta/D");
  otree.Branch("true_el_phi", &true_el_phi, "true_el_phi/D");
  Bool_t s1_IsRec, s2_IsRec;
  otree.Branch("s1_IsRec", &s1_IsRec, "s1_IsRec/O");
  otree.Branch("s2_IsRec", &s2_IsRec, "s2_IsRec/O");

  //event loop
  Long64_t nev = tree.GetEntries();
  //Long64_t nev = 320;
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    tag_s1.ProcessEvent();
    tag_s2.ProcessEvent();

    s1_IsRec = kFALSE;
    s2_IsRec = kFALSE;

    if( tag_s1.GetIsHit() ) {
      Double_t quant[4]{tag_s1.GetX(), tag_s1.GetY(), tag_s1.GetThetaX(), tag_s1.GetThetaY()};
      s1_IsRec = s1_rec.Reconstruct(quant);
    }

    if( tag_s2.GetIsHit() ) {
      Double_t quant[4]{tag_s2.GetX(), tag_s2.GetY(), tag_s2.GetThetaX(), tag_s2.GetThetaY()};
      s2_IsRec = s2_rec.Reconstruct(quant);
    }

    otree.Fill();

  }//event loop

  cout << "All events: " << tree.GetEntries() << endl;

  s1_rec.WriteRecoOutput();
  s2_rec.WriteRecoOutput();
  otree.Write();

  out.Close();









  return 0;

}

