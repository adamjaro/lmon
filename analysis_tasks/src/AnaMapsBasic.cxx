
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
#include "G4Step.hh"
#include "G4String.hh"

//local classes
#include "TrkMapsBasicHits.h"
#include "GeoParser.h"
#include "AnaMapsBasic.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
void AnaMapsBasic::Run(const char *conf) {

  //configuration file
  program_options::options_description opt("opt");
  opt.add_options()
    ("main.input", program_options::value<string>(), "Analysis input")
    ("main.geo", program_options::value<string>(), "Geometry configuration")
    ("main.outfile", program_options::value<string>(), "Output from the analysis")
  ;

  //load the configuration file
  ifstream config(conf);
  program_options::variables_map opt_map;
  program_options::store(program_options::parse_config_file(config, opt), opt_map);

  //inputs
  string input = GetStr(opt_map, "main.input");
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
  string geo_nam = GetStr(opt_map, "main.geo");
  cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

  //threshold for hits
  Double_t en_min = 0.4; // keV

  //first layers for both taggers
  TrkMapsBasicHits s1A, s2A;
  s1A.ConnectInput("lowQ2_s1A", &tree);
  s2A.ConnectInput("lowQ2_s2A", &tree);
  s1A.LocalFromGeo("vac_B2Q3", &geo); // local coordinates from geometry
  s2A.LocalFromGeo("vac_B2Q3", &geo);
  s1A.SetXPos( s1A.GetXPos() + geo.GetD("lowQ2_s1A", "xpos") ); // correction for plane position in its volume
  s2A.SetXPos( s2A.GetXPos() + geo.GetD("lowQ2_s2A", "xpos") );

  //outputs
  string outfile = GetStr(opt_map, "main.outfile");
  cout << "Output: " << outfile << endl;
  TFile out(outfile.c_str(), "recreate");

  //hit trees
  TTree hs1A("hs1A", "hs1A");
  Double_t x1A, y1A, z1A, en1A;
  Int_t pdg1A, id1A;
  hs1A.Branch("x1A", &x1A, "x1A/D");
  hs1A.Branch("y1A", &y1A, "y1A/D");
  hs1A.Branch("z1A", &z1A, "z1A/D");
  hs1A.Branch("en1A", &en1A, "en1A/D");
  hs1A.Branch("pdg1A", &pdg1A, "pdg1A/I");
  hs1A.Branch("id1A", &id1A, "id1A/I");

  TTree hs2A("hs2A", "hs2A");
  Double_t x2A, y2A, z2A, en2A;
  Int_t pdg2A, id2A;
  hs2A.Branch("x2A", &x2A, "x2A/D");
  hs2A.Branch("y2A", &y2A, "y2A/D");
  hs2A.Branch("z2A", &z2A, "z2A/D");
  hs2A.Branch("en2A", &en2A, "en2A/D");
  hs2A.Branch("pdg2A", &pdg2A, "pdg2A/I");
  hs2A.Branch("id2A", &id2A, "id2A/I");

  //interaction tree
  TTree otree("event", "event");
  Int_t n1A, n2A;
  otree.Branch("n1A", &n1A, "n1A/I");
  otree.Branch("n2A", &n2A, "n2A/I");

  //event loop
  Long64_t nev = tree.GetEntries();
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    s1A.LoadHits();
    s2A.LoadHits();

    s1A.GlobalToLocal();
    s2A.GlobalToLocal();

    n1A = 0;
    n2A = 0;

    //hits loop for tagger 1
    //cout << "s1A: " << s1A.GetNhits() << endl;
    for(unsigned long ihit=0; ihit<s1A.GetNhits(); ihit++) {

      const TrkMapsBasicHits::Hit& hit = s1A.GetHit(ihit);

      //energy threshold
      if( hit.en < en_min ) continue;

      n1A++;

      x1A = hit.x;
      y1A = hit.y;
      z1A = hit.z;
      en1A = hit.en;

      pdg1A = hit.pdg;
      id1A = hit.itrk;

      //cout << hit.pdg << " " << hit.x << " " << hit.y << " " << hit.z << " " << hit.en << endl;

      hs1A.Fill();

    }//hits loop for tagger 1

    //hits loop for tagger 2
    for(unsigned long ihit=0; ihit<s2A.GetNhits(); ihit++) {

      const TrkMapsBasicHits::Hit& hit = s2A.GetHit(ihit);

      //energy threshold
      if( hit.en < en_min ) continue;

      n2A++;

      x2A = hit.x;
      y2A = hit.y;
      z2A = hit.z;
      en2A = hit.en;

      pdg2A = hit.pdg;
      id2A = hit.itrk;

      hs2A.Fill();

    }//hits loop for tagger 2

    otree.Fill();

  }//event loop

  cout << "s1A hits: " << hs1A.GetEntries() << endl;
  cout << "s2A hits: " << hs2A.GetEntries() << endl;

  otree.Write();
  hs1A.Write();
  hs2A.Write();
  out.Close();

}//Run

//_____________________________________________________________________________
string AnaMapsBasic::GetStr(program_options::variables_map& opt_map, std::string par) {

  string res = opt_map[par].as<string>();
  res.erase(remove(res.begin(), res.end(), '\"'), res.end());

  return res;

}//GetStr



































