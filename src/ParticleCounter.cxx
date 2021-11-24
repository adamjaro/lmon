
//_____________________________________________________________________________
//
// Counter plane for incoming particles
//
//_____________________________________________________________________________

//C++
#include <vector>

//ROOT
#include "TTree.h"

//Geant
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4PVPlacement.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"
#include "G4ThreeVector.hh"

//local classes
#include "ParticleCounter.h"
#include "GeoParser.h"
#include "DetUtils.h"

using namespace std;

//_____________________________________________________________________________
ParticleCounter::ParticleCounter(const G4String& nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  ParticleCounter: " << fNam << G4endl;

  //full size in x, y and z, mm for rectangular counter
  G4double dx = 0, dy = 0;
  geo->GetOptD(fNam, "dx", dx, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "dy", dy, GeoParser::Unit(mm));
  G4double dz = geo->GetD(fNam, "dz")*mm;

  //inner and outer radius, mm, in case of cylindrical counter
  G4double inner_r = 0, outer_r = 0;
  geo->GetOptD(fNam, "inner_r", inner_r, GeoParser::Unit(mm));
  G4bool is_tubs = geo->GetOptD(fNam, "outer_r", outer_r, GeoParser::Unit(mm));

  //cylindrical or rectangular shape for the counter
  G4CSGSolid *shape = 0x0;
  if(is_tubs) {
    shape = new G4Tubs(fNam, inner_r, outer_r, dz/2, 0., 360.*deg);
  } else {
    shape = new G4Box(fNam, dx/2, dy/2, dz/2);
  }

  //logical volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(1, 0, 0, 0.3);
  vis->SetForceSolid(true);
  vol->SetVisAttributes(vis);

  //center position, mm
  G4double xpos=0*mm, ypos=0*mm, zpos=0*mm;
  geo->GetOptD(fNam, "xpos", xpos, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "ypos", ypos, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "zpos", zpos, GeoParser::Unit(mm));

  //mother volume for the detector
  G4LogicalVolume *mvol = top;
  G4String mother_nam;
  if( geo->GetOptS(fNam, "place_into", mother_nam) ) {
    mvol = GetMotherVolume(mother_nam, top);
  }

  //placement in mother volume
  G4RotationMatrix rot(G4ThreeVector(0, 1, 0), 0); //CLHEP::HepRotation
  G4ThreeVector pos(xpos, ypos, zpos);
  G4Transform3D transform(rot, pos); //HepGeom::Transform3D

  new G4PVPlacement(transform, vol, fNam, mvol, false, 0);

}//ParticleCounter

//_____________________________________________________________________________
G4LogicalVolume* ParticleCounter::GetMotherVolume(G4String mother_nam, G4LogicalVolume *top) {

  for(size_t i=0; i<top->GetNoDaughters(); i++) {

    G4LogicalVolume *dv = top->GetDaughter(i)->GetLogicalVolume();

    if( dv->GetName() == mother_nam ) {
      return dv;
    }
  }

  return 0x0;

}//GetMotherVolume

//_____________________________________________________________________________
G4bool ParticleCounter::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //remove the track
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
  const G4ThreeVector hp = step->GetPreStepPoint()->GetPosition();

  //add the hit
  fHitPdg.push_back( track->GetDynamicParticle()->GetPDGcode() );
  fHitEn.push_back( en_step/GeV );
  fHitX.push_back( hp.x()/mm );
  fHitY.push_back( hp.y()/mm );
  fHitZ.push_back( hp.z()/mm );

  //G4cout << track->GetTrackID() << " " << track->GetDynamicParticle()->GetPDGcode() << " " << track->GetTotalEnergy()/GeV;
  //G4cout << " " << hp.x() << " " << hp.y() << " " << hp.z() << G4endl;

  return true;

}//ProcessHits

//_____________________________________________________________________________
void ParticleCounter::CreateOutput(TTree *tree) {

  //output from ParticleCounter

  DetUtils u(fNam, tree);

  u.AddBranch("_HitPdg", &fHitPdg);
  u.AddBranch("_HitEn", &fHitEn);
  u.AddBranch("_HitX", &fHitX);
  u.AddBranch("_HitY", &fHitY);
  u.AddBranch("_HitZ", &fHitZ);

}//CreateOutput

//_____________________________________________________________________________
void ParticleCounter::ClearEvent() {

  fHitPdg.clear();
  fHitEn.clear();
  fHitX.clear();
  fHitY.clear();
  fHitZ.clear();

}//ClearEvent


































