
//_____________________________________________________________________________
//
// collimator between photon exit window and dipole magnet
//
//_____________________________________________________________________________

//Geant headers
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4SubtractionSolid.hh"
#include "G4SystemOfUnits.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"

//local headers
#include "Collimator.h"

//_____________________________________________________________________________
Collimator::Collimator(G4double zpos, G4LogicalVolume *top) {

  //inner aperture in x and y
  G4double dx = 9.6*cm;
  G4double dy = 7*cm;

  //length
  G4double len = 30*cm;

  //outer size
  G4double siz = 50*cm;

  //collimator shape
  G4String nam = "Collimator";
  G4Box *outer = new G4Box(nam, siz/2, siz/2, len/2);
  G4Box *inner = new G4Box(nam, dx/2, dy/2, len/2);
  G4SubtractionSolid *shape = new G4SubtractionSolid(nam, outer, inner);

  //collimator volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_STAINLESS-STEEL");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, nam);

  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(1, 1, 0);
  //vis->SetLineWidth(2);
  vol->SetVisAttributes(vis);

  //put the collimator to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos-len/2), vol, nam, top, false, 0);

}//Collimator





















