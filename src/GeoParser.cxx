
//C++
#include <fstream>
#include <string>
#include <boost/tokenizer.hpp>

//Geant
#include "G4String.hh"
#include "G4ios.hh"

//local classes
#include "GeoParser.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
void GeoParser::LoadInput(G4String input) {

  //load geometry input

  ifstream in(input);

  char_separator<char> sep(" ");
  string line;

  //input loop
  while( getline(in, line) ) {

    //remove leading white spaces
    if( line.find_first_not_of(" \t") != string::npos ) {
      line = line.substr( line.find_first_not_of(" \t") );
    }

    //skip comments and empty lines
    if(line.empty() || line.find("#") == 0) continue;

    //G4cout << "GeoParser::LoadInput: " << line << G4endl;

    tokenizer< char_separator<char> > cline(line, sep);
    token_it it = cline.begin();

    string cmd = *it;
    if( cmd == "include" ) {
      //another geometry file
      Include(it);

    } else if( cmd == "new" ) {
      //new detector
      AddNew(it);

    } else if( cmd.find(".") != string::npos ) {
      //detector parameter
      AddPar(it);

    }

  }//input loop

  in.close();

}//LoadInput

//_____________________________________________________________________________
void GeoParser::Include(token_it &it) {

  //include another geometry input

  G4String infile = *(++it);
  LoadInput(infile);

}//Include

//_____________________________________________________________________________
void GeoParser::AddNew(token_it &it) {

  //add new element

  G4String type = *(++it);
  G4String name = *(++it);

  fDet.push_back( make_pair(type, name) );

}//AddNew

//_____________________________________________________________________________
void GeoParser::AddPar(token_it &it) {

  //add new geometry parameter

  G4String nam = *it;
  it++;
  G4String val = *(++it);

  fPar.insert( make_pair(nam, val) );

}//AddPar

//_____________________________________________________________________________
const G4String& GeoParser::GetS(G4String name, G4String par) {

  //load geometry parameter 'par' as a string from the map for detector 'name'

  map<G4String, G4String>::iterator ival;
  ival = fPar.find(name+"."+par);

  return (*ival).second;

}//GetS

//_____________________________________________________________________________
template<typename par_type> par_type GeoParser::GetPar(G4String name, G4String par) {

  //get parameter 'par' value as par_type for detector named 'name'

  G4String sval = GetS(name, par);

  istringstream st(sval);
  par_type val;
  st >> val;

  return val;

}//GetPar

//_____________________________________________________________________________
G4double GeoParser::GetD(G4String name, G4String par) {

  return GetPar<G4double>(name, par);

}//GetD

//_____________________________________________________________________________
G4int GeoParser::GetI(G4String name, G4String par) {

  return GetPar<G4int>(name, par);

}//GetI













