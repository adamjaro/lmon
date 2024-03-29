
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
    ("main.input_resp", program_options::value<string>(), "Response input for reconstruction")
    ("main.up_y_min", program_options::value<double>(), "Minimal up y")
    ("main.down_y_max", program_options::value<double>(), "Maximal down y")
  ;

  //load the configuration file
  if(argc < 2) {
    cout << "No configuration specified." << endl;
    return -1;
  }
  ifstream config(argv[1]);
  program_options::variables_map opt_map;
  program_options::store(program_options::parse_config_file(config, opt), opt_map);

  //data input for reconstruction
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

  Double_t up_y_min=-9e9, down_y_max=9e9;
  if( opt_map.find("main.up_y_min") != opt_map.end() ) {
    up_y_min = opt_map["main.up_y_min"].as<double>();
    cout << "up_y_min: " << up_y_min << endl;
  }
  if( opt_map.find("main.down_y_max") != opt_map.end() ) {
    down_y_max = opt_map["main.down_y_max"].as<double>();
    cout << "down_y_max: " << down_y_max << endl;
  }

  //import the response for reconstruction
  string input_resp = get_str(opt_map, "main.input_resp");
  cout << "Response input: " << input_resp << endl;
  TFile in_resp(input_resp.c_str(), "read");
  EThetaPhiReco spec_rec("spec");
  spec_rec.Import(&in_resp);

  //outputs
  string outfile = get_str(opt_map, "main.outfile");
  cout << "Output: " << outfile << endl;
  TFile out(outfile.c_str(), "recreate");

  //output from reconstruction
  spec_rec.CreateRecoOutput();
  spec_rec.AddOutputBranch("true_phot_E", &true_phot_E);
  spec_rec.AddOutputBranch("true_phot_theta", &true_phot_theta);
  spec_rec.AddOutputBranch("true_phot_phi", &true_phot_phi);
  Double_t quant[10];
  spec_rec.AddOutputBranch("up_x", &quant[0]); // xup
  spec_rec.AddOutputBranch("down_x", &quant[1]); // xdown
  spec_rec.AddOutputBranch("up_y", &quant[2]); // yup
  spec_rec.AddOutputBranch("down_y", &quant[3]); // ydown
  spec_rec.AddOutputBranch("up_tx", &quant[4]); // txup
  spec_rec.AddOutputBranch("down_tx", &quant[5]); // txdown
  spec_rec.AddOutputBranch("up_ty", &quant[6]); // tyup
  spec_rec.AddOutputBranch("down_ty", &quant[7]); // tydown
  spec_rec.AddOutputBranch("up_calE", &quant[8]); // eup
  spec_rec.AddOutputBranch("down_calE", &quant[9]); // edown

  //interaction tree
  TTree otree("event", "event");
  Bool_t up_hit, down_hit, is_spect, is_rec;
  otree.Branch("up_hit", &up_hit, "up_hit/O");
  otree.Branch("down_hit", &down_hit, "down_hit/O");
  otree.Branch("is_spect", &is_spect, "is_spect/O");
  otree.Branch("is_rec", &is_rec, "is_rec/O");
  otree.Branch("true_phot_theta", &true_phot_theta, "true_phot_theta/D");
  otree.Branch("true_phot_phi", &true_phot_phi, "true_phot_phi/D");
  otree.Branch("true_phot_E", &true_phot_E, "true_phot_E/D");

  //event loop
  Long64_t nev = tree.GetEntries();
  //Long64_t nev = 220;
  Long64_t iprint = nev/12;
  Long64_t nrec=0;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    //hits in spectrometers
    up_hit = up.IsHit();
    down_hit = down.IsHit();

    //spectrometer coincidence
    is_spect = up_hit and down_hit;

    if( up_hit and up.GetY() < up_y_min ) is_spect = kFALSE;

    if( down_hit and down.GetY() > down_y_max ) is_spect = kFALSE;

    is_rec = kFALSE;

    //proceed with reconstruction only for spectrometer coincidence
    if( is_spect ) {

      //measured quantities, same order as they were created by MakeQuantity
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

      //run the reconstruction
      is_rec = spec_rec.Reconstruct(quant);

      nrec++;
    }

    //fill the interaction tree
    otree.Fill();

  }//event loop

  cout << "All events: " << tree.GetEntries() << endl;
  cout << "Reconstructed events: " << nrec << endl;

  spec_rec.WriteRecoOutput();
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









