
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

  //detector shape
  G4double xysiz = 200*mm;
  G4double zsiz = 350*mm;
  G4Box *shape = new G4Box(fNam, xysiz/2., xysiz/2., zsiz/2.);

  //PbWO4 material
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_PbWO4");

  //logical volume
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 0, 1); // blue
  vol->SetVisAttributes(vis);

  //rotation in x-z plane by rotation along y
  G4double rot_y = 0;
  geo->GetOptD(fNam, "rot_y", rot_y);
  G4RotationMatrix rot(G4ThreeVector(0, 1, 0), rot_y*rad); //is typedef to CLHEP::HepRotation

  //placement with rotation at a given position in x, y and z
  G4double xpos = 0; // center position in x, mm
  geo->GetOptD(fNam, "xpos", xpos);

  G4double ypos = 0; // position in y, mm
  geo->GetOptD(fNam, "ypos", ypos);

  //use y position as the edge closer to the beam axis
  G4double ymid = 0;
  if(ypos > 0.1) {
    ymid = xysiz/2. + ypos;
  } else if(ypos < -0.1) {
    ymid = -1*xysiz/2. + ypos;
  }

  G4double zpos = geo->GetD(fNam, "zpos") * mm; // position of the front face along z
  G4ThreeVector pos(xpos*mm, ymid*mm, zpos-zsiz/2);
  G4Transform3D transform(rot, pos); // is HepGeom::Transform3D

  //put to the top volume
  new G4PVPlacement(transform, vol, fNam, top, false, 0);

  //load flag for primary particles in ProcessHits if defined
  fSelectPrim = false;
  geo->GetOptB(fNam, "select_prim", fSelectPrim);
  //G4cout << "  BoxCalV2, select_prim: " << fSelectPrim << G4endl;

  //clear all event variables
  ClearEvent();

}//BoxCalV2

//_____________________________________________________________________________
G4bool BoxCalV2::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //remove the track
  G4Track *track = step->GetTrack();
  track->SetTrackStatus(fKillTrackAndSecondaries);

  fEnAll += track->GetTotalEnergy();

  //primary track only
  if( fSelectPrim == true || track->GetParentID() != 0 ) return true;

  //consider only first hit by the primary track
  if(fIsHit == kFALSE) {

    fIsHit = kTRUE;
  } else {
    return true;
  }

  //energy
  fEnPrim = track->GetTotalEnergy();

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

  u.AddBranch("_EnPrim", &fEnPrim, "D");
  u.AddBranch("_en", &fEnAll, "D");

  u.AddBranch("_hx", &fHx, "D");
  u.AddBranch("_hy", &fHy, "D");
  u.AddBranch("_hz", &fHz, "D");

}//CreateOutput

//_____________________________________________________________________________
void BoxCalV2::ClearEvent() {

  fIsHit = kFALSE;

  fEnPrim = -9999.;
  fEnAll = 0;

  fHx = 9999.;
  fHy = 9999.;
  fHz = 9999.;

}//ClearEvent














