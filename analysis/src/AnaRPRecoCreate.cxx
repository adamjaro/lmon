
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
#include "TagRecoRP.h"
#include "TagCounter.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
int main(int argc, char* argv[]) {

  //configuration file
  program_options::options_description opt("opt");
  opt.add_options()
    ("main.input", program_options::value<string>(), "Analysis input")
  ;

  //reconstruction for tagger stations
  TagRecoRP s1_rec("s1", &opt);

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

  //initialize the reconstruction
  s1_rec.Initialize(&opt_map);

  GeoParser geo("../../config/rp1/geom_rp1.in");

  //outputs
  TFile out("tag_reco.root", "recreate"); // outfile.c_str()

  //interaction tree
  TTree otree("event", "event");

  //tagger stations
  TagCounter tag_s1("s1", &tree, &otree, &geo);

  //event loop
  Long64_t nev = tree.GetEntries();
  //Long64_t nev = 220;
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    tag_s1.ProcessEvent();

    if( tag_s1.GetIsHit() ) {
      s1_rec.AddInput(tag_s1.GetX(), tag_s1.GetY(), tag_s1.GetThetaX(), tag_s1.GetThetaY());
    }

    //s2.ProcessEvent();

    //otree.Fill();

  }//event loop

  cout << "All events: " << tree.GetEntries() << endl;



  s1_rec.WriteOutput();
  out.Close();

  return 0;

}//main




















