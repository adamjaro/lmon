
//_____________________________________________________________________________
//
// beamline dipole magnet, version 2, intended first for B2eR
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

//_____________________________________________________________________________
BeamMagnetV2::BeamMagnetV2(G4String nam, G4double zpos, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  //conical inner core
  G4double length = 5.5*meter;
  G4double r1 = 0.097*meter;
  G4double r2 = 0.139*meter;

  G4String nam_inner = fNam+"_inner";
  G4Cons *shape_inner = new G4Cons(nam_inner, 0, r2, 0, r1, length/2, 0, 360*deg);

  G4Material *mat_inner = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol_inner = new G4LogicalVolume(shape_inner, mat_inner, nam_inner);
  vol_inner->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //magnetic field inside the inner core
  G4UniformMagField *field = new G4UniformMagField(G4ThreeVector(0, -0.198*tesla, 0));
  G4FieldManager *fman = new G4FieldManager();
  fman->SetDetectorField(field);
  fman->CreateChordFinder(field);

  vol_inner->SetFieldManager(fman, true);

  //put the inner core to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol_inner, nam_inner, top, false, 0);

  //cylindrical outer shape
  G4double r3 = 0.2*meter;
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



































