
//_____________________________________________________________________________
//
// Exit window version 1, output on photon impact point and on conversion to pair,
// flat (perpendicular) geometry or tilted geometry
//_____________________________________________________________________________

//C++
#include <math.h>
#include <vector>

//ROOT
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
#include "GeoParser.h"

using namespace std;

//_____________________________________________________________________________
ExitWindowV1::ExitWindowV1(const G4String& nam, GeoParser *geo, G4LogicalVolume *top): Detector(),
    G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "ExitWindowV1: " << fNam << G4endl;

  //transverse and longitudinal size
  G4double dxy = geo->GetD(nam, "dxy")*mm;
  G4double dz = geo->GetD(nam, "dz")*mm;

  //center position along z
  G4double zpos = geo->GetD(nam, "zpos")*m;

  //tilt angle along y, given from z axis towards x axis
  G4double tilt = geo->GetD(nam, "tilt")*mrad;
  tilt -= CLHEP::pi/2;

  //box shape, Al material
  G4Box *shape = new G4Box(nam+"_shape", dxy/2, dxy/2, dz/2);
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Al");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, nam);

  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 1, 0, 0.5);
  vis->SetForceSolid(true);
  vol->SetVisAttributes(vis);

  //put the exit window to the top
  G4RotationMatrix rot(G4ThreeVector(0, 1, 0), tilt); //is typedef to CLHEP::HepRotation
  G4ThreeVector pos(0, 0, zpos);
  G4Transform3D transform(rot, pos); // is HepGeom::Transform3D
  new G4PVPlacement(transform, vol, vol->GetName(), top, false, 0);

  ClearEvent();

}//ExitWindowV1

//_____________________________________________________________________________
G4bool ExitWindowV1::ProcessHits(G4Step *step, G4TouchableHistory*) {

  G4Track *track = step->GetTrack();

  //add the hit
  fHitPdg.push_back( track->GetDynamicParticle()->GetPDGcode() );
  fHitEn.push_back( track->GetTotalEnergy()/GeV );

  //hit position
  const G4ThreeVector hp = step->GetPreStepPoint()->GetPosition();
  fHitX.push_back( hp.x()/mm );
  fHitY.push_back( hp.y()/mm );
  fHitZ.push_back( hp.z()/mm );

  //deposited energy in hit
  fHitEdep.push_back( step->GetTotalEnergyDeposit()/GeV );

  //flag for primary particle in hit
  Int_t prim = 0;
  if( track->GetParentID() == 0 ) {prim = 1;}
  fHitPrim.push_back( prim );

  //conversion to e+e- pair and number of secondaries
  Int_t nsec = 0; // number of secondaries
  G4int sign = 1; // sing of the pair
  G4bool electron = true;
  const vector<const G4Track*> *sec = step->GetSecondaryInCurrentStep();
  vector<const G4Track*>::const_iterator i;
  //secondary loop
  for(i = sec->begin(); i != sec->end(); i++) {
    const G4Track *t = *i;
    const G4ParticleDefinition *def = t->GetParticleDefinition();

    G4int pdg = def->GetPDGEncoding();
    sign *= pdg;
    electron = (abs(pdg) == 11) and electron;

    nsec++;
  }//secondary loop

  //number of secondaries in hit
  fHitNsec.push_back( nsec );

  //evaluate the conversion in the hit
  Int_t conv = 0;
  if(nsec == 2 and sign < 0 and electron) {conv = 1;}
  fHitConv.push_back( conv );

  return true;

}//ProcessHits

//_____________________________________________________________________________
void ExitWindowV1::CreateOutput(TTree *tree) {

  DetUtils u(fNam, tree); // prefix for variable names and tree for AddBranch

  u.AddBranch("_HitPdg", &fHitPdg);
  u.AddBranch("_HitEn", &fHitEn);
  u.AddBranch("_HitX", &fHitX);
  u.AddBranch("_HitY", &fHitY);
  u.AddBranch("_HitZ", &fHitZ);
  u.AddBranch("_HitPrim", &fHitPrim);
  u.AddBranch("_HitConv", &fHitConv);
  u.AddBranch("_HitEdep", &fHitEdep);
  u.AddBranch("_HitNsec", &fHitNsec);

}//CreateOutput

//_____________________________________________________________________________
void ExitWindowV1::ClearEvent() {

  fHitPdg.clear();
  fHitEn.clear();
  fHitX.clear();
  fHitY.clear();
  fHitZ.clear();
  fHitPrim.clear();
  fHitConv.clear();
  fHitEdep.clear();
  fHitNsec.clear();

}//ClearEvent























