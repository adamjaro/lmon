
//_____________________________________________________________________________
//
// testing calorimeter with radial symmetry, no secondaries
//
//_____________________________________________________________________________

//C++
#include <vector>

//ROOT
#include "TTree.h"

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
#include "DetUtils.h"

using namespace std;

//_____________________________________________________________________________
BoxCalR::BoxCalR(G4String nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  BoxCalR: " << fNam << G4endl;

  //position along z
  G4double zpos = geo->GetD(fNam, "zpos") * mm;

  //calorimeter shape
  G4double length = 200*mm;
  G4double r1 = geo->GetD(fNam, "r1") * mm;
  G4double r2 = 2870*mm;

  G4Tubs *shape = new G4Tubs(fNam, r1, r2, length/2, 0., 360.*deg);
  //G4Tubs *shape = new G4Tubs(fNam, r1, r2, length/2, 90*deg, 270.*deg);

  //logical volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_W");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  //vis->SetColor(0, 0, 1); // blue
  vis->SetColor(1, 0, 0); // red
  vis->SetLineWidth(2);
  //vis->SetForceSolid(true);
  vol->SetVisAttributes(vis);

  //put the calorimeter to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos-length/2), vol, fNam, top, false, 0);

  //clear all event variables
  ClearEvent();

}//BoxCalR

//_____________________________________________________________________________
G4bool BoxCalR::ProcessHits(G4Step *step, G4TouchableHistory*) {

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
void BoxCalR::CreateOutput(TTree *tree) {

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
void BoxCalR::ClearEvent() {

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

















