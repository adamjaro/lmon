
//_____________________________________________________________________________
//
// Vacuum section in front of taggers
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
#include "VacTaggerWin.h"
#include "GeoParser.h"

using namespace std;

//_____________________________________________________________________________
VacTaggerWin::VacTaggerWin(const G4String& nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), fNam(nam) {

  G4cout << "VacTaggerWin: " << fNam << G4endl;

  // full size in y, mm
  G4double ysiz = geo->GetD(fNam, "ysiz")*mm;

  G4double zB = geo->GetD(fNam, "zB")*mm;
  G4double xB = geo->GetD(fNam, "xB")*mm;

  G4double zT = geo->GetD(fNam, "zT")*mm;
  G4double xT = geo->GetD(fNam, "xT")*mm;
  G4double zTB = geo->GetD(fNam, "zTB")*mm;
  G4double xTB = geo->GetD(fNam, "xTB")*mm;


  //generic trapezoid native coordinates: 4 xy points plane at -dz, 4 xy points plane at +dz, both clockwise
  //rotation by +pi/2 about x from generic trapezoid coordinates to detector frame: y -> z,  z -> y

  //vertices for the trapezoid
  vector<G4TwoVector> ver(8);

  ver[0].set(xTB, zTB);

  ver[1].set(xB, zB);

  ver[2].set(xB, zB);

  ver[3].set(xT, zT);

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

}//VacTaggerWin

















