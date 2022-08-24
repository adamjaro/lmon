
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
#include "G4String.hh"

//local classes
#include "AnaPhotTime.h"
#include "PhotoHits.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
void AnaPhotTime::Run(const char*) {

  cout << "AnaPhotTime::Run" << endl;

  //configuration file will be here

  //inputs
  //string input = GetStr(opt_map, "main.input");
  string input = "/home/jaroslav/sim/lmon/calo/macro/PWO/pwo.root";
  cout << "Input: " << input << endl;
  glob_t glob_inputs;
  glob(input.c_str(), GLOB_TILDE, NULL, &glob_inputs);

  //input tree
  TChain tree("DetectorTree");
  for(size_t i=0; i<glob_inputs.gl_pathc; i++) {
    cout << "Adding input: " << glob_inputs.gl_pathv[i] << endl;
    tree.Add( glob_inputs.gl_pathv[i] );
  }

  cout << tree.GetName() << endl;

  //PMT hits
  PhotoHits hits;
  hits.ConnectInput("pwo_cath", &tree);

  //event loop
  Long64_t nev = tree.GetEntries();
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    cout << "Next event: " << iev << endl;

    hits.LoadHits();

    cout << "Hits: " << hits.GetNhits() << endl;

    //hit loop
    for(unsigned int ihit = 0; ihit < hits.GetNhits(); ihit++) {

      PhotoHits::Hit hit = hits.GetHit(ihit);

      cout << hit.time << " " << hit.pos_x << " " << hit.pos_y << " " << hit.pos_z << endl;

    }

  }//event loop

}//Run

















