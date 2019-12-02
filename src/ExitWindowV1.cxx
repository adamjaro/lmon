
//_____________________________________________________________________________
//
// Exit window version 1, output on photon impact point and on conversion to pair,
// flat (perpendicular) geometry or tilted geometry
//_____________________________________________________________________________

//C++
#include <string>

//ROOT
#include "TMath.h"
#include "TTree.h"

//Geant
#include "G4VSensitiveDetector.hh"
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Tubs.hh"
#include "G4Box.hh"
#include "G4SystemOfUnits.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"

//local classes
#include "ExitWindowV1.h"
#include "DetUtils.h"

using namespace std;

//_____________________________________________________________________________
ExitWindowV1::ExitWindowV1(const G4String& nam, G4double zpos, geom geo, G4LogicalVolume *top): Detector(),
    G4VSensitiveDetector(nam), fNam(nam), fZpos(zpos), fTop(top) {

  G4cout << "ExitWindowV1: " << fNam << G4endl;

  //material for the exit window
  fMat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Al");

  //select the geometry
  if(geo == kFlat) {
    ConstructFlat();
  }
  if(geo == kTilt) {
    ConstructTilt();
  }

  ClearEvent();

}//ExitWindowV1

//_____________________________________________________________________________
void ExitWindowV1::ConstructFlat() {

  // flat geometry, perpendicular to electron beam axis

  G4cout << "ExitWindowV1::ConstructFlat" << G4endl;

  G4double radius = 5.*cm;
  G4double dz = 1*cm;

  G4Tubs *shape = new G4Tubs(fNam, 0., radius, dz/2., 0., 360.*deg);
  G4LogicalVolume *vol = new G4LogicalVolume(shape, fMat, fNam);

  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 1, 0, 0.5);
  vis->SetForceSolid(true);
  vol->SetVisAttributes(vis);

  new G4PVPlacement(0, G4ThreeVector(0, 0, fZpos-dz/2.), vol, fNam, fTop, false, 0);

}//ConstructFlat

//_____________________________________________________________________________
void ExitWindowV1::ConstructTilt() {

  // tilted geometry, angle to electron beam axis

  G4cout << "ExitWindowV1::ConstructTilt" << G4endl;

  G4double dx = 10.*cm;
  G4double dz = 1.*cm;

  G4Box *shape = new G4Box(fNam, dx/2., dx/2., dz/2.);
  G4LogicalVolume *vol = new G4LogicalVolume(shape, fMat, fNam);

  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 1, 0, 0.5);
  vis->SetForceSolid(true);
  vol->SetVisAttributes(vis);

  G4RotationMatrix rot(0, 45*deg, 0); //phi, theta, psi, is typedef to CLHEP::HepRotation
  //G4RotationMatrix rot(0, 0, 0);
  G4ThreeVector pos(0, 0, fZpos);
  G4Transform3D transform(rot, pos); // is HepGeom::Transform3D

  new G4PVPlacement(transform, vol, fNam, fTop, false, 0);

}//ConstructTilt

//_____________________________________________________________________________
G4bool ExitWindowV1::ProcessHits(G4Step *step, G4TouchableHistory*) {

  G4Track *track = step->GetTrack();

  //select primary track
  if( track->GetParentID() != 0 ) return true;

  //first point on the exit window
  if( fPhotZ > 9998.) {

    //const G4ThreeVector point = step->GetPreStepPoint()->GetPosition();
    const G4ThreeVector point = step->GetPostStepPoint()->GetPosition();

    fPhotX = point.x();
    fPhotY = point.y();
    fPhotZ = point.z();
  }

  //conversion to a pair
  G4int nsec = 0; // number of secondaries
  G4int apdg[2] = {0, 0}; // absolute value of pdg
  G4int sign = 1; // sing of the pair
  const vector<const G4Track*> *sec = step->GetSecondaryInCurrentStep();
  vector<const G4Track*>::const_iterator i;
  //secondary loop
  for(i = sec->begin(); i != sec->end(); i++) {
    const G4Track *t = *i;
    const G4ParticleDefinition *def = t->GetParticleDefinition();

    //get the pdg
    G4int pdg = def->GetPDGEncoding();
    sign *= pdg;

    //abs of the pdg
    if(nsec < 2) {
      apdg[nsec] = TMath::Abs( pdg );
    }
    nsec++;
  }//secondary loop

  //sign +/- 1
  if(sign < 0) {
    sign = -1;
  } else {
    sign = 1;
  }

  //select pair conversion
  if(nsec != 2 || sign > 0) return true;

  //test for e+e- conversion
  if(apdg[0] == 11 && apdg[1] == 11) {

    fConv = kTRUE;
  }

  //test for mu+mu- conversion
  if(apdg[0] == 13 && apdg[1] == 13) {

    fMuConv = kTRUE;
  }

  //location of the conversion
  const G4ThreeVector cp = step->GetPostStepPoint()->GetPosition();
  fConvX = cp.x();
  fConvY = cp.y();
  fConvZ = cp.z();

  //step lenght with the conversion
  fConvStepLen = step->GetStepLength();

  //G4cout << "conv " << sign << G4endl;

  return true;

}//ProcessHits

//_____________________________________________________________________________
void ExitWindowV1::CreateOutput(TTree *tree) {

  //set output branches of exit window

  //DetUtils u(fNam, tree);
  DetUtils u("ew", tree);

  u.AddBranch("_photX", &fPhotX, "D");
  u.AddBranch("_photY", &fPhotY, "D");
  u.AddBranch("_photZ", &fPhotZ, "D");

  u.AddBranch("_conv", &fConv, "O");
  u.AddBranch("_muconv", &fMuConv, "O");

  u.AddBranch("_convX", &fConvX, "D");
  u.AddBranch("_convY", &fConvY, "D");
  u.AddBranch("_convZ", &fConvZ, "D");

  u.AddBranch("_steplen", &fConvStepLen, "D");
  u.AddBranch("_convlen", &fPhotConvLen, "D");

}//CreateOutput

//_____________________________________________________________________________
void ExitWindowV1::ClearEvent() {

  //G4cout << "ExitWindowV1::ClearEvent" << G4endl;

  //default values

  fPhotX = 9999.;
  fPhotY = 9999.;
  fPhotZ = 9999.;

  fConv = kFALSE;
  fMuConv = kFALSE;

  fConvStepLen = -9999.;
  fPhotConvLen = -9999.;

  fConvX = 9999.;
  fConvY = 9999.;
  fConvZ = 9999.;

}//ClearEvent

//_____________________________________________________________________________
void ExitWindowV1::FinishEvent() {

  // length between photon first point and conversion point
  fPhotConvLen = (fConvX-fPhotX)*(fConvX-fPhotX) + (fConvY-fPhotY)*(fConvY-fPhotY) + (fConvZ-fPhotZ)*(fConvZ-fPhotZ);
  fPhotConvLen = TMath::Sqrt(fPhotConvLen);
/*
  G4cout << fPhotX << " " << fPhotY << " " << fPhotZ;

  if(fConv) {

    G4cout << " " << fConvX << " " << fConvY << " " << fConvZ << " " << fConvStepLen << " " << fPhotConvLen;

  }

  G4cout << G4endl;
*/
}//FinishEvent





















