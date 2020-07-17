
//_____________________________________________________________________________
//
// Simple tracking layer which writes an array of hits
//
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
#include "TrackDet.h"
#include "DetUtils.h"
#include "GeoParser.h"

using namespace std;

//_____________________________________________________________________________
TrackDet::TrackDet(const G4String& nam, GeoParser *geo, G4LogicalVolume *top): Detector(),
  G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  TrackDet: " << fNam << G4endl;

  //detector shape, mm
  G4double xsiz = 200;
  G4double ysiz = 200;
  G4double zsiz = 0.3;
  geo->GetOptD(fNam, "xsiz", xsiz);
  geo->GetOptD(fNam, "ysiz", ysiz);
  geo->GetOptD(fNam, "zsiz", zsiz);
  G4Box *shape = new G4Box(fNam, (xsiz*mm)/2., (ysiz*mm)/2., (zsiz*mm)/2.);

  //silicon as a material
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Si");

  //logical volume
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  G4bool vis_full = true;
  geo->GetOptB(fNam, "vis_full", vis_full);
  if(vis_full) {
    //vis->SetColor(1, 0, 0, 0.6); // red
    vis->SetColor(1, 0, 0); // red
    //vis->SetLineWidth(2);
    //vis->SetForceSolid(true);
  } else {
    vis->SetColor(0, 0, 1); // blue
    vis->SetForceAuxEdgeVisible(true);
  }
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

  G4double zpos = geo->GetD(fNam, "zpos") * mm; // position of the front face along z

  //make the placement
  G4ThreeVector pos(xpos*mm, ypos*mm, zpos-zsiz/2);
  G4Transform3D transform(rot, pos); // is HepGeom::Transform3D

  //put to the top volume
  new G4PVPlacement(transform, vol, fNam, top, false, 0);

  //clear all event variables
  ClearEvent();

}//BoxCalV2

//_____________________________________________________________________________
G4bool TrackDet::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //mark the hit
  fIsHit = kTRUE;

  //get the track
  G4Track *track = step->GetTrack();

  //energy in current step in GeV
  G4double en_step = track->GetTotalEnergy()/GeV;

  //add energy in step to the total energy in event
  fEnAll += en_step;

  //hit position
  const G4ThreeVector hp = step->GetPostStepPoint()->GetPosition();

  //add the hit
  fHitPdg.push_back( track->GetDynamicParticle()->GetPDGcode() );
  fHitEn.push_back( en_step );
  fHitX.push_back( hp.x() );
  fHitY.push_back( hp.y() );
  fHitZ.push_back( hp.z() );

  return true;

}//ProcessHits

//_____________________________________________________________________________
void TrackDet::CreateOutput(TTree *tree) {

  //output from TrackDet

  DetUtils u(fNam, tree);

  u.AddBranch("_IsHit", &fIsHit, "O");

  u.AddBranch("_en", &fEnAll, "D");

  u.AddBranch("_HitPdg", &fHitPdg);
  u.AddBranch("_HitEn", &fHitEn);
  u.AddBranch("_HitX", &fHitX);
  u.AddBranch("_HitY", &fHitY);
  u.AddBranch("_HitZ", &fHitZ);

}//CreateOutput

//_____________________________________________________________________________
void TrackDet::ClearEvent() {

  fIsHit = kFALSE;

  fEnAll = 0;

  fHitPdg.clear();
  fHitEn.clear();
  fHitX.clear();
  fHitY.clear();
  fHitZ.clear();

}//ClearEvent














