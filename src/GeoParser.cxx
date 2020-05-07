
//C++
#include <fstream>
#include <string>
#include <boost/tokenizer.hpp>

//Geant
#include "G4String.hh"
#include "G4ios.hh"
#include "globals.hh"

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
G4String GeoParser::GetTopName() {

  vector< pair<G4String, G4String> >::reverse_iterator i = fDet.rbegin();
  while(i != fDet.rend()) {

    if( (*i).first == "top" ) return (*i).second;

    i++;
  }

  return "";

}//GetTopName

//_____________________________________________________________________________
const G4String& GeoParser::GetS(G4String name, G4String par) {

  //load geometry parameter 'par' as a string from the map for detector 'name'

  map<G4String, G4String>::iterator ival;
  ival = fPar.find(name+"."+par);

  if( ival == fPar.end() ) {
    //parameter not found
    string description = "Parameter '" + par + "' not found for '" + name + "'";
    G4Exception("GeoParser::GetS", "ParameterNotFound01", FatalException, description.c_str());
  }

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

//_____________________________________________________________________________
G4bool GeoParser::GetB(G4String name, G4String par) {

  return GetPar<G4bool>(name, par);

}//GetB

//_____________________________________________________________________________
template<typename par_type> void GeoParser::GetOptPar(G4String name, G4String par, par_type& val) {

  //get value 'val' for optional parameter 'par' as par_type for detector named 'name'

  map<G4String, G4String>::iterator ival;
  ival = fPar.find(name+"."+par);

  if( ival == fPar.end() ) return;

  istringstream st( (*ival).second );
  st >> val;

}//GetOptPar

//_____________________________________________________________________________
void GeoParser::GetOptD(G4String name, G4String par, G4double& val) {

  //optional G4double parameter

  GetOptPar<G4double>(name, par, val);

}//GetOptD

//_____________________________________________________________________________
void GeoParser::GetOptI(G4String name, G4String par, G4int& val) {

  //optional G4int parameter

  GetOptPar<G4int>(name, par, val);

}//GetOptI

//_____________________________________________________________________________
void GeoParser::GetOptB(G4String name, G4String par, G4bool& val) {

  //optional G4bool parameter

  GetOptPar<G4bool>(name, par, val);

}//GetOptI










