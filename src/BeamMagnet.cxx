
//_____________________________________________________________________________
//
// beamline dipole magnet, intended first for B2eR
//
//_____________________________________________________________________________

//Geant headers
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Cons.hh"
#include "G4SystemOfUnits.hh"
#include "G4PVPlacement.hh"
#include "G4FieldManager.hh"
#include "G4UniformMagField.hh"
#include "G4VisAttributes.hh"

//local headers
#include "BeamMagnet.h"

//_____________________________________________________________________________
BeamMagnet::BeamMagnet(G4double zpos, G4LogicalVolume *top) {

  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");

  //conical shape
  G4double length = 5.5*meter;
  G4double r1 = 0.097*meter;
  G4double r2 = 0.139*meter;

  G4String nam = "B2eR";
  G4Cons *shape = new G4Cons(nam, 0, r2, 0, r1, length/2, 0, 360*deg);
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, nam);

  G4VisAttributes *vis = new G4VisAttributes();
  //vis->SetColor(1, 1, 0); // yellow
  //vis->SetColor(1, 0, 1); // magenta
  vis->SetColor(0, 0, 1); // blue
  vis->SetLineWidth(2);
  //vis->SetForceSolid();
  vis->SetForceAuxEdgeVisible();
  vol->SetVisAttributes(vis);

  //maginetic field
  G4UniformMagField *field = new G4UniformMagField(G4ThreeVector(0, -0.198*tesla, 0));
  G4FieldManager *fman = new G4FieldManager();
  fman->SetDetectorField(field);
  fman->CreateChordFinder(field);

  vol->SetFieldManager(fman, true);

  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol, nam, top, false, 0);

}//BeamMagnet





















