
//_____________________________________________________________________________
//
// Basic tracking layer which writes an array of hits
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <string>
#include <sstream>

//Boost
#include <boost/tokenizer.hpp>

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
#include "PolTrackLay.h"
#include "DetUtils.h"
#include "GeoParser.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
PolTrackLay::PolTrackLay(const G4String& nam, GeoParser *geo, G4LogicalVolume *top): Detector(),
  G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "PolTrackLay: " << fNam << G4endl;

  //full size in x, y and z, mm
  G4double dx = geo->GetD(fNam, "dx")*mm;
  G4double dy = geo->GetD(fNam, "dy")*mm;
  G4double dz = geo->GetD(fNam, "dz")*mm;
  G4Box *shape = new G4Box(fNam, dx/2, dy/2, dz/2);

  //silicon as a material
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Si");

  //logical volume
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  vol->SetVisAttributes(ColorDecoder(geo));

  //center position, mm
  G4double xpos=0*mm, ypos=0*mm, zpos=0*mm;
  geo->GetOptD(fNam, "xpos", xpos, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "ypos", ypos, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "zpos", zpos, GeoParser::Unit(mm));

  //rotation along a given axis
  G4double rot_x=0, rot_y=1, rot_z=0, rot_angle=0;
  geo->GetOptD(fNam, "rot_x", rot_x);
  geo->GetOptD(fNam, "rot_y", rot_y);
  geo->GetOptD(fNam, "rot_z", rot_z);
  geo->GetOptD(fNam, "rot_angle", rot_angle, GeoParser::Unit(rad));
  G4ThreeVector rot_axis(rot_x, rot_y, rot_z);
  G4RotationMatrix rot(rot_axis, rot_angle); //CLHEP::HepRotation

  //transformation for placement to top volume
  G4ThreeVector pos(xpos, ypos, zpos);
  G4Transform3D transform(rot, pos); //HepGeom::Transform3D

  //put to the top volume
  new G4PVPlacement(transform, vol, fNam, top, false, 0);

  //clear all event variables
  ClearEvent();

}//PolTrackLay

//_____________________________________________________________________________
G4bool PolTrackLay::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //track in hit
  G4Track *track = step->GetTrack();

  //hit position
  const G4ThreeVector hp = step->GetPreStepPoint()->GetPosition();

  //add the hit
  fHitPdg.push_back( track->GetDynamicParticle()->GetPDGcode() ); // pdg
  fHitEtrack.push_back( track->GetTotalEnergy()/GeV ); // track energy
  fHitEdep.push_back( step->GetTotalEnergyDeposit()/GeV ); // deposited energy
  fHitX.push_back( hp.x()/mm ); // position x
  fHitY.push_back( hp.y()/mm ); // position y
  fHitZ.push_back( hp.z()/mm ); // position z
  fHitStepL.push_back( step->GetStepLength()/mm ); // step length

  return true;

}//ProcessHits

//_____________________________________________________________________________
void PolTrackLay::CreateOutput(TTree *tree) {

  //output from PolTrackLay

  DetUtils u(fNam, tree);

  u.AddBranch("_HitPdg", &fHitPdg); // pdg
  u.AddBranch("_HitEtrack", &fHitEtrack); // track energy, GeV
  u.AddBranch("_HitEdep", &fHitEdep); // deposited energy , GeV
  u.AddBranch("_HitX", &fHitX); // x, mm
  u.AddBranch("_HitY", &fHitY); // y, mm
  u.AddBranch("_HitZ", &fHitZ); // z, mm
  u.AddBranch("_HitStepL", &fHitStepL); // step length, mm

}//CreateOutput

//_____________________________________________________________________________
void PolTrackLay::ClearEvent() {

  fHitPdg.clear();
  fHitEtrack.clear();
  fHitEdep.clear();
  fHitX.clear();
  fHitY.clear();
  fHitZ.clear();
  fHitStepL.clear();

}//ClearEvent

//_____________________________________________________________________________
G4VisAttributes *PolTrackLay::ColorDecoder(GeoParser *geo) {

  G4String col("0:1:0:0.6"); // red:green:blue:alpha 
  geo->GetOptS(fNam, "vis", col);

  char_separator<char> sep(":");
  tokenizer< char_separator<char> > clin(col, sep);
  tokenizer< char_separator<char> >::iterator it = clin.begin();

  stringstream st;
  for(int i=0; i<4; i++) {
    st << *(it++) << " ";
  }

  G4double red=0, green=0, blue=0, alpha=0;
  st >> red >> green >> blue >> alpha;

  G4VisAttributes *vis = new G4VisAttributes();
  if(alpha < 1.1) {
    vis->SetColor(red, green, blue, alpha);
    vis->SetForceSolid(true);
  } else {
    vis->SetColor(red, green, blue);
    vis->SetForceAuxEdgeVisible(true);
  }

  return vis;

}//ColorDecoder
























