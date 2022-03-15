
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

  //geometry
  string geo_nam = get_str(opt_map, "main.geo");
  cout << "Geometry: " << geo_nam << endl;
  GeoParser geo(geo_nam);

  SpectDet up("up", "LumiSUbox", &tree, &geo);
  SpectDet down("down", "LumiSDbox", &tree, &geo);

  up.SetLayEmin(0.1);
  down.SetLayEmin(0.1);
  up.SetLayPdg(11);
  down.SetLayPdg(-11);

  //outputs
  string outfile = get_str(opt_map, "main.outfile");
  cout << "Output: " << outfile << endl;
  TFile out(outfile.c_str(), "recreate");

  up.CreateOutput();
  down.CreateOutput();

  //event loop
  Long64_t nev = tree.GetEntries();
  //Long64_t nev = 220;
  Long64_t iprint = nev/12;
  for(Long64_t iev=0; iev<nev; iev++) {
    tree.GetEntry(iev);

    if( iev > 0 and iev%iprint == 0 ) {
      //cout << Form("%.1f", 100.*iev/nev) << "%" << endl;
    }

    up.ProcessEvent();
    down.ProcessEvent();

  }//event loop

  cout << "All events: " << tree.GetEntries() << endl;

  up.WriteOutputs();
  down.WriteOutputs();
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



