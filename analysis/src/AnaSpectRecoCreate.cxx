
//C++
#include <iostream>
#include "glob.h"
#include <fstream>
#include <vector>

//Boost
#include <boost/program_options.hpp>

//ROOT
#include "TChain.h"
#include "TTree.h"
#include "TFile.h"

//local classes
#include "GeoParser.h"
#include "EThetaPhiReco.h"
#include "SpectDet.h"

using namespace std;
using namespace boost;

string get_str(program_options::variables_map& opt_map, string par);

//_____________________________________________________________________________
int main(int argc, char* argv[]) {

  //configuration file
  program_options::options_description opt("opt");
  opt.add_options()
    ("main.input", program_options::value<string>(), "Analysis input")
    ("main.geo", program_options::value<string>(), "Geometry configuration")
    ("main.outfile", program_options::value<string>(), "Output from the analysis")
  ;

  //reconstruction for the spectrometer
  EThetaPhiReco spec_rec("spec", &opt);

  //quantities measured by the spectrometer
  spec_rec.MakeQuantity("xup"); // x position, mm
  spec_rec.MakeQuantity("xdown");

  spec_rec.MakeQuantity("yup"); // y position, mm
  spec_rec.MakeQuantity("ydown");

  spec_rec.MakeQuantity("txup", 1e-3); // theta_x angle, range in mrad, conversion to rad
  spec_rec.MakeQuantity("txdown", 1e-3);

  spec_rec.MakeQuantity("tyup", 1e-3); // theta_y angle, range in mrad, conversion to rad
  spec_rec.MakeQuantity("tydown", 1e-3);

  spec_rec.MakeQuantity("eup"); // calorimeter energy, GeV
  spec_rec.MakeQuantity("edown");

  //load the configuration file
  if(argc < 2) {
    cout << "No configuration specified." << endl;
    return -1;
  }
  ifstream config(argv[1]);
  program_options::variables_map opt_map;
  program_options::store(program_options::parse_config_file(config, opt), opt_map);

  //initialize the reconstruction
  spec_rec.Initialize(&opt_map);

  //inputs
  string input = get_str(opt_map, "main.input");
  cout << "Input: " << input << endl;
  glob_t glob_inputs;
  glob(input.c_str(), GLOB_TILDE, NULL, &glob_inputs);

  //input tree
  TChain tree("DetectorTree");
  for(size_t i=0; i<glob_inputs.gl_pathc; i++) {
    cout << "Adding input: " << glob_inputs.gl_pathv[i] << endl;
    tree.Add( glob_inputs.gl_pathv[i] );
  }

  //MC data
  Double_t true_phot_theta, true_phot_phi, true_phot_E;
  tree.SetBranchAddress("true_phot_theta", &true_phot_theta);
  tree.SetBranchAddress("true_phot_phi", &true_phot_phi);
  tree.SetBranchAddress("true_phot_E", &true_phot_E);

  //geometry
  string geo_nam = get_str(opt_map, "main.geo");
  cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

  //spectrometer detectors
  SpectDet up("up", "LumiSUbox", &tree, &geo);
  SpectDet down("down", "LumiSDbox", &tree, &geo);

  //selection criteria
  up.SetLayEmin(0.1); // GeV
  up.SetLayPdg(11);
  up.SetCalEmin(0.02); // GeV

  down.SetLayEmin(0.1);
  down.SetLayPdg(-11);
  down.SetCalEmin(0.02);

  //outputs
  string outfile = get_str(opt_map, "main.outfile");
  cout << "Output: " << outfile << endl;
  TFile out(outfile.c_str(), "recreate");

  //event loop
  Long64_t nev = tree.GetEntries();
  //Long64_t nev = 220;
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    //spectrometer coincidence
    if( !up.IsHit() or !down.IsHit() ) continue;

    //measured quantities, same order as they were created by MakeQuantity
    Double_t quant[10];
    quant[0] = up.GetX(); // xup
    quant[1] = down.GetX(); // xdown
    quant[2] = up.GetY(); // yup
    quant[3] = down.GetY(); // ydown
    quant[4] = up.GetThetaX()*1e-3; // txup, from mrad to rad
    quant[5] = down.GetThetaX()*1e-3; // txdown
    quant[6] = up.GetThetaY()*1e-3; // tyup
    quant[7] = down.GetThetaY()*1e-3; // tydown
    quant[8] = up.GetCalE(); // eup
    quant[9] = down.GetCalE(); // edown

    //input for the response
    spec_rec.AddInput(quant, true_phot_E, true_phot_theta, true_phot_phi);

  }//event loop

  cout << "All events: " << tree.GetEntries() << endl;

  spec_rec.Export();
  out.Close();

  return 0;

}//main

//_____________________________________________________________________________
string get_str(program_options::variables_map& opt_map, string par) {

  //retrieve string value from input configuration

  string res = opt_map[par].as<string>();
  res.erase(remove(res.begin(), res.end(), '\"'), res.end());

  return res;

}//get_str








