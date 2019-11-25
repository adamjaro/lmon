
//_____________________________________________________________________________
//
// simple exit window as an Al disc
//
//_____________________________________________________________________________

//Geant headers
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Tubs.hh"
#include "G4SystemOfUnits.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"

//local headers
#include "ExitWindow.h"

//_____________________________________________________________________________
ExitWindow::ExitWindow(G4double zpos, G4LogicalVolume *top) {

  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Al");

  G4double radius = 5.*cm;
  G4double dz = 1.*cm;

  G4String nam = "ExitWindow";
  G4Tubs *shape = new G4Tubs(nam, 0., radius, dz, 0., 360.*deg);
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, nam);

  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 1, 0, 0.5);
  vis->SetForceSolid(true);
  vol->SetVisAttributes(vis);

  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos-dz/2.), vol, nam, top, false, 0);

  //G4cout << *(G4Material::GetMaterialTable()) << G4endl;

}//ExitWindow

