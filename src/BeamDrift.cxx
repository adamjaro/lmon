
//_____________________________________________________________________________
//
// Beam drift section between B2 and Q3 magnets
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
#include "BeamDrift.h"
#include "GeoParser.h"
//#include "ComponentBuilder.h"

using namespace std;

//_____________________________________________________________________________
BeamDrift::BeamDrift(G4String nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), fNam(nam) {

  G4cout << "BeamDrift: " << fNam << G4endl;

  // full size in y, mm
  G4double ysiz = geo->GetD(fNam, "ysiz")*mm;

  //at at lower z
  G4double z0T = geo->GetD(fNam, "z0T")*mm;
  G4double x0T = geo->GetD(fNam, "x0T")*mm;
  G4double z0B = geo->GetD(fNam, "z0B")*mm;
  G4double x0B = geo->GetD(fNam, "x0B")*mm;

  //at larger z
  G4double z1T = geo->GetD(fNam, "z1T")*mm;
  G4double x1T = geo->GetD(fNam, "x1T")*mm;
  G4double z1B = geo->GetD(fNam, "z1B")*mm;
  G4double x1B = geo->GetD(fNam, "x1B")*mm;

  //G4GenericTrap or TGeoArb8
  //generic trapezoid native coordinates: 4 xy points plane at -dz, 4 xy points plane at +dz, both clockwise
  //rotation by +pi/2 about x from generic trapezoid coordinates to detector frame: y -> z,  z -> y

  //vertices for the trapezoid
  vector<G4TwoVector> ver(8);

  ver[0].set(x0B, z0B); // point #1

  ver[1].set(x1B, z1B); // point #2

  ver[2].set(x1T, z1T); // point #3

  ver[3].set(x0T, z0T); // point #4

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
  //G4RotationMatrix rot(G4ThreeVector(1, 0, 0), 0); //CLHEP::HepRotation

  //placement in top
  G4ThreeVector pos(0, 0, 0);
  G4Transform3D transform(rot, pos); //HepGeom::Transform3D

  new G4PVPlacement(transform, vol, fNam, top, false, 0);

}//BeamDrift

















