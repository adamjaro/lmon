
//_____________________________________________________________________________
//
// testing calorimeter with radial symmetry
//
//_____________________________________________________________________________

//Geant
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"
#include "G4Tubs.hh"

//local classes
#include "BoxCalR.h"
#include "GeoParser.h"

//_____________________________________________________________________________
BoxCalR::BoxCalR(G4String nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  BoxCalR: " << fNam << G4endl;

  //position along z
  G4double zpos = geo->GetD(fNam, "zpos") * mm;

  //calorimeter shape
  G4double length = 200*mm;
  G4double r1 = 80*mm;
  G4double r2 = 2870*mm;

  G4Tubs *shape = new G4Tubs(fNam, r1, r2, length/2, 0., 360.*deg);

  //logical volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_W");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 0, 1); // blue
  vis->SetLineWidth(2);
  //vis->SetForceSolid(true);
  //vis->SetForceAuxEdgeVisible(true);
  vol->SetVisAttributes(vis);

  //put the calorimeter to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos-length/2), vol, fNam, top, false, 0);

}//BoxCalR

//_____________________________________________________________________________
G4bool BoxCalR::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //G4cout << "BoxCalR::ProcessHits" << G4endl;

  //remove the track
  G4Track *track = step->GetTrack();
  track->SetTrackStatus(fKillTrackAndSecondaries);

  //primary track only
  //if( track->GetParentID() != 0 ) return true;

  //G4cout << track->GetTotalEnergy()/GeV << " " << track->GetDynamicParticle()->GetTotalEnergy()/GeV << " ";
  //G4cout << track->GetTotalEnergy() - track->GetDynamicParticle()->GetTotalEnergy() << G4endl;

  //G4cout << track->GetDynamicParticle()->GetPrimaryParticle() << G4endl;

  //hit position
  //const G4ThreeVector hp = step->GetPostStepPoint()->GetPosition();
  //G4cout << hp.x() << " " << hp.y() << " " << hp.z() <<G4endl;

  return true;

}//ProcessHits



















