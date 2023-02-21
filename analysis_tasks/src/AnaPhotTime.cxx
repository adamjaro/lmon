
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
#include "PhotoHitsV2.h"
#include "CalPWOHits.h"

using namespace std;
using namespace boost;
using namespace boost::program_options;

//_____________________________________________________________________________
void AnaPhotTime::Run(const char *conf) {

  cout << "AnaPhotTime::Run" << endl;

  //configuration file
  options_description opt("opt");
  opt.add_options()
    ("main.input", program_options::value<string>(), "Analysis input")
    ("main.outfile", program_options::value<string>(), "Output from the analysis")
  ;

  //load the configuration file
  variables_map opt_map;
  store(parse_config_file(conf, opt), opt_map);

  //inputs
  string input = GetStr(opt_map, "main.input");
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
  PhotoHitsV2::Coll hits;
  hits.ConnectInput("pwo_cath", &tree);

  //tower cell hits
  CalPWOHits::Coll cell_hits;
  cell_hits.ConnectInput("pwo", &tree);

  //outputs
  string outfile = GetStr(opt_map, "main.outfile");
  cout << "Output: " << outfile << endl;
  TFile out(outfile.c_str(), "recreate");

  //hit output tree
  TTree hit_tree("hits", "hits");
  Double_t hit_time;
  hit_tree.Branch("hit_time", &hit_time, "hit_time/D");

  //event loop
  Long64_t nev = tree.GetEntries();
  Long64_t iprint = nev>12 ? nev/12 : 1;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    //load the hits
    hits.LoadInput();
    cell_hits.LoadInput();

    cout << "PMT hits: " << hits.GetN() << endl;

    //hit loop
    for(auto it = hits.read_begin(); it != hits.read_end(); ++it) {

      PhotoHitsV2::Hit hit = *it;

      cout << "PhotoHit: " << hit.time << " " << hit.pos_x << " " << hit.pos_y << " " << hit.pos_z << endl;
      //cout << hit.cell_id << " " << hit.prim_id << " " << hit.pmt_x << " " << hit.pmt_y << " " << hit.pmt_z << endl;

      //set the hit output
      hit_time = hit.time;
      hit_tree.Fill();
    }//hit loop

    cout << "Cell hits: " << cell_hits.GetN() << endl;

    //cell hit loop
    for(unsigned int ihit = 0; ihit < cell_hits.GetN(); ihit++) {

      CalPWOHits::Hit hit = cell_hits.GetUnit(ihit);

      cout << "CalPWOHit: " << hit.cell_id << " " << hit.en << endl;

    }//cell hit loop


  }//event loop

  hit_tree.Write();

  out.Close();

}//Run

//_____________________________________________________________________________
string AnaPhotTime::GetStr(program_options::variables_map& opt_map, std::string par) {

  string res = opt_map[par].as<string>();
  res.erase(remove(res.begin(), res.end(), '\"'), res.end());

  return res;

}//GetStr















