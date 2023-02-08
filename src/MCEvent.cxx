
//ROOT
#include "TTree.h"

//Geant
#include "G4Event.hh"
#include "G4SystemOfUnits.hh"

//local classes
#include "MCEvent.h"

//_____________________________________________________________________________
MCEvent::MCEvent(): Detector(), fNam("MCEvent") {

}//MCEvent

//_____________________________________________________________________________
void MCEvent::BeginEvent(const G4Event *evt) {

  //generator data
  ReadEvtDat(evt);

  //G4cout << "MCEvent::BeginEvent: " << evt->GetNumberOfPrimaryVertex() << G4endl;

}//BeginEvent

//_____________________________________________________________________________
void MCEvent::ReadEvtDat(const G4Event *evt) {

  //generator data

  MCEvtDat *dat = dynamic_cast<MCEvtDat*>(evt->GetUserInformation());
  if(!dat) return;

  //load the input data
  fDat.LoadGenVal(*dat);

  //fDat.Print("MCEvent power:", "power_W");
  //G4cout << G4endl;

}//ReadEvtDat















