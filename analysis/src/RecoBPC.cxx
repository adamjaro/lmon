
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
#include "TMath.h"

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
    ("config", program_options::value<string>(), "Configuration file")
    ("main.input", program_options::value<string>(), "Analysis input")
    ("main.outfile", program_options::value<string>(), "Output from the analysis")
    ("main.W0", program_options::value<double>(), "Threshold for scintillator energy")
  ;

  //command line options
  program_options::variables_map opt_map;
  program_options::store(program_options::parse_command_line(argc, argv, opt), opt_map);

  //load the configuration file
  if( !opt_map.count("config") ) {
    cout << "No configuration specified." << endl;
    return -1;
  }
  ifstream config(opt_map["config"].as<string>());
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
  TFile out(outfile.c_str(), "recreate");

  TTree otree("bpc", "bpc");
  Double_t xrec; // reconstructed position in x, mm
  otree.Branch("xrec", &xrec, "xrec/D");

  //threshold for scintillator energy
  Double_t W0 = opt_map["main.W0"].as<double>();
  Double_t eW0 = TMath::Exp(-W0);
  cout << "W0, e^(-W0): " << W0 << ", " << eW0 << endl;

  //event loop
  Long64_t nev = tree.GetEntries();
  Long64_t iprint = nev>12 ? nev/12: 12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);
    hits.LoadHits();

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    //cout << "Next event" << endl;

    //total shower energy
    Double_t etot = 0.;
    for(unsigned long i=0; i<hits.GetNhits(); i++) {
      etot += hits.GetHit(i).en;
    }

    xrec = 0.;
    Double_t wsum = 0;

    //vertical hits loop
    for(unsigned long i=0; i<hits.GetNhits(); i++) {

      const CaloBPCHits::Hit& hit = hits.GetHit(i);

      //vertical only
      if( !hit.vert ) continue;

      //weitht for strips above the threshold
      Double_t wi = 0.;
      if( hit.en/etot > eW0 ) {
        wi = W0 + TMath::Log(hit.en/etot);
      }

      xrec += wi*hit.x;
      wsum += wi;

      //cout << i << " " << wi << endl;

      //cout << i << " " << hit.vert << " " << hit.x << " " << hit.y << " " << hit.en << endl;

    }//vertical hits loop

    xrec = xrec/wsum;

    otree.Fill();

  }//event loop

  otree.Write();
  out.Close();

  cout << "All events: " << nev << endl;

  return 0;

}//main



























