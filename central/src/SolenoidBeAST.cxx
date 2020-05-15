
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
#include "G4SubtractionSolid.hh"
#include "G4RotationMatrix.hh"
#include "G4Transform3D.hh"
#include "G4UniformMagField.hh"

//local classes
#include "SolenoidBeAST.h"
#include "BeastMagneticField.h"
#include "GeoParser.h"

using namespace std;

//_____________________________________________________________________________
SolenoidBeAST::SolenoidBeAST(G4String nam, GeoParser *geo, G4LogicalVolume *top) {

  G4cout << "  SolenoidBeAST: " << nam << G4endl;

  //solenoid dimensions
  G4double length = geo->GetD(nam, "length") * mm;
  G4double radius = geo->GetD(nam, "radius") * mm;

  G4double zcut = 0; // cutout at negative z, position, mm
  G4double rcut = 0; // radius of the cutout
  geo->GetOptD(nam, "zcut", zcut);
  geo->GetOptD(nam, "rcut", rcut);

  //shape
  G4VSolid *shape = 0;
  if(rcut < 1e-3) {
    //default cylinder
    shape = new G4Tubs(nam, 0, radius, length/2, 0., 360.*deg);
    //shape = new G4Tubs(nam, 0, radius, length/2, 90*deg, 270.*deg); // for drawing
  } else {
    //cylinder with cutout at negative z
    shape = CylWithCutout(nam, radius, length, zcut, rcut);
  }

  //logical volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, nam);
  fVol = vol;

  //magnetic field
  G4MagneticField *field = 0;
  G4bool set_uniform = false; // override for uniform field along z
  geo->GetOptB(nam, "set_uniform", set_uniform);

  //construct the field
  if( !set_uniform ) {

    //field map
    string map = geo->GetS(nam, "map");
    if(map.find("~") == 0) {
      string hdir(getenv("HOME"));
      map = hdir + "/" + map.substr(1);
    }
    field = new Field(new BeastMagneticField(map.c_str()));

  } else {

    //override active for uniform field along z
    G4double uniform_field = geo->GetD(nam, "uniform_field") * tesla;
    field = new G4UniformMagField(G4ThreeVector(0, 0, uniform_field));
  }

  //set the field to field manager
  G4FieldManager *fman = new G4FieldManager();
  fman->SetDetectorField(field);
  fman->CreateChordFinder(field);
  vol->SetFieldManager(fman, true);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  //vis->SetColor(0, 0, 1); // blue
  vis->SetColor(0.7, 0.15, 0.15); // dark red
  vis->SetLineWidth(2);
  //vis->SetForceSolid(true);
  //vis->SetForceAuxEdgeVisible(true);
  vol->SetVisAttributes(vis);

  //put the solenoid to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0), vol, nam, top, false, 0);

}//SolenoidBeAST

//_____________________________________________________________________________
void SolenoidBeAST::Field::GetFieldValue(const G4double p[4], G4double *B) const {

  //G4cout << "Field::GetFieldValue, " << p << " " << p[0] << " " << p[1] << " " << p[2] << G4endl;

  //coordinates in cm, field in T
  double bx, by, bz;
  fMap->GetFieldValue(p[0]/cm, p[1]/cm, p[2]/cm, bx, by, bz);

  //G4cout << "Field::GetFieldValue, " << p[0]/cm << " " << bx << G4endl;

  B[0] = bx*tesla;
  B[1] = by*tesla;
  B[2] = bz*tesla;

}//GetFieldValue

//_____________________________________________________________________________
G4VSolid *SolenoidBeAST::CylWithCutout(G4String nam, G4double r, G4double len, G4double zs, G4double r1) {

  G4cout << "SolenoidBeAST::CylWithCutout" << G4endl;

  //outer cylinder
  G4Tubs *shape_outer = new G4Tubs(nam, 0, r, len/2, 0., 360.*deg);
  //G4Tubs *shape_outer = new G4Tubs(nam, 0, r, len/2, 90*deg, 270.*deg); // for drawing

  //cutout inner cylinder
  G4double lcut = (len/2)+zs;
  G4Tubs *cutout = new G4Tubs(nam, 0, r1, lcut/2, 0., 360.*deg);

  //cutout position at negative zs
  G4double zcut = zs - lcut/2;

  G4RotationMatrix rot(0, 0, 0);
  G4ThreeVector pos(0, 0, zcut);
  G4Transform3D transform(rot, pos); // is HepGeom::Transform3D

  G4SubtractionSolid *shape = new G4SubtractionSolid(nam, shape_outer, cutout, transform);

  return shape;

}//CylWithCutout
















