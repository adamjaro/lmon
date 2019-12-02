
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
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"

//local headers
#include "LgenReader.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
LgenReader::LgenReader() : G4VUserPrimaryGeneratorAction() {

  //open lgen input
  string inp = "../lgen_5x41_12evt_evt.dat";
  //string inp = "/direct/eic+u/jadam/sim/lgen/data/lgen_18x275_1p2Mevt_evt.dat";
  fIn.open(inp.c_str());

  //skip the header, 6 lines
  string line;
  for(int i=0; i<6; i++) {
    getline(fIn, line);
  }

  //gamma definition for the generator
  fGammaDef = G4ParticleTable::GetParticleTable()->FindParticle("gamma");

}//LgenReader

//_____________________________________________________________________________
void LgenReader::GeneratePrimaries(G4Event *evt) {

  //read the lgen event

  char_separator<char> sep(" ");
  string line;
  double px, py, pz;
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

    //select only final state photon
    if( pdg != 22 || stat != 1 ) continue;

    //get photon momentum
    for(int i=0; i<3; i++) ++trk_it;
    ss.str("");
    ss.clear();
    ss << *(trk_it++) << " " << *(trk_it++) << " " << *(trk_it++);
    ss >> pz >> py >> px;

  }//event loop

  //generate the photon
  G4ParticleGun gun(fGammaDef);
  gun.SetParticleMomentum(G4ParticleMomentum(px*GeV, py*GeV, pz*GeV));

  gun.GeneratePrimaryVertex(evt);

}//GeneratePrimaries




















