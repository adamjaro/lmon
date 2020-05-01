
//_____________________________________________________________________________
//
// generator reader for Pythia6 ascii (Lund) events
//
//_____________________________________________________________________________

//C++
#include <string.h>
#include <sstream>
#include <vector>
#include <boost/tokenizer.hpp>

//Geant
#include "G4GenericMessenger.hh"
#include "G4Event.hh"

//local classes
#include "Pythia6Reader.h"
#include "GenParticle.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
Pythia6Reader::Pythia6Reader() : G4VPrimaryGenerator() {

  //default input name
  //fInputName = "../lgen_5x41_12evt_evt.dat";
  fInputName = "../pythia6_pp_255.txt";

  //command for name of input file
  fMsg = new G4GenericMessenger(this, "/lmon/input/pythia6/");
  fMsg->DeclareProperty("name", fInputName);

  //pdg selection
  fMsg->DeclareMethod("select", &Pythia6Reader::AddSelectPdg);

}//Pythia6Reader

//_____________________________________________________________________________
Pythia6Reader::~Pythia6Reader() {

  delete fMsg;

}//~Pythia6Reader

//_____________________________________________________________________________
void Pythia6Reader::GeneratePrimaryVertex(G4Event *evt) {

  //open the input
  if(!fIn.is_open()) OpenInput();

  //read the event
  fParticles.clear();

  char_separator<char> sep(" ");
  string line;
  //event loop
  while( line.find("Event finished") == string::npos ) {
    getline(fIn, line);

    if( !fIn.good() ) {
      G4cout << "Pythia6Reader::GeneratePrimaries: no more events" << G4endl;
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
    int statKS, pdg;
    ss >> pdg >> statKS;

    //final particles only
    if( statKS != 1 ) continue;

    //select according to pdg if required
    if( fSelPdg.empty() != true && fSelPdg.find(pdg) == fSelPdg.end() ) continue;

    //G4cout << statKS << " " << pdg << G4endl;

    //skip to particle momentum
    for(int i=0; i<3; i++) ++trk_it;

    //add the particle
    fParticles.push_back( GenParticle(pdg) );
    fParticles.back().ReadFromPythia6(trk_it);

  }//event loop

  if( fParticles.size() == 0 ) return;

  //generate the particles
  G4PrimaryVertex *vtx = fParticles[0].MakePrimaryVertex();

  vector<GenParticle>::iterator i = fParticles.begin();
  while( i != fParticles.end() ) {
    (*i).GenerateToVertex(vtx);
    i++;
  }

  //put vertex to the event
  evt->AddPrimaryVertex(vtx);

}//GeneratePrimaries

//_____________________________________________________________________________
void Pythia6Reader::OpenInput() {

  //open the input file

  G4cout << "Pythia6Reader::OpenInput: " << fInputName << G4endl;
  fIn.open(fInputName);

  //test if file exists
  if(fIn.fail()) {
    string description = "Can't open input: " + fInputName;
    G4Exception("Pythia6Reader::OpenInput", "InputNotOpen01", FatalException, description.c_str());
  }

  //skip the header, 6 lines
  string line;
  for(int i=0; i<6; i++) {
    getline(fIn, line);
  }


}//OpenInput

//_____________________________________________________________________________
void Pythia6Reader::AddSelectPdg(G4int pdg) {

  //pdg selection

  //G4cout << "Pythia6Reader::AddSelectPdg " << pdg << G4endl;

  fSelPdg.insert(pdg);

}//AddSelectPdg
















