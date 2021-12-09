
//_____________________________________________________________________________
//
// Construction box segment
//
//_____________________________________________________________________________

//Geant
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4PVPlacement.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"
#include "G4ThreeVector.hh"

//local classes
#include "BoxSegment.h"
#include "GeoParser.h"

using namespace std;

//_____________________________________________________________________________
BoxSegment::BoxSegment(const G4String& nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), fNam(nam) {

  G4cout << "BoxSegment: " << fNam << G4endl;

  //full size in x, y and z, mm
  G4double dx = geo->GetD(fNam, "dx")*mm;
  G4double dy = geo->GetD(fNam, "dy")*mm;
  G4double dz = geo->GetD(fNam, "dz")*mm;
  G4Box *shape = new G4Box(fNam, dx/2, dy/2, dz/2);

  //logical volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 0, 1);
  //vis->SetForceSolid(true);
  vis->SetForceWireframe();
  vol->SetVisAttributes(vis);

  //center position, mm
  G4double xpos=0*mm, ypos=0*mm, zpos=0*mm;
  geo->GetOptD(fNam, "xpos", xpos, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "ypos", ypos, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "zpos", zpos, GeoParser::Unit(mm));

  G4cout << "  " << fNam << ", xpos: " << xpos << G4endl;
  G4cout << "  " << fNam << ", ypos: " << ypos << G4endl;
  G4cout << "  " << fNam << ", zpos: " << zpos << G4endl;

  //polar angle along the y axis
  G4double theta = 0;
  geo->GetOptD(fNam, "theta", theta, GeoParser::Unit(rad));

  //select the rotation axis
  G4ThreeVector rot_axis(0, 1, 0); // y
  G4bool rotate_x = false;
  geo->GetOptB(fNam, "rotate_x", rotate_x);
  if(rotate_x) {
    rot_axis = G4ThreeVector(1, 0, 0); // x
  }

  G4RotationMatrix rot(rot_axis, theta); //CLHEP::HepRotation
  G4cout << "  " << fNam << ", theta: " << theta << G4endl;

  //placement in top
  G4ThreeVector pos(xpos, ypos, zpos);
  G4Transform3D transform(rot, pos); //HepGeom::Transform3D

  new G4PVPlacement(transform, vol, fNam, top, false, 0);

}//BoxSegment














