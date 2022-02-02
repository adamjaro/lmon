
//_____________________________________________________________________________
//
// Reconstruction for CaloBPC
//
//_____________________________________________________________________________

//C++
#include <iostream>
#include "glob.h"
#include <fstream>

//Boost
#include <boost/program_options.hpp>

//ROOT
#include "TChain.h"
#include "TTree.h"
#include "TFile.h"

//Geant
#include "G4String.hh"

//local classes
#include "CaloBPCHits.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
int main(int argc, char* argv[]) {

  //configuration file
  program_options::options_description opt("opt");
  opt.add_options()
    ("main.input", program_options::value<string>(), "Analysis input")
    ("main.outfile", program_options::value<string>(), "Output from the analysis")
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

  //BPC hits
  CaloBPCHits hits;
  hits.ConnectInput("bpc", &tree);

  //output tree
  string outfile = opt_map["main.outfile"].as<string>();
  outfile.erase(remove(outfile.begin(), outfile.end(), '\"'), outfile.end());
  cout << "Output: " << outfile << endl;

  //event loop
  Long64_t nev = tree.GetEntries();
  Long64_t iprint = nev>12 ? nev/12: 12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);
    hits.LoadHits();

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    cout << "Next event" << endl;

    //hit loop
    for(unsigned long i=0; i<hits.GetNhits(); i++) {

      const CaloBPCHits::Hit& hit = hits.GetHit(i);

      cout << i << " " << hit.vert << " " << hit.x << " " << hit.y << " " << hit.en << endl;

    }//hit loop

  }//event loop

  return 0;

}//main



























