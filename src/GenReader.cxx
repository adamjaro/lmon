
//_____________________________________________________________________________
//
// generator reader
//
//_____________________________________________________________________________

//C++

//Geant
#include "G4GenericMessenger.hh"
#include "G4Event.hh"
#include "G4ParticleGun.hh"

//local classes
#include "GenReader.h"
#include "TxReader.h"
#include "Pythia6Reader.h"
#include "TParticleReader.h"
#include "HepMC3Reader.h"

using namespace std;

//_____________________________________________________________________________
GenReader::GenReader() : G4VUserPrimaryGeneratorAction(), fGenType("tx"), fGen(0) {

  //command for generator reader type
  fMsg = new G4GenericMessenger(this, "/lmon/input/");
  fMsg->DeclareProperty("type", fGenType);

  //prepare the generators
  fGenAll.insert( make_pair("tx", new TxReader()) );
  fGenAll.insert( make_pair("pythia6", new Pythia6Reader()) );
  fGenAll.insert( make_pair("tparticle", new TParticleReader()) );
  fGenAll.insert( make_pair("gun", new G4ParticleGun()) );
  fGenAll.insert( make_pair("hepmc", new HepMC3Reader()) );

}//GenReader

//_____________________________________________________________________________
GenReader::~GenReader() {

  delete fMsg;

}//~GenReader

//_____________________________________________________________________________
void GenReader::GeneratePrimaries(G4Event *evt) {

  //G4cout << "GenReader::GeneratePrimaries " << fGenType << G4endl;

  //select the reader at the first call
  if(!fGen) {
    map<G4String, G4VPrimaryGenerator*>::iterator igen = fGenAll.find(fGenType);
    if (igen == fGenAll.end()) return;

    fGen = (*igen).second;
  }

  //generate the event
  fGen->GeneratePrimaryVertex(evt);

}//GeneratePrimaries


















