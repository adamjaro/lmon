
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

  //load the configuration file
  if(argc < 2) {
    cout << "No configuration specified." << endl;
    return -1;
  }
  ifstream config(argv[1]);
  program_options::variables_map opt_map;
  program_options::store(program_options::parse_config_file(config, opt), opt_map);

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
  vector<Int_t> *gen_pdg = 0x0;
  vector<Float_t> *gen_en = 0x0;
  tree.SetBranchAddress("gen_pdg", &gen_pdg);
  tree.SetBranchAddress("gen_en", &gen_en);
  Double_t true_phot_theta, true_phot_phi, true_phot_E;
  tree.SetBranchAddress("true_phot_theta", &true_phot_theta);
  tree.SetBranchAddress("true_phot_phi", &true_phot_phi);
  tree.SetBranchAddress("true_phot_E", &true_phot_E);

  //geometry
  string geo_nam = get_str(opt_map, "main.geo");
  cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

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

  //detector outputs
  up.CreateOutput();
  down.CreateOutput();

  //interaction tree
  TTree otree("event", "event");
  otree.Branch("true_phot_theta", &true_phot_theta, "true_phot_theta/D");
  otree.Branch("true_phot_phi", &true_phot_phi, "true_phot_phi/D");
  otree.Branch("true_phot_E", &true_phot_E, "true_phot_E/D");
  Bool_t up_hit, down_hit, is_spect;
  Double_t up_x, up_y, up_z, up_tx, up_ty, up_calE;
  Double_t down_x, down_y, down_z, down_tx, down_ty, down_calE;
  Double_t phot_en;
  otree.Branch("up_hit", &up_hit, "up_hit/O");
  otree.Branch("down_hit", &down_hit, "down_hit/O");
  otree.Branch("is_spect", &is_spect, "is_spect/O");
  otree.Branch("up_x", &up_x, "up_x/D");
  otree.Branch("up_y", &up_y, "up_y/D");
  otree.Branch("up_z", &up_z, "up_z/D");
  otree.Branch("up_tx", &up_tx, "up_tx/D");
  otree.Branch("up_ty", &up_ty, "up_ty/D");
  otree.Branch("up_calE", &up_calE, "up_calE/D");
  otree.Branch("down_x", &down_x, "down_x/D");
  otree.Branch("down_y", &down_y, "down_y/D");
  otree.Branch("down_z", &down_z, "down_z/D");
  otree.Branch("down_tx", &down_tx, "down_tx/D");
  otree.Branch("down_ty", &down_ty, "down_ty/D");
  otree.Branch("down_calE", &down_calE, "down_calE/D");
  otree.Branch("phot_en", &phot_en, "phot_en/D");

  //event loop
  Long64_t nev = tree.GetEntries();
  //Long64_t nev = 220;
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    //generated photon energy
    for(unsigned long imc=0; imc<gen_pdg->size(); imc++) {
      if( gen_pdg->at(imc) == 22 ) phot_en = gen_en->at(imc);
    }

    up_hit = up.IsHit();
    down_hit = down.IsHit();
    is_spect = up_hit and down_hit;

    up_x = up.GetX();
    up_y = up.GetY();
    up_z = up.GetZ();
    up_tx = up.GetThetaX();
    up_ty = up.GetThetaY();
    up_calE = up.GetCalE();

    down_x = down.GetX();
    down_y = down.GetY();
    down_z = down.GetZ();
    down_tx = down.GetThetaX();
    down_ty = down.GetThetaY();
    down_calE = down.GetCalE();

    otree.Fill();

  }//event loop

  cout << "All events: " << tree.GetEntries() << endl;

  up.WriteOutputs();
  down.WriteOutputs();
  otree.Write();
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



