
//_____________________________________________________________________________
//
// Vacuum drift section between B2 and Q3 magnets
//
//_____________________________________________________________________________

//ROOT
#include "TMath.h"

//Geant
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4GenericTrap.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4PVPlacement.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"
#include "G4ThreeVector.hh"

//local classes
#include "VacDrift.h"
#include "GeoParser.h"

using namespace std;

//_____________________________________________________________________________
VacDrift::VacDrift(const G4String& nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), fNam(nam) {

  G4cout << "VacDrift: " << fNam << G4endl;

  // full size in y, mm
  G4double ysiz = geo->GetD(fNam, "ysiz")*mm;

  //at Q3eR
  G4double zQT = geo->GetD(fNam, "zQT")*mm;
  G4double xQT = geo->GetD(fNam, "xQT")*mm;
  G4double zQB = geo->GetD(fNam, "zQB")*mm;
  G4double xQB = geo->GetD(fNam, "xQB")*mm;

  //at exit window
  G4double zW = geo->GetD(fNam, "zW")*mm;
  G4double xW = geo->GetD(fNam, "xW")*mm;
  G4double xA = geo->GetD(fNam, "xA")*mm;

  //generic trapezoid native coordinates: 4 xy points plane at -dz, 4 xy points plane at +dz, both clockwise
  //rotation by +pi/2 about x from generic trapezoid coordinates to detector frame: y -> z,  z -> y

  //vertices for the trapezoid
  vector<G4TwoVector> ver(8);

  ver[0].set(xQB, zQB);

  ver[1].set(xQT, zQT);

  ver[2].set(xW, zW);

  ver[3].set(xA, zW);

  //plane at lower y
  for(int i=4; i<8; i++) {
    ver[i].set(ver[i-4].x(), ver[i-4].y());
  }

  G4GenericTrap *shape = new G4GenericTrap(fNam, ysiz/2, ver);

  //logical volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 0, 1);
  //vis->SetForceSolid(true);
  vis->SetForceWireframe();
  vol->SetVisAttributes(vis);

  //placement in top
  G4RotationMatrix rot(G4ThreeVector(1, 0, 0), TMath::Pi()/2); //CLHEP::HepRotation

  //placement in top
  G4ThreeVector pos(0, 0, 0);
  G4Transform3D transform(rot, pos); //HepGeom::Transform3D

  new G4PVPlacement(transform, vol, fNam, top, false, 0);

}//VacDrift

















