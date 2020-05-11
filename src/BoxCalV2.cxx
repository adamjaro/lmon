
//_____________________________________________________________________________
//
// Simple calorimeter version 2 (V2) for tests,
// absorbs every particle in a single step with no secondaries.
//
// Historical note: such calorimeter was originally invented by Jara Cimrman.
//_____________________________________________________________________________

//C++
#include <vector>

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

using namespace std;

//_____________________________________________________________________________
BoxCalV2::BoxCalV2(const G4String& nam, GeoParser *geo, G4LogicalVolume *top): Detector(),
  G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  BoxCalV2: " << fNam << G4endl;

  //detector shape, mm
  G4double xsiz = 200;
  G4double ysiz = 200;
  G4double zsiz = 350;
  geo->GetOptD(fNam, "xsiz", xsiz);
  geo->GetOptD(fNam, "ysiz", ysiz);
  geo->GetOptD(fNam, "zsiz", zsiz);
  G4Box *shape = new G4Box(fNam, (xsiz*mm)/2., (ysiz*mm)/2., (zsiz*mm)/2.);

  //PbWO4 material
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_W");

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
    ymid = ysiz/2. + ypos;
  } else if(ypos < -0.1) {
    ymid = -1*ysiz/2. + ypos;
  }

  G4double zpos = geo->GetD(fNam, "zpos") * mm; // position of the front face along z
  G4ThreeVector pos(xpos*mm, ymid*mm, zpos-zsiz/2);
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
  track->SetTrackStatus(fKillTrackAndSecondaries);

  //mark the hit
  fIsHit = kTRUE;

  //energy in current step
  G4double en_step = track->GetTotalEnergy();

  //add possible secondaries to the energy
  const vector<const G4Track*> *sec = step->GetSecondaryInCurrentStep();
  vector<const G4Track*>::const_iterator isec = sec->begin();
  while(isec != sec->end()) {
    en_step += (*isec)->GetTotalEnergy();
    isec++;
  }

  //add energy in step to the total energy in event
  fEnAll += en_step/GeV;

  //hit position
  const G4ThreeVector hp = step->GetPostStepPoint()->GetPosition();

  //add the hit
  fHitPdg.push_back( track->GetDynamicParticle()->GetPDGcode() );
  fHitEn.push_back( en_step/GeV );
  fHitX.push_back( hp.x() );
  fHitY.push_back( hp.y() );
  fHitZ.push_back( hp.z() );

  //first hit by primary particle
  if(!fPrimHit && track->GetParentID() == 0) {
    fPrimHit = true;
    fHx = hp.x();
    fHy = hp.y();
    fHz = hp.z();
  }

  return true;

}//ProcessHits

//_____________________________________________________________________________
void BoxCalV2::CreateOutput(TTree *tree) {

  //output from BoxCalV2

  DetUtils u(fNam, tree);

  u.AddBranch("_IsHit", &fIsHit, "O");

  u.AddBranch("_en", &fEnAll, "D");

  u.AddBranch("_hx", &fHx, "D");
  u.AddBranch("_hy", &fHy, "D");
  u.AddBranch("_hz", &fHz, "D");

  u.AddBranch("_HitPdg", &fHitPdg);
  u.AddBranch("_HitEn", &fHitEn);
  u.AddBranch("_HitX", &fHitX);
  u.AddBranch("_HitY", &fHitY);
  u.AddBranch("_HitZ", &fHitZ);

}//CreateOutput

//_____________________________________________________________________________
void BoxCalV2::ClearEvent() {

  fIsHit = kFALSE;

  fEnAll = 0;

  fHx = 99999.;
  fHy = 99999.;
  fHz = 99999.;

  fHitPdg.clear();
  fHitEn.clear();
  fHitX.clear();
  fHitY.clear();
  fHitZ.clear();

  fPrimHit = false;

}//ClearEvent














