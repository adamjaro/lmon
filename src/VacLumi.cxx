
//_____________________________________________________________________________
//
// Vacuum section in luminosity system
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
#include "VacLumi.h"
#include "GeoParser.h"

using namespace std;

//_____________________________________________________________________________
VacLumi::VacLumi(const G4String& nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), fNam(nam) {

  G4cout << "VacLumi: " << fNam << G4endl;

  //start and end in z
  G4double z0 = geo->GetD(fNam, "z0")*mm;
  G4double z1 = geo->GetD(fNam, "z1")*mm;

  //full length in z and center position along z
  G4double zsiz = z0 - z1;
  G4double zcen = (z0+z1)/2;

  //points
  G4double dX0 = geo->GetD(fNam, "dX0")*mm;
  G4double dY0 = geo->GetD(fNam, "dY0")*mm;
  G4double dX1 = geo->GetD(fNam, "dX1")*mm;
  G4double dY1 = geo->GetD(fNam, "dY1")*mm;

  //vertices for the trapezoid
  vector<G4TwoVector> ver(8);

  //plane at lower z
  ver[0].set(-dX1, -dY1);

  ver[1].set(-dX1, dY1);

  ver[2].set(dX1, dY1);

  ver[3].set(dX1, -dY1);

  //plane at higher z
  ver[4].set(-dX0, -dY0);

  ver[5].set(-dX0, dY0);

  ver[6].set(dX0, dY0);

  ver[7].set(dX0, -dY0);

  G4GenericTrap *shape = new G4GenericTrap(fNam, zsiz/2, ver);

  //logical volume
  G4String inner_material = "G4_Galactic";
  geo->GetOptS(fNam, "inner_material", inner_material);
  G4cout << "  " << fNam << ", inner_material: " << inner_material << G4endl;
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial(inner_material);
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 0, 1);
  //vis->SetForceSolid(true);
  vis->SetForceWireframe();
  vol->SetVisAttributes(vis);

  //placement in top
  new G4PVPlacement(0, G4ThreeVector(0, 0, zcen), vol, fNam, top, false, 0);

}//VacLumi

















