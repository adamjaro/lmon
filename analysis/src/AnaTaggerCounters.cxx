
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
#include "ParticleCounterHits.h"

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

  //geometry
  string geo_nam = opt_map["main.geo"].as<string>();
  geo_nam.erase(remove(geo_nam.begin(), geo_nam.end(), '\"'), geo_nam.end());
  cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

  //counter hits
  ParticleCounterHits hits_tag1, hits_tag2;
  hits_tag1.ConnectInput("lowQ2s1", &tree);
  hits_tag1.LocalFromGeo("Tagger1box", &geo);
  hits_tag2.ConnectInput("lowQ2s2", &tree);
  hits_tag2.LocalFromGeo("Tagger2box", &geo);

  //input true kinematics
  Double_t true_x, true_y, true_Q2, true_el_pT, true_el_theta, true_el_phi, true_el_E;
  tree.SetBranchAddress("true_x", &true_x);
  tree.SetBranchAddress("true_y", &true_y);
  tree.SetBranchAddress("true_Q2", &true_Q2);
  tree.SetBranchAddress("true_el_pT", &true_el_pT);
  tree.SetBranchAddress("true_el_theta", &true_el_theta);
  tree.SetBranchAddress("true_el_phi", &true_el_phi);
  tree.SetBranchAddress("true_el_E", &true_el_E);

  //output trees
  string outfile = opt_map["main.outfile"].as<string>();
  outfile.erase(remove(outfile.begin(), outfile.end(), '\"'), outfile.end());
  cout << "Output: " << outfile << endl;
  TFile out(outfile.c_str(), "recreate");

  //tagger trees
  TTree s1_out("s1", "s1");
  Double_t s1_en, s1_x, s1_y, s1_z;
  Int_t s1_pdg, s1_nhit;
  s1_out.Branch("en", &s1_en, "en/D");
  s1_out.Branch("x", &s1_x, "x/D");
  s1_out.Branch("y", &s1_y, "y/D");
  s1_out.Branch("z", &s1_z, "z/D");
  s1_out.Branch("pdg", &s1_pdg, "pdg/I");
  s1_out.Branch("nhit", &s1_nhit, "nhit/I");
  TTree s2_out("s2", "s2");
  Double_t s2_en, s2_x, s2_y, s2_z;
  Int_t s2_pdg, s2_nhit;
  s2_out.Branch("en", &s2_en, "en/D");
  s2_out.Branch("x", &s2_x, "x/D");
  s2_out.Branch("y", &s2_y, "y/D");
  s2_out.Branch("z", &s2_z, "z/D");
  s2_out.Branch("pdg", &s2_pdg, "pdg/I");
  s2_out.Branch("nhit", &s2_nhit, "nhit/I");

  //interaction tree
  TTree otree("event", "event");
  Bool_t s1_IsHit, s2_IsHit;
  otree.Branch("s1_IsHit", &s1_IsHit, "s1_IsHit/O");
  otree.Branch("s2_IsHit", &s2_IsHit, "s2_IsHit/O");
  otree.Branch("true_x", &true_x, "true_x/D");
  otree.Branch("true_y", &true_y, "true_y/D");
  otree.Branch("true_Q2", &true_Q2, "true_Q2/D");
  otree.Branch("true_el_pT", &true_el_pT, "true_el_pT/D");
  otree.Branch("true_el_theta", &true_el_theta, "true_el_theta/D");
  otree.Branch("true_el_phi", &true_el_phi, "true_el_phi/D");
  otree.Branch("true_el_E", &true_el_E, "true_el_E/D");

  //event loop
  Long64_t nev = tree.GetEntries();
  //Long64_t nev = 220;
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    s1_IsHit = kFALSE;
    s2_IsHit = kFALSE;

    //Tagger 1
    s1_nhit = 0;
    for(int ihit=0; ihit<hits_tag1.GetNHits(); ihit++) {

      ParticleCounterHits::CounterHit hit = hits_tag1.GetHit(ihit);

      if( hit.parentID != 0 ) continue;
      s1_nhit++;

      hit = hits_tag1.GlobalToLocal(hit);

      s1_en = hit.en;
      s1_x = hit.x;
      s1_y = hit.y;
      s1_z = hit.z;
      s1_pdg = hit.pdg;

      //cout << iev << " " << ihit << " " << hit.pdg  << " " << hit.parentID  << " " << hit.en << " ";
      //cout << iev << " " << hit.x << " " << hit.y << " " << hit.z << endl;

    }

    if( s1_nhit > 0 ) {
      s1_IsHit = kTRUE;
      s1_out.Fill();
    }

    //Tagger 2
    s2_nhit = 0;
    for(int ihit=0; ihit<hits_tag2.GetNHits(); ihit++) {

      ParticleCounterHits::CounterHit hit = hits_tag2.GetHit(ihit);

      if( hit.parentID != 0 ) continue;
      s2_nhit++;

      hit = hits_tag2.GlobalToLocal(hit);

      s2_en = hit.en;
      s2_x = hit.x;
      s2_y = hit.y;
      s2_z = hit.z;
      s2_pdg = hit.pdg;
    }

    if( s2_nhit > 0 ) {
      s2_IsHit = kTRUE;
      s2_out.Fill();
    }

    otree.Fill();

  }//event loop

  s1_out.Write();
  s2_out.Write();
  otree.Write();
  out.Close();

  cout << "All events: " << tree.GetEntries() << endl;
  cout << "Tagger 1:   " << s1_out.GetEntries() << endl;
  cout << "Tagger 2:   " << s2_out.GetEntries() << endl;

  return 0;

}//main

















