
//_____________________________________________________________________________
//
// beam pipe element for particle counts on its inner wall
//_____________________________________________________________________________

//C++
#include <vector>

//ROOT
#include "TTree.h"

//Geant
#include "G4Cons.hh"
#include "G4LogicalVolume.hh"
#include "G4SystemOfUnits.hh"
#include "G4NistManager.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"

//local classes
#include "GeoParser.h"
#include "DetUtils.h"
#include "BeamPipeV1.h"

using namespace std;

//_____________________________________________________________________________
BeamPipeV1::BeamPipeV1(G4String nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  BeamPipeV1: " << fNam << G4endl;

  //length, meters
  G4double length = geo->GetD(fNam, "length") * m;

  //inner radius, mm
  G4double r1 = geo->GetD(fNam, "r1") * mm;

  //radial thickness
  G4double dr = geo->GetD(fNam, "dr") * mm;

  //shape
  G4Cons *shape = new G4Cons(fNam, r1, r1+dr, r1, r1+dr, length/2, 0, 360*deg);

  //logical volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Al");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(1, 0, 0); // red
  vis->SetLineWidth(2);
  vis->SetForceSolid(true);
  vol->SetVisAttributes(vis);

  //vessel in top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0), vol, fNam, top, false, 0);

}//BeamPipeV1

//_____________________________________________________________________________
G4bool BeamPipeV1::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //remove track incident on vessel
  G4Track *track = step->GetTrack();
  track->SetTrackStatus(fKillTrackAndSecondaries);

  //energy in current step
  G4double en_step = track->GetTotalEnergy();

  //add possible secondaries to the energy
  const vector<const G4Track*> *sec = step->GetSecondaryInCurrentStep();
  vector<const G4Track*>::const_iterator isec = sec->begin();
  while(isec != sec->end()) {
    en_step += (*isec)->GetTotalEnergy();
    isec++;
  }

  //hit position
  const G4ThreeVector hp = step->GetPostStepPoint()->GetPosition();

  //add the hit
  fHitPdg.push_back( track->GetDynamicParticle()->GetPDGcode() );
  fHitEn.push_back( en_step/GeV );
  fHitX.push_back( hp.x() );
  fHitY.push_back( hp.y() );
  fHitZ.push_back( hp.z() );

  return true;

}//ProcessHits

//_____________________________________________________________________________
void BeamPipeV1::CreateOutput(TTree *tree) {

  DetUtils u(fNam, tree);

  u.AddBranch("_HitPdg", &fHitPdg);
  u.AddBranch("_HitEn", &fHitEn);
  u.AddBranch("_HitX", &fHitX);
  u.AddBranch("_HitY", &fHitY);
  u.AddBranch("_HitZ", &fHitZ);

}//CreateOutput

//_____________________________________________________________________________
void BeamPipeV1::ClearEvent() {

  fHitPdg.clear();
  fHitEn.clear();
  fHitX.clear();
  fHitY.clear();
  fHitZ.clear();

}//ClearEvent























