
//_____________________________________________________________________________
//
// generator reader for TX events according to specification here:
// https://www.star.bnl.gov/public/comp/simu/newsite/gstar/Manual/txformat.html
// selects only the gamma for now
//_____________________________________________________________________________

//C++ headers
#include <string.h>
#include <sstream>
#include <vector>
#include <map>
#include <boost/tokenizer.hpp>

//Geant headers
#include "G4GenericMessenger.hh"
#include "G4SystemOfUnits.hh"
#include "G4PrimaryVertex.hh"
#include "G4Event.hh"

//local headers
#include "TxReader.h"
#include "GenParticle.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
TxReader::TxReader() : G4VUserPrimaryGeneratorAction(), fIev(0) {

  //default input name
  fInputName = "../lgen_5x41_0p5min_12evt.tx";

  //command for name of input file
  fMsg = new G4GenericMessenger(this, "/lmon/input/");
  fMsg->DeclareProperty("name", fInputName);

}//TxReader

//_____________________________________________________________________________
void TxReader::GeneratePrimaries(G4Event *evt) {

  //open TX input
  if(!fIn.is_open()) OpenInput();

  //load the next TX event
  string line;
  while( line.find("EVENT") == string::npos ) {

    if( !fIn.good() ) {
      G4cout << "TxReader::GeneratePrimaries: no more events" << G4endl;
      return;
    }

    getline(fIn, line);
    //G4cout << line << G4endl;
  }

  //increment event count for progress printout
  fIev++;
  if( fIev%100000 == 0 ) {
    G4cout << "TxReader::GeneratePrimaries, event number: " << fIev << G4endl;
  }

  //get vertex coordinates, cm, and number of particles
  getline(fIn, line);
  G4double vx, vy, vz; // cm
  int ntrk; // number of particles
  ReadVertex(line, vx, vy, vz, ntrk); // read from the vertex line

  //G4cout << line << G4endl;
  //G4cout << "TxReader::GeneratePrimaries " << vx << " " << vy << " " << vz << " " << ntrk << G4endl;

  //make the primary vertex
  G4PrimaryVertex *vtx = new G4PrimaryVertex(vx*cm, vy*cm, vz*cm, 0);

  //tracks in event
  vector<GenParticle> tracks;

  //particle loop
  for(int itrk=0; itrk<ntrk; itrk++) {

    getline(fIn, line);
    tracks.push_back( GenParticle(line) );
  }//particle loop

  //put tracks to map according to pdg
  map<G4int, GenParticle*> tmap;
  for(vector<GenParticle>::iterator i = tracks.begin(); i != tracks.end(); i++) {

    //put the electron
    if( (*i).GetPdg() == 11 ) tmap.insert( make_pair(11, &(*i)) );

    //photon
    if( (*i).GetPdg() == 22 ) tmap.insert( make_pair(22, &(*i)) );

    //G4cout << "TxReader::GeneratePrimaries: " << (*i).GetPdg() << G4endl;
  }

  //G4cout << "TxReader::GeneratePrimaries: " << tmap[11]->GetPdg() << " " << tmap[22]->GetPdg() << G4endl;

  //generate the photon
  //tmap[22]->GenerateToVertex(vtx);

  //scattered electron
  tmap[11]->GenerateToVertex(vtx);

  //put vertex to the event
  evt->AddPrimaryVertex(vtx);

}//GeneratePrimaries

//_____________________________________________________________________________
void TxReader::ReadVertex(const std::string& line, G4double& vx, G4double& vy, G4double& vz, int& ntrk) {

  //vertex coordinates and number of tracks

  //split the vertex line
  tokenizer< char_separator<char> > vtxline(line, char_separator<char>(" "));
  tokenizer< char_separator<char> >::iterator vtx_it = vtxline.begin();

  //get vertex coordinates, cm
  stringstream ss;
  ++vtx_it;
  ss << *(vtx_it++) << " " << *(vtx_it++) << " " << *(vtx_it++);
  ss >> vz >> vy >> vx;

  //get number of particles
  for(int i=0; i<4; i++) ++vtx_it;
  ss.str("");
  ss.clear();
  ss << *(vtx_it++);
  ss >> ntrk;

}//ReadVertex

//_____________________________________________________________________________
void TxReader::OpenInput() {

  //open the input file

  G4cout << "TxReader::OpenInput: " << fInputName << G4endl;
  fIn.open(fInputName);

  //test if file exists
  if(fIn.fail()) {
    string description = "Can't open input: " + fInputName;
    G4Exception("TxReader::OpenInput", "InputNotOpen01", FatalException, description.c_str());
  }

}//OpenInput


















