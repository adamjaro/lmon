
//_____________________________________________________________________________
//
// generator reader
//
//_____________________________________________________________________________

//C++

//Geant
#include "G4GenericMessenger.hh"
#include "G4Event.hh"

//local classes
#include "GenReader.h"
#include "TxReader.h"
#include "Pythia6Reader.h"


//_____________________________________________________________________________
GenReader::GenReader() : G4VUserPrimaryGeneratorAction(), fGenType("tx"), fGen(0) {

  //command for generator reader type
  fMsg = new G4GenericMessenger(this, "/lmon/input/");
  fMsg->DeclareProperty("type", fGenType);

  fGenTX = new TxReader();
  fGenPy = new Pythia6Reader();

}//Pythia6Reader

//_____________________________________________________________________________
GenReader::~GenReader() {

  delete fMsg;

}//~GenReader

//_____________________________________________________________________________
void GenReader::GeneratePrimaries(G4Event *evt) {

  //G4cout << "GenReader::GeneratePrimaries " << fGenType << G4endl;

  //select the reader
  if(!fGen) {
    if(fGenType == "tx") {
      fGen = fGenTX;
    } else if (fGenType == "pythia6") {
      fGen = fGenPy;
    }
  }

  //generate the event
  fGen->GeneratePrimaryVertex(evt);

}//GeneratePrimaries


















