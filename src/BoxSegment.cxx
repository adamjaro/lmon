
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

  G4cout << "  BoxSegment: " << fNam << G4endl;

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

  //center position, m
  G4double xpos=0*mm, ypos=0*mm, zpos=0*mm;
  geo->GetOptD(fNam, "xpos", xpos, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "ypos", ypos, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "zpos", zpos, GeoParser::Unit(mm));

  //polar angle along the y axis
  G4double theta = 0;
  geo->GetOptD(fNam, "theta", theta, GeoParser::Unit(rad));
  G4RotationMatrix rot(G4ThreeVector(0, 1, 0), theta); //CLHEP::HepRotation

  //placement in top
  G4ThreeVector pos(xpos, ypos, zpos);
  G4Transform3D transform(rot, pos); //HepGeom::Transform3D

  new G4PVPlacement(transform, vol, fNam, top, false, 0);

}//BoxSegment














