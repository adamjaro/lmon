
//_____________________________________________________________________________
//
// Carbon target
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <string>
#include <sstream>

//Boost
#include <boost/tokenizer.hpp>

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
#include "PolCTarget.h"
#include "GeoParser.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
PolCTarget::PolCTarget(const G4String& nam, GeoParser *geo, G4LogicalVolume *top):
  Detector(), fNam(nam) {

  G4cout << "PolCTarget: " << fNam << G4endl;

  //full size in x, y and z, mm
  G4double dx = geo->GetD(fNam, "dx")*mm;
  G4double dy = geo->GetD(fNam, "dy")*mm;
  G4double dz = geo->GetD(fNam, "dz")*mm;
  G4Box *shape = new G4Box(fNam, dx/2, dy/2, dz/2);

  //carbon material
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_C");

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

}//PolCTarget

//_____________________________________________________________________________
G4VisAttributes *PolCTarget::ColorDecoder(GeoParser *geo) {

  G4String col("0.5:0.5:0.5:1"); // red:green:blue:alpha 
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
























