
//_____________________________________________________________________________
//
// Simple calorimeter version 2 (V2) for tests,
// absorbs every particle in a single step with no secondaries.
//
// Historical note: such calorimeter was originally invented by Jara Cimrman.
//_____________________________________________________________________________

//C++

//ROOT
#include "TTree.h"

//Geant
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4VPhysicalVolume.hh"
#include "G4VisAttributes.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"
#include "G4ThreeVector.hh"

//local classes
#include "BoxCalV2.h"
#include "DetUtils.h"
#include "GeoParser.h"

//_____________________________________________________________________________
BoxCalV2::BoxCalV2(const G4String& nam, GeoParser *geo, G4LogicalVolume *top): Detector(),
  G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  BoxCalV2: " << fNam << G4endl;

  //position along z and x
  G4double zpos = geo->GetD(fNam, "zpos") * mm;
  G4double xpos = geo->GetD(fNam, "xpos") * mm;

  //G4cout << "  BoxCalV2: " << zpos << " " << xpos << G4endl;

  //detector shape
  G4double xysiz = 20*cm;
  G4double zsiz = 35*cm;
  G4Box *shape = new G4Box(fNam, xysiz/2., xysiz/2., zsiz/2.);

  //PbWO4 material
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_PbWO4");
  //G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");

  //logical volume
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 0, 1); // blue
  vol->SetVisAttributes(vis);

  //rotation in x-z plane by rotation along y
  G4RotationMatrix rot(G4ThreeVector(0, 1, 0), -0.02*rad); //typedef to CLHEP::HepRotation

  //placement with rotation at a given position in x and z
  G4ThreeVector pos(xpos, 0, zpos-zsiz/2);
  G4Transform3D transform(rot, pos); // is HepGeom::Transform3D

  //put to the top volume
  new G4PVPlacement(transform, vol, fNam, top, false, 0);

  //clear all event variables
  ClearEvent();

}//BoxCalV2

//_____________________________________________________________________________
G4bool BoxCalV2::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //remove the track
  G4Track *track = step->GetTrack();
  //track->SetTrackStatus(G4TrackStatus::fKillTrackAndSecondaries);
  track->SetTrackStatus(fKillTrackAndSecondaries);

  //primary track only
  if( track->GetParentID() != 0 ) return true;

  //consider only first hit by the primary track
  if(fIsHit == kFALSE) {

    fIsHit = kTRUE;
  } else {
    return true;
  }

  //energy
  fEn = track->GetTotalEnergy();

  //hit position
  const G4ThreeVector hp = step->GetPostStepPoint()->GetPosition();
  fHx = hp.x();
  fHy = hp.y();
  fHz = hp.z();

  //G4cout << "BoxCalV2::ProcessHits: " << track->GetParentID() << G4endl;

  return true;

}//ProcessHits

//_____________________________________________________________________________
void BoxCalV2::CreateOutput(TTree *tree) {

  //output from BoxCalV2

  DetUtils u(fNam, tree);

  u.AddBranch("_IsHit", &fIsHit, "O");

  u.AddBranch("_en", &fEn, "D");

  u.AddBranch("_hx", &fHx, "D");
  u.AddBranch("_hy", &fHy, "D");
  u.AddBranch("_hz", &fHz, "D");

}//CreateOutput

//_____________________________________________________________________________
void BoxCalV2::ClearEvent() {

  fIsHit = kFALSE;

  fEn = -9999.;

  fHx = 9999.;
  fHy = 9999.;
  fHz = 9999.;

}//ClearEvent














