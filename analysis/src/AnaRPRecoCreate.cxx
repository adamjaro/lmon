
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
//#include "TagRecoRP.h"
#include "EThetaPhiReco.h"
#include "TagCounter.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
int main(int argc, char* argv[]) {

  //configuration file
  program_options::options_description opt("opt");
  opt.add_options()
    ("main.input", program_options::value<string>(), "Analysis input")
    ("main.output", program_options::value<string>(), "Output on reconstruction response")
    ("main.geo", program_options::value<string>(), "Geometry configuration")
  ;

  //reconstruction for tagger stations
  //TagRecoRP s1_rec("s1", &opt);
  //TagRecoRP s2_rec("s2", &opt);
  EThetaPhiReco s1_rec("s1", &opt);
  EThetaPhiReco s2_rec("s2", &opt);

  //quantities measured by the taggers
  s1_rec.MakeQuantity("x"); // x position, mm
  s1_rec.MakeQuantity("y"); // y position, mm
  s1_rec.MakeQuantity("tx", 1e-3); // theta_x angle, set in mrad, conversion to rad
  s1_rec.MakeQuantity("ty", 1e-3); // theta_y angle, mrad conversion to rad
  s2_rec.MakeQuantity("x");
  s2_rec.MakeQuantity("y");
  s2_rec.MakeQuantity("tx", 1e-3);
  s2_rec.MakeQuantity("ty", 1e-3);

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
  Double_t true_el_E, true_el_theta, true_el_phi;
  tree.SetBranchAddress("true_el_E", &true_el_E);
  tree.SetBranchAddress("true_el_theta", &true_el_theta);
  tree.SetBranchAddress("true_el_phi", &true_el_phi);

  //initialize the reconstruction
  s1_rec.Initialize(&opt_map);
  s2_rec.Initialize(&opt_map);

  //geometry
  string geo_nam = opt_map["main.geo"].as<string>();
  geo_nam.erase(remove(geo_nam.begin(), geo_nam.end(), '\"'), geo_nam.end());
  cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

  //output on reconstruction response
  string outfile = opt_map["main.output"].as<string>();
  outfile.erase(remove(outfile.begin(), outfile.end(), '\"'), outfile.end());
  cout << "Output: " << outfile << endl;
  TFile out(outfile.c_str(), "recreate");

  //interaction tree
  TTree otree("event", "event");

  //tagger stations
  TagCounter tag_s1("s1", &tree, &otree, &geo);
  TagCounter tag_s2("s2", &tree, &otree, &geo);

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
    tag_s2.ProcessEvent();

    if( tag_s1.GetIsHit() ) {
      //s1_rec.AddInput(tag_s1.GetX(), tag_s1.GetY(), tag_s1.GetThetaX(), tag_s1.GetThetaY(), true_el_E, true_el_theta, true_el_phi);
      Double_t quant[4]{tag_s1.GetX(), tag_s1.GetY(), tag_s1.GetThetaX(), tag_s1.GetThetaY()};
      s1_rec.AddInput(quant, true_el_E, true_el_theta, true_el_phi);
    }

    if( tag_s2.GetIsHit() ) {
      //s2_rec.AddInput(tag_s2.GetX(), tag_s2.GetY(), tag_s2.GetThetaX(), tag_s2.GetThetaY(), true_el_E, true_el_theta, true_el_phi);
      Double_t quant[4]{tag_s2.GetX(), tag_s2.GetY(), tag_s2.GetThetaX(), tag_s2.GetThetaY()};
      s2_rec.AddInput(quant, true_el_E, true_el_theta, true_el_phi);
    }

    //otree.Fill();

  }//event loop

  cout << "All events: " << tree.GetEntries() << endl;

  s1_rec.Export();
  s2_rec.Export();

  out.Close();

  return 0;

}//main




















