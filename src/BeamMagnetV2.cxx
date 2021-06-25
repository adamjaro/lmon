
//_____________________________________________________________________________
//
// beamline dipole magnet, version 2
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
#include "G4Tubs.hh"
#include "G4SubtractionSolid.hh"

//local headers
#include "BeamMagnetV2.h"
#include "GeoParser.h"

//_____________________________________________________________________________
BeamMagnetV2::BeamMagnetV2(G4String nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  BeamMagnetV2: " << fNam << G4endl;

  //center position along z, mm
  G4double zpos = -1;
  geo->GetOptD(fNam, "zpos", zpos, GeoParser::Unit(mm));

  //total length in z, mm
  G4double length = -1;
  geo->GetOptD(fNam, "length", length, GeoParser::Unit(mm));

  //start and end along z, meters
  G4double z1 = -1, z2 = -1;
  G4bool z1def = geo->GetOptD(fNam, "z1", z1, GeoParser::Unit(m));
  G4bool z2def = geo->GetOptD(fNam, "z2", z2, GeoParser::Unit(m));

  //center along z and length from z1 and z2
  if(z1def and z2def) {
    zpos = z1 + (z2-z1)/2.;
    length = std::abs(z2) - std::abs(z1);
  }

  G4cout << "    zpos: " << zpos << G4endl;
  G4cout << "    length: " << length << G4endl;

  //conical inner core, entrance radius (r1) and exit radius (r2)
  G4double r1 = 1*mm, r2 = 1*mm;
  geo->GetOptD(fNam, "r1", r1, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "r2", r2, GeoParser::Unit(mm));
  //radii from diameters
  G4double d1, d2;
  if( geo->GetOptD(fNam, "d1", d1, GeoParser::Unit(mm)) ) {
    r1 = d1/2;
  }
  if( geo->GetOptD(fNam, "d2", d2, GeoParser::Unit(mm)) ) {
    r2 = d2/2;
  }
  G4cout << "    r1: " << r1 << G4endl;
  G4cout << "    r2: " << r2 << G4endl;

  G4String nam_inner = fNam+"_inner";
  G4Cons *shape_inner = new G4Cons(nam_inner, 0, r2, 0, r1, length/2, 0, 360*deg);

  G4Material *mat_inner = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol_inner = new G4LogicalVolume(shape_inner, mat_inner, nam_inner);
  vol_inner->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //magnetic field inside the inner core
  G4double dipole_field = geo->GetD(fNam, "field") * tesla; // magnet field
  G4UniformMagField *field = new G4UniformMagField(G4ThreeVector(0, dipole_field, 0));
  G4FieldManager *fman = new G4FieldManager();
  fman->SetDetectorField(field);
  fman->CreateChordFinder(field);

  vol_inner->SetFieldManager(fman, true);

  //put the inner core to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol_inner, nam_inner, top, false, 0);

  //cylindrical outer shape
  G4double r3 = geo->GetD(fNam, "rout") * mm; // vessel outer radius
  G4Tubs *shape_outer = new G4Tubs(fNam+"_outer", 0., r3, length/2-1e-4*meter, 0., 360.*deg);

  //magnet vessel around the inner magnetic core
  G4SubtractionSolid *shape_vessel = new G4SubtractionSolid(fNam, shape_outer, shape_inner);

  G4Material *mat_outer = G4NistManager::Instance()->FindOrBuildMaterial("G4_Fe");
  G4LogicalVolume *vol_vessel = new G4LogicalVolume(shape_vessel, mat_outer, fNam);

  //vessel visibility
  G4VisAttributes *vis_vessel = new G4VisAttributes();
  vis_vessel->SetColor(0, 0, 1); // blue
  vis_vessel->SetLineWidth(2);
  vis_vessel->SetForceSolid(true);
  //vis_vessel->SetForceAuxEdgeVisible(true);
  vol_vessel->SetVisAttributes(vis_vessel);

  //put the magnet vessel to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol_vessel, fNam, top, false, 0);

}//BeamMagnetV2

//_____________________________________________________________________________
G4bool BeamMagnetV2::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //remove the track entering the magnet vessel
  G4Track *track = step->GetTrack();
  track->SetTrackStatus(fKillTrackAndSecondaries);

  return true;

}//ProcessHits



































