
//C++
#include <fstream>
#include <string>
#include <boost/tokenizer.hpp>

//ROOT
#include "TFormula.h"

//Geant
#include "G4String.hh"
#include "G4ios.hh"
#include "globals.hh"

//local classes
#include "GeoParser.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
GeoParser::GeoParser(G4String input): fIncDir(".") {

  //default include directory for geometry inputs
  string in(input);
  if( in.find_last_of("/") != string::npos ) {
    fIncDir = in.substr(0, in.find_last_of("/"));
  }

  //main geometry input
  LoadInput(input);

}//GeoParser

//_____________________________________________________________________________
void GeoParser::LoadInput(G4String input) {

  //load geometry input

  G4cout << "GeoParser::LoadInput, " << input << G4endl;

  ifstream in(input);

  if(in.fail()) {
    string description = "Can't open input: '" + input + "'";
    G4Exception("GeoParser::LoadInput", "InputNotOpen01", FatalException, description.c_str());
  }

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

    tokenizer< char_separator<char> > cline(line, sep);
    token_it it = cline.begin();

    string cmd = *it;
    if( cmd == "include" ) {
      //another geometry file
      Include(it);

    } else if( cmd == "new" ) {
      //new detector
      AddNew(it);

    } else if( cmd == "const" ) {
      //constant in geometry
      AddConst(it);

    } else if( cmd == "inc_dir" ) {
      //include directory for geometry inputs
      fIncDir = *(++it);

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
  LoadInput(fIncDir+"/"+infile);

}//Include

//_____________________________________________________________________________
void GeoParser::AddNew(token_it &it) {

  //add new element

  G4String type = *(++it);
  G4String name = *(++it);

  fDet.push_back( make_pair(type, name) );

}//AddNew

//_____________________________________________________________________________
void GeoParser::AddConst(token_it &it) {

  //add new element

  G4String name = *(++it);
  G4String value = *(++it);

  fConst.insert( make_pair(name, Evaluate(value)) );

}//AddConst

//_____________________________________________________________________________
void GeoParser::AddPar(token_it &it) {

  //add new geometry parameter

  G4String nam = *it; // detector.parameter
  it++;
  G4String val = *(++it); // parameter value

  fPar.insert( make_pair(nam, Evaluate(val)) );

}//AddPar

//_____________________________________________________________________________
G4String GeoParser::Evaluate(G4String val) {

  val = val.strip(G4String::both, '"'); // remove string quote characters

  //parse for possible constants
  tokenizer< char_separator<char> > val_sep(val, char_separator<char>("", "+-*/()"));
  int ntok = 0;
  stringstream ss;
  for(token_it i = val_sep.begin(); i != val_sep.end(); i++) {

    string ival = *i;

    //substitute the constant if present
    map<string, string>::iterator iconst = fConst.find(ival);
    if(iconst != fConst.end()) {
      ival = (*iconst).second;
    }

    ss << ival;
    ntok++;
  }

  //arithmetic expression
  if(ntok > 1) {
    TFormula form("form", ss.str().c_str(), false);

    ss.str("");
    ss.precision(16);
    ss << scientific << form.Eval(0);
  }

  return ss.str();

}//Evaluate

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
template<typename par_type> bool GeoParser::GetOptPar(G4String name, G4String par, par_type& val) {

  //get value 'val' for optional parameter 'par' as par_type for detector named 'name'

  map<G4String, G4String>::iterator ival;
  ival = fPar.find(name+"."+par);

  if( ival == fPar.end() ) return false;

  istringstream st( (*ival).second );
  st >> val;

  return true;

}//GetOptPar

//_____________________________________________________________________________
G4bool GeoParser::GetOptD(G4String name, G4String par, G4double& val, const Unit& un) {

  //optional G4double parameter

  if( !GetOptPar<G4double>(name, par, val) ) return false;

  //apply the units if provided
  if(un.apply) val *= un.u;

  return true;

}//GetOptD

//_____________________________________________________________________________
G4bool GeoParser::GetOptI(G4String name, G4String par, G4int& val) {

  //optional G4int parameter

  return GetOptPar<G4int>(name, par, val);

}//GetOptI

//_____________________________________________________________________________
G4bool GeoParser::GetOptB(G4String name, G4String par, G4bool& val) {

  //optional G4bool parameter

  return GetOptPar<G4bool>(name, par, val);

}//GetOptI

//_____________________________________________________________________________
G4bool GeoParser::GetOptS(G4String name, G4String par, G4String& val) {

  //optional G4String parameter

  return GetOptPar<G4String>(name, par, val);

}//GetOptI

//_____________________________________________________________________________
G4String GeoParser::GetConst(std::string nam) {

  //retrieve the value of the constant for geometry development

  map<string, string>::iterator iconst = fConst.find(nam);
  if(iconst == fConst.end()) {
    return "";
  }

  return (*iconst).second;

}//GetConst







