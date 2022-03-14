
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

//Geant
#include "G4String.hh"

//local classes
#include "GeoParser.h"
#include "TagCounter.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
int main(int argc, char* argv[]) {

  //configuration file
  program_options::options_description opt("opt");
  opt.add_options()
    ("main.input", program_options::value<string>(), "Analysis input")
    ("main.geo", program_options::value<string>(), "Geometry configuration")
    ("main.outfile", program_options::value<string>(), "Output from the analysis")
    ("main.planes_output", program_options::value<bool>(), "Output for individual planes")
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
  string input = opt_map["main.input"].as<string>();
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
  Double_t true_x, true_y, true_Q2, true_el_pT, true_el_theta, true_el_phi, true_el_E;
  tree.SetBranchAddress("true_x", &true_x);
  tree.SetBranchAddress("true_y", &true_y);
  tree.SetBranchAddress("true_Q2", &true_Q2);
  tree.SetBranchAddress("true_el_pT", &true_el_pT);
  tree.SetBranchAddress("true_el_theta", &true_el_theta);
  tree.SetBranchAddress("true_el_phi", &true_el_phi);
  tree.SetBranchAddress("true_el_E", &true_el_E);

  //geometry
  string geo_nam = opt_map["main.geo"].as<string>();
  geo_nam.erase(remove(geo_nam.begin(), geo_nam.end(), '\"'), geo_nam.end());
  cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

  //output trees
  string outfile = opt_map["main.outfile"].as<string>();
  outfile.erase(remove(outfile.begin(), outfile.end(), '\"'), outfile.end());
  cout << "Output: " << outfile << endl;
  TFile out(outfile.c_str(), "recreate");

  //interaction tree
  TTree otree("event", "event");
  otree.Branch("true_x", &true_x, "true_x/D");
  otree.Branch("true_y", &true_y, "true_y/D");
  otree.Branch("true_Q2", &true_Q2, "true_Q2/D");
  otree.Branch("true_el_pT", &true_el_pT, "true_el_pT/D");
  otree.Branch("true_el_theta", &true_el_theta, "true_el_theta/D");
  otree.Branch("true_el_phi", &true_el_phi, "true_el_phi/D");
  otree.Branch("true_el_E", &true_el_E, "true_el_E/D");

  //output for individual planes
  bool planes_output = opt_map["main.planes_output"].as<bool>();

  //tagger stations
  TagCounter s1("s1", &tree, &otree, &geo);
  TagCounter s2("s2", &tree, &otree, &geo);
  s1.CreateOutput(planes_output);
  s1.AddOutputBranch("true_el_E", &true_el_E);
  s1.AddOutputBranch("true_el_theta", &true_el_theta);
  s1.AddOutputBranch("true_el_phi", &true_el_phi);
  s2.CreateOutput(planes_output);
  s2.AddOutputBranch("true_el_E", &true_el_E);
  s2.AddOutputBranch("true_el_theta", &true_el_theta);
  s2.AddOutputBranch("true_el_phi", &true_el_phi);

  //event loop
  Long64_t nev = tree.GetEntries();
  //Long64_t nev = 220;
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    s1.ProcessEvent();
    s2.ProcessEvent();

    otree.Fill();

  }//event loop

  cout << "All events: " << tree.GetEntries() << endl;

  otree.Write();
  s1.WriteOutputs();
  s2.WriteOutputs();
  out.Close();

  return 0;

}//main
















