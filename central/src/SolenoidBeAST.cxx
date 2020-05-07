
//_____________________________________________________________________________
//
// central solenoid with BeAST field map
//
//_____________________________________________________________________________

//C++
#include <stdlib.h>
#include <string>

//Geant
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"
#include "G4Tubs.hh"
#include "G4FieldManager.hh"

//local classes
#include "SolenoidBeAST.h"
#include "BeastMagneticField.h"
#include "GeoParser.h"

using namespace std;

//_____________________________________________________________________________
SolenoidBeAST::SolenoidBeAST(G4String nam, GeoParser *geo, G4LogicalVolume *top) {

  G4cout << "  SolenoidBeAST: " << nam << G4endl;

  //solenoid dimensions
  //G4double length = 10000*mm;
  G4double length = 6556*mm;
  G4double radius = 2500*mm;

  //cylinder shape
  G4Tubs *shape = new G4Tubs(nam, 0, radius, length/2, 0., 360.*deg);

  //logical volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, nam);

  //field map
  string map = geo->GetS(nam, "map");
  if(map.find("~") == 0) {
    string hdir(getenv("HOME"));
    map = hdir + "/" + map.substr(1);
  }

  //G4cout << map << G4endl;

  //magnetic field
  G4MagneticField *field = new Field(new BeastMagneticField(map.c_str()));
  G4FieldManager *fman = new G4FieldManager();
  fman->SetDetectorField(field);
  fman->CreateChordFinder(field);
  vol->SetFieldManager(fman, true);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 0, 1); // blue
  vis->SetLineWidth(2);
  //vis->SetForceSolid(true);
  //vis->SetForceAuxEdgeVisible(true);
  vol->SetVisAttributes(vis);

  //put the solenoid to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0), vol, nam, top, false, 0);

}//SolenoidBeAST

//_____________________________________________________________________________
void SolenoidBeAST::Field::GetFieldValue(const G4double p[4], G4double *B) const {

  //coordinates in cm, field in T
  double bx, by, bz;
  fMap->GetFieldValue(p[0]/cm, p[1]/cm, p[2]/cm, bx, by, bz);

  //G4cout << "Field::GetFieldValue, " << p[0]/cm << " " << bx << G4endl;

  B[0] = bx*tesla;
  B[1] = by*tesla;
  B[2] = bz*tesla;

}//GetFieldValue


















