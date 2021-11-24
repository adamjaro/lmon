
//_____________________________________________________________________________
//
// spectrometer dipole magnet
//
//_____________________________________________________________________________

//Geant headers
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Tubs.hh"
#include "G4SystemOfUnits.hh"
#include "G4PVPlacement.hh"
#include "G4FieldManager.hh"
#include "G4UniformMagField.hh"
#include "G4VisAttributes.hh"

//local headers
#include "Magnet.h"
#include "GeoParser.h"

//_____________________________________________________________________________
Magnet::Magnet(const G4String& nam, GeoParser *geo, G4LogicalVolume *top) {

  G4cout << "  Magnet: " << nam << G4endl;

  //center position along z
  G4double zpos = geo->GetD(nam, "zpos")*mm;

  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");

  //magnet shape
  G4double dz = geo->GetD(nam, "dz")*mm;
  G4double inner_r = geo->GetD(nam, "inner_r")*mm;

  G4Tubs *mshape = new G4Tubs(nam, 0., inner_r, dz/2., 0., 360.*deg);
  G4LogicalVolume *mvol = new G4LogicalVolume(mshape, mat, nam);

  G4VisAttributes *vis = new G4VisAttributes();
  //vis->SetColor(1, 1, 0); // yellow
  vis->SetColor(1, 0, 1); // magenta
  vis->SetLineWidth(1); // 2
  mvol->SetVisAttributes(vis);

  //magnetic field
  G4double dipole_field = geo->GetD(nam, "field") * tesla; // magnet field
  G4UniformMagField *field = new G4UniformMagField(G4ThreeVector(dipole_field, 0, 0));
  G4FieldManager *fman = new G4FieldManager();
  fman->SetDetectorField(field);
  fman->CreateChordFinder(field);

  mvol->SetFieldManager(fman, true);

  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), mvol, nam, top, false, 0);

}//Magnet

























