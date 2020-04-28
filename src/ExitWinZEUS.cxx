
//_____________________________________________________________________________
//
// exit window as an Al disc according to ZEUS, also demonstrator to write
// the detector as a branch to the output tree
//_____________________________________________________________________________

//C++
#include <string>

//ROOT
#include "Rtypes.h"
#include "TTree.h"

//Geant
#include "G4VSensitiveDetector.hh"
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Tubs.hh"
#include "G4SystemOfUnits.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"

//local classes
#include "ExitWinZEUS.h"

//ClassImp(ExitWinZEUS)

//_____________________________________________________________________________
ExitWinZEUS::ExitWinZEUS(const G4String& nam, G4double zpos, G4LogicalVolume *top): Detector(),
    G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "ExitWinZEUS: " << fNam << G4endl;

  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Al");

  G4double radius = 5.*cm;
  G4double dz = 1.*cm;

  G4Tubs *shape = new G4Tubs(fNam, 0., radius, dz, 0., 360.*deg);
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 1, 0, 0.5);
  vis->SetForceSolid(true);
  vol->SetVisAttributes(vis);

  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos-dz/2.), vol, fNam, top, false, 0);

  ClearEvent();

}//ExitWinZEUS

//_____________________________________________________________________________
G4bool ExitWinZEUS::ProcessHits(G4Step *step, G4TouchableHistory*) {

  G4Track *track = step->GetTrack();

  //select primary track
  if( track->GetParentID() != 0 ) return true;

  //first point on the exit window
  if(fZ > 9998.) {

    const G4ThreeVector point = step->GetPreStepPoint()->GetPosition();

    fX = point.x();
    fY = point.y();
    fZ = point.z();

    //G4cout << "primary " << fX << " " << fY << " " << fZ << G4endl;
  }

  return true;

}//ProcessHits

//_____________________________________________________________________________
void ExitWinZEUS::CreateOutput(TTree *tree) {

  //add this detector to the tree

  fAddr = this;
  tree->Branch(fNam, &fAddr);

}//CreateOutput

//_____________________________________________________________________________
void ExitWinZEUS::ClearEvent() {

  //default values for the position

  fX = 9999.;
  fY = 9999.;
  fZ = 9999.;

}//ClearEvent

























