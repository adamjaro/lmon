
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
class plane {
public:

  //_____________________________________________________________________________
  plane(string nam, TTree *tree, GeoParser *geo): fNam(nam) {

    fHits.ConnectInput("lowQ2_"+fNam, tree);
    fHits.LocalFromGeo("vac_B2Q3", geo);
    fOfsX = geo->GetD("lowQ2_"+fNam, "xpos");

    ptree = new TTree(fNam.c_str(), fNam.c_str());
    ptree->Branch("x", &fX, "x/D");
    ptree->Branch("y", &fY, "y/D");
    ptree->Branch("z", &fZ, "Z/D");
  }//plane

  //_____________________________________________________________________________
  bool is_hit() {

    int nhit = 0;
    //hit loop
    for(int ihit=0; ihit<fHits.GetNHits(); ihit++) {

      ParticleCounterHits::CounterHit hit = fHits.GetHit(ihit);
      if( hit.parentID != 0 ) continue;

      hit = fHits.GlobalToLocal(hit);
      fX = hit.x - fOfsX;
      fY = hit.y;
      fZ = hit.z;
      nhit++;
    }//hit loop

    if( nhit <= 0 ) return false;

    ptree->Fill();
    return true;

  }//is_hit

  //_____________________________________________________________________________
  void write_outputs() {
    cout << "Plane " << fNam << ": " << ptree->GetEntries() << endl;
    ptree->Write();
  }//write_outputs

private:

  string fNam; // plane name
  ParticleCounterHits fHits; // hits for the plane
  TTree *ptree; // plane output tree
  Double_t fX; // x of primary hit, mm
  Double_t fY; // y of primary hit, mm
  Double_t fZ; // z of primary hit, mm
  Double_t fOfsX; // offset in local x position, mm

};//plane

//_____________________________________________________________________________
class tagger {
public:

  //_____________________________________________________________________________
  tagger(string nam, TTree *tree , TTree *otree, GeoParser *geo): fNam(nam),
      fIsHit(0), fNPlane(0) {

    //planes for the station, A, B and C
    fPlanes.push_back( new plane(fNam+"A", tree, geo) );
    fPlanes.push_back( new plane(fNam+"B", tree, geo) );
    fPlanes.push_back( new plane(fNam+"C", tree, geo) );

    //branches for output tree
    otree->Branch((fNam+"_IsHit").c_str(), &fIsHit, (fNam+"_IsHit/O").c_str());
    otree->Branch((fNam+"_NPlane").c_str(), &fNPlane, (fNam+"_NPlane/I").c_str());

  }//tagger

  //_____________________________________________________________________________
  void process_event() {

    fNPlane = 0;
    fIsHit = kTRUE;
    //planes loop
    for(unsigned int i=0; i<fPlanes.size(); i++) {

      fIsHit *= fPlanes[i]->is_hit();

      if( !fPlanes[i]->is_hit() ) continue;
      fNPlane++;
    }//planes loop

  }//process_event

  //_____________________________________________________________________________
  void write_outputs() {
    for_each(fPlanes.begin(), fPlanes.end(), mem_fun( &plane::write_outputs ));
  }//write_outputs

private:

  string fNam; // station name
  vector<plane*> fPlanes; // planes for the station
  Bool_t fIsHit; // flag for hit in station
  Int_t fNPlane; // number of planes with hit

};//tagger

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

  //tagger stations
  tagger s1("s1", &tree, &otree, &geo);
  tagger s2("s2", &tree, &otree, &geo);

  //event loop
  Long64_t nev = tree.GetEntries();
  //Long64_t nev = 220;
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    s1.process_event();
    s2.process_event();

    otree.Fill();

  }//event loop

  cout << "All events: " << tree.GetEntries() << endl;

  otree.Write();
  s1.write_outputs();
  s2.write_outputs();
  out.Close();

  return 0;

}//main
















