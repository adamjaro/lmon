
//_____________________________________________________________________________
//
// beam quadrupole magnet, its vessel absorbes all particles, no secondaries
//
//_____________________________________________________________________________

//C++
#include "math.h"

//Geant
#include "G4Cons.hh"
#include "G4LogicalVolume.hh"
#include "G4SystemOfUnits.hh"
#include "G4NistManager.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"
#include "G4QuadrupoleMagField.hh"
#include "G4FieldManager.hh"
#include "G4RotationMatrix.hh"

//local classes
#include "GeoParser.h"
#include "BeamQuadrupole.h"

//_____________________________________________________________________________
BeamQuadrupole::BeamQuadrupole(G4String nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  BeamQuadrupole: " << fNam << G4endl;

  //magnet center along z, mm
  G4double zpos = -1;
  geo->GetOptD(fNam, "zpos", zpos, GeoParser::Unit(mm));

  //length, mm
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

  //inner radii
  G4double r1 = geo->GetD(fNam, "r1") * mm; // inner radius closer to the IP
  G4double r2 = geo->GetD(fNam, "r2") * mm; // inner radious further from the IP

  //radial thickness, mm
  G4double dr = 40;
  geo->GetOptD(fNam, "dr", dr);

  //magnet inner core
  G4String nam_mag = fNam+"_mag";
  G4Cons *shape_mag = new G4Cons(nam_mag, 0, r2, 0, r1, length/2, 0, 360*deg);

  //core logical volume
  G4Material *mat_core = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol_mag = new G4LogicalVolume(shape_mag, mat_core, nam_mag);
  vol_mag->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //quadrupole field inside the core
  G4double grad = geo->GetD(fNam, "grad") * tesla/meter; // field gradient, T/m
  G4double angle = 90; // deg, field angle
  geo->GetOptD(fNam, "angle", angle);
  G4RotationMatrix *rot = new G4RotationMatrix(G4ThreeVector(0, 0, 1), angle*deg); //is typedef to CLHEP::HepRotation
  G4QuadrupoleMagField *field = new G4QuadrupoleMagField(grad, G4ThreeVector(0, 0, zpos), rot);

  G4FieldManager *fman = new G4FieldManager();
  fman->SetDetectorField(field);
  fman->CreateChordFinder(field);
  vol_mag->SetFieldManager(fman, true);

  //put the inner core to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol_mag, nam_mag, top, false, 0);

  //vessel shape
  G4Cons *shape = new G4Cons(fNam, r2, r2+dr, r1, r1+dr, length/2, 0, 360*deg);

  //vessel logical volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Fe");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //vessel visibility
  G4VisAttributes *vis_vessel = new G4VisAttributes();
  vis_vessel->SetColor(0, 0, 1); // blue
  vis_vessel->SetLineWidth(2);
  vis_vessel->SetForceSolid(true);
  //vis_vessel->SetForceAuxEdgeVisible(true);
  vol->SetVisAttributes(vis_vessel);

  //put the vessel cone to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol, fNam, top, false, 0);

}//ConeAperture

//_____________________________________________________________________________
G4bool BeamQuadrupole::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //remove the track entering the cone aperture vessel
  G4Track *track = step->GetTrack();
  track->SetTrackStatus(fKillTrackAndSecondaries);

  return true;

}//ProcessHits
















