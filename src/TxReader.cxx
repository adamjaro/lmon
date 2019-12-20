
//_____________________________________________________________________________
//
// generator reader for TX events according to specification here:
// https://www.star.bnl.gov/public/comp/simu/newsite/gstar/Manual/txformat.html
// selects only the gamma for now
//_____________________________________________________________________________

//C++ headers
#include <string.h>
#include <sstream>
#include <boost/tokenizer.hpp>

//Geant headers
#include "G4GenericMessenger.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"

//local headers
#include "TxReader.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
TxReader::TxReader() : G4VUserPrimaryGeneratorAction() {

  //default input name
  fInputName = "../lgen_5x41_0p5min_12evt.tx";

  //command for name of input file
  fMsg = new G4GenericMessenger(this, "/lmon/input/");
  fMsg->DeclareProperty("name", fInputName);

  //gamma definition for the generator
  fGammaDef = G4ParticleTable::GetParticleTable()->FindParticle("gamma");

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

    G4cout << line << G4endl;
  }

  //get vertex coordinates
  getline(fIn, line);

  //split the vertex line
  char_separator<char> sep(" ");
  tokenizer< char_separator<char> > vtxline(line, sep);
  tokenizer< char_separator<char> >::iterator vtx_it = vtxline.begin();

  //get vertex coordinates, cm
  G4double vx, vy, vz; // cm
  stringstream ss;
  ++vtx_it;
  ss << *(vtx_it++) << " " << *(vtx_it++) << " " << *(vtx_it++);
  ss >> vz >> vy >> vx;

  //G4cout << line << G4endl;
  //G4cout << "TxReader::GeneratePrimaries " << vx << " " << vy << " " << vz << G4endl;

  //get number of particles
  for(int i=0; i<4; i++) ++vtx_it;
  ss.str("");
  ss.clear();
  ss << *(vtx_it++);
  int ntrk;
  ss >> ntrk;

  //G4cout << ntrk << G4endl;

  //get photon momentum
  G4double px, py, pz;

  //particle loop
  for(int itrk=0; itrk<ntrk; itrk++) {
    getline(fIn, line);

    //split the particle line
    tokenizer< char_separator<char> > trkline(line, sep);
    tokenizer< char_separator<char> >::iterator trk_it = trkline.begin();

    //get the momentum
    for(int i=0; i<2; i++) ++trk_it;
    ss.str("");
    ss.clear();
    ss << *(trk_it++) << " " << *(trk_it++) << " " << *(trk_it++);
    ss >> pz >> py >> px;

    //get pdg
    for(int i=0; i<3; i++) ++trk_it;
    ss.str("");
    ss.clear();
    ss << *(trk_it++);
    int pdg;
    ss >> pdg;

    //G4cout << line << G4endl;
    //G4cout << pdg << G4endl;

    //select the photon
    if(pdg == 22) break;

  }//particle loop

  //G4cout << "tx: " << px << " " << py << " " << pz << G4endl;

  //generate the photon
  G4ParticleGun gun(fGammaDef);

  gun.SetParticleMomentum(G4ParticleMomentum(px*GeV, py*GeV, pz*GeV));
  gun.SetParticlePosition(G4ThreeVector(vx*cm, vy*cm, vz*cm));

  gun.GeneratePrimaryVertex(evt);

  //G4cout << "TxReader::GeneratePrimaries " << vx << " " << vy << " " << vz << G4endl;

}//GeneratePrimaries

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


















