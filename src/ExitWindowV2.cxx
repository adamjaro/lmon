
//_____________________________________________________________________________
//
// Exit window version 2, radial geometry
//
//_____________________________________________________________________________

//ROOT
#include "TMath.h"
#include "TTree.h"

//Geant
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Tubs.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4PVPlacement.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"
#include "G4ThreeVector.hh"

//local classes
#include "ExitWindowV2.h"
#include "DetUtils.h"

using namespace std;

//_____________________________________________________________________________
ExitWindowV2::ExitWindowV2(const G4String& nam, G4double zpos, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  ExitWindowV2: " << fNam << G4endl;

  G4double dz = 2.5*meter; // length along z
  G4double radius = 10*cm; // inner radius
  G4double thickness = 1*mm; // exit window thickness

  //cylindrical U-shape
  G4Tubs *shape = new G4Tubs(fNam, radius, radius+thickness, dz/2., 90*deg, 180*deg);

  //exit window material
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Al");

  //logical volume
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visualization
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 1, 0, 0.5);
  vis->SetForceSolid(true);
  vol->SetVisAttributes(vis);

  //100 mrad in x-z plane by rotation along y
  G4RotationMatrix rot(G4ThreeVector(0, 1, 0), -0.1*rad); //typedef to CLHEP::HepRotation

  //placement with rotation at a given position along z
  G4ThreeVector pos(0, 0, zpos);
  G4Transform3D transform(rot, pos); // is HepGeom::Transform3D

  new G4PVPlacement(transform, vol, fNam, top, false, 0);

}//ExitWindowV2

//_____________________________________________________________________________
G4bool ExitWindowV2::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //track in current step
  G4Track *track = step->GetTrack();

  //primary only
  if( track->GetParentID() != 0 ) return true;

  //first point on the exit window
  if( fPhotZ > 9998.) {

    const G4ThreeVector point = step->GetPostStepPoint()->GetPosition();

    fPhotX = point.x();
    fPhotY = point.y();
    fPhotZ = point.z();
  }

  //conversion to a pair
  G4int nsec = 0, nel = 0, npos = 0; // number of secondaries, electrons and positrons
  Double_t en_el=-9999., en_pos=-9999.;

  //secondary loop
  const vector<const G4Track*> *sec = step->GetSecondaryInCurrentStep();
  vector<const G4Track*>::const_iterator i;
  for(i = sec->begin(); i != sec->end(); i++) {

    //all secondaries
    nsec++;

    //get the pdg
    const G4ParticleDefinition *def = (*i)->GetParticleDefinition();
    G4int pdg = def->GetPDGEncoding();

    //electrons and positrons
    if(pdg == 11) {
      nel++;
      en_el = (*i)->GetTotalEnergy();
    }
    if(pdg == -11) {
      npos++;
      en_pos = (*i)->GetTotalEnergy();
    }

  }//secondary loop

  //select e+e- conversion
  if(nsec != 2 || nel != 1 || npos != 1) return true;

  fConv = kTRUE;

  //energy of electron and positron
  fEnEl = en_el;
  fEnPos = en_pos;

  //location of the conversion
  const G4ThreeVector cp = step->GetPostStepPoint()->GetPosition();
  fConvX = cp.x();
  fConvY = cp.y();
  fConvZ = cp.z();

  //step lenght with the conversion
  fConvStepLen = step->GetStepLength();

  return true;

}//ProcessHits

//_____________________________________________________________________________
void ExitWindowV2::CreateOutput(TTree *tree) {

  //set output branches of exit window

  DetUtils u(fNam, tree); // prefix for variable names and tree for AddBranch

  u.AddBranch("_IsHit", &fIsHit, "O");

  u.AddBranch("_photX", &fPhotX, "D");
  u.AddBranch("_photY", &fPhotY, "D");
  u.AddBranch("_photZ", &fPhotZ, "D");

  u.AddBranch("_conv", &fConv, "O");

  u.AddBranch("_enEl", &fEnEl, "D");
  u.AddBranch("_enPos", &fEnPos, "D");

  u.AddBranch("_convX", &fConvX, "D");
  u.AddBranch("_convY", &fConvY, "D");
  u.AddBranch("_convZ", &fConvZ, "D");

  u.AddBranch("_steplen", &fConvStepLen, "D");
  u.AddBranch("_convlen", &fPhotConvLen, "D");

}//CreateOutput

//_____________________________________________________________________________
void ExitWindowV2::ClearEvent() {

  //default values

  fIsHit = kFALSE;

  fPhotX = 9999.;
  fPhotY = 9999.;
  fPhotZ = 9999.;

  fConv = kFALSE;

  fEnEl = -9999.;
  fEnPos = -9999.;

  fConvStepLen = -9999.;
  fPhotConvLen = -9999.;

  fConvX = 9999.;
  fConvY = 9999.;
  fConvZ = 9999.;

}//ClearEvent

//_____________________________________________________________________________
void ExitWindowV2::FinishEvent() {

  // length between photon first point and conversion point
  fPhotConvLen = (fConvX-fPhotX)*(fConvX-fPhotX) + (fConvY-fPhotY)*(fConvY-fPhotY) + (fConvZ-fPhotZ)*(fConvZ-fPhotZ);
  fPhotConvLen = TMath::Sqrt(fPhotConvLen);

}//FinishEvent














