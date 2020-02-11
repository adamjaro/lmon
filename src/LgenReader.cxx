
//_____________________________________________________________________________
//
// generator reader for lgen / DJANGOH events,
// selects primary gamma for now
//_____________________________________________________________________________

//C++ headers
#include <string.h>
#include <sstream>
#include <boost/tokenizer.hpp>

//Geant headers
#include "G4GenericMessenger.hh"
#include "G4Event.hh"

//local headers
#include "LgenReader.h"
#include "GenParticle.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
LgenReader::LgenReader() : G4VUserPrimaryGeneratorAction() {

  //default input name
  fInputName = "../lgen_5x41_12evt_evt.dat";

  //command for name of input file
  fMsg = new G4GenericMessenger(this, "/lmon/input/");
  fMsg->DeclareProperty("name", fInputName);

  //generated particles
  fPhot = new GenParticle(22);
  fEl = new GenParticle(11);
  fBeamEl = new GenParticle(11);

}//LgenReader

//_____________________________________________________________________________
LgenReader::~LgenReader() {

  delete fMsg;
  delete fPhot;
  delete fEl;
  delete fBeamEl;

}//~LgenReader

//_____________________________________________________________________________
void LgenReader::GeneratePrimaries(G4Event *evt) {

  //open lgen input
  if(!fIn.is_open()) OpenInput();

  //read the lgen event

  char_separator<char> sep(" ");
  string line;
  //event loop
  while( line.find("Event finished") == string::npos ) {
    getline(fIn, line);

    if( !fIn.good() ) {
      G4cout << "LgenReader::GeneratePrimaries: no more events" << G4endl;
      return;
    }

    //split the line
    tokenizer< char_separator<char> > trkline(line, sep);
    tokenizer< char_separator<char> >::iterator trk_it = trkline.begin();

    //skip non-particle lines
    if( (*trk_it).find("=") == 0 || (*trk_it).find("0") == 0 ) continue;

    //get status code and pdg
    ++trk_it;
    stringstream ss;
    ss << *(trk_it++) << " " << *(trk_it++);
    int stat, pdg;
    ss >> pdg >> stat;

    //skip to particle momentum
    for(int i=0; i<3; i++) ++trk_it;

    //final state photon
    if( pdg == 22 && stat == 1 ) {
      fPhot->ReadFromPythia6(trk_it);
      continue;
    }

    //scattered electron
    if( pdg == 11 && stat == 1 ) {
      fEl->ReadFromPythia6(trk_it);
      continue;
    }

    //beam electron
    if( pdg == 11 && stat == 201 ) {
      fBeamEl->ReadFromPythia6(trk_it);
      continue;
    }

  }//event loop

  //generate the photon
  G4PrimaryVertex *vtx = fPhot->MakePrimaryVertex();
  fPhot->GenerateToVertex(vtx);

  //scattered electron
  fEl->GenerateToVertex(vtx);

  //beam electron
  //fBeamEl->GenerateToVertex(vtx);

  //put vertex to the event
  evt->AddPrimaryVertex(vtx);

}//GeneratePrimaries

//_____________________________________________________________________________
void LgenReader::OpenInput() {

  //open the input file

  G4cout << "LgenReader::OpenInput: " << fInputName << G4endl;
  fIn.open(fInputName);

  //test if file exists
  if(fIn.fail()) {
    string description = "Can't open input: " + fInputName;
    G4Exception("LgenReader::OpenInput", "InputNotOpen01", FatalException, description.c_str());
  }

  //skip the header, 6 lines
  string line;
  for(int i=0; i<6; i++) {
    getline(fIn, line);
  }


}//OpenInput


















