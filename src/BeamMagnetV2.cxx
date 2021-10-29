
//_____________________________________________________________________________
//
// beamline dipole magnet, version 2
//
//_____________________________________________________________________________

//C++
#include <typeinfo>

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
#include "G4VIntegrationDriver.hh"
#include "G4ChordFinder.hh"
#include "G4ClassicalRK4.hh"
#include "G4IntegrationDriver.hh"
#include "G4Mag_UsualEqRhs.hh"

//local headers
#include "BeamMagnetV2.h"
#include "GeoParser.h"

//_____________________________________________________________________________
BeamMagnetV2::BeamMagnetV2(G4String nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  BeamMagnetV2: " << fNam << G4endl;

  //center position along z, mm
  G4double zpos = 0;
  geo->GetOptD(fNam, "zpos", zpos, GeoParser::Unit(mm));

  //total length in z, mm
  G4double length = geo->GetD(fNam, "length")*mm;

  //conical inner core, entrance radius (r1) and exit radius (r2)
  G4double r1 = 10*mm, r2 = 10*mm;
  geo->GetOptD(fNam, "r1", r1, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "r2", r2, GeoParser::Unit(mm));

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

  //alternative stepper
  G4ClassicalRK4 *stepper = new G4ClassicalRK4(new G4Mag_UsualEqRhs(field));
  G4VIntegrationDriver *driver = new G4IntegrationDriver<G4ClassicalRK4>(5e-05*mm, stepper);
  G4ChordFinder *finder = new G4ChordFinder(driver);
  fman->SetChordFinder(finder);
  fman->SetMinimumEpsilonStep(5e-4);
  fman->SetMaximumEpsilonStep(0.01);

  //fman->CreateChordFinder(field);
  PrintField(fman);

  vol_inner->SetFieldManager(fman, true);

  //put the inner core to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol_inner, nam_inner, top, false, 0);

  //cylindrical outer shape
  G4double r3 = r2*2;
  geo->GetOptD(fNam, "r3", r3, GeoParser::Unit(mm)); // vessel outer radius
  G4Tubs *shape_outer = new G4Tubs(fNam+"_outer", 0., r3, length/2-1e-4*meter, 0., 360.*deg);

  //magnet vessel around the inner magnetic core
  G4SubtractionSolid *shape_vessel = new G4SubtractionSolid(fNam, shape_outer, shape_inner);

  G4Material *mat_outer = G4NistManager::Instance()->FindOrBuildMaterial("G4_Fe");
  G4LogicalVolume *vol_vessel = new G4LogicalVolume(shape_vessel, mat_outer, fNam);

  //vessel visibility
  G4VisAttributes *vis_vessel = new G4VisAttributes();
  vis_vessel->SetColor(0, 1, 0, 0.7); // blue
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

//_____________________________________________________________________________
void BeamMagnetV2::PrintField(G4FieldManager *fman) {

  G4ChordFinder *finder = fman->GetChordFinder();

  G4cout << "BeamMagnetV2:" << G4endl;
  G4cout << "eps_min: " << fman->GetMinimumEpsilonStep()/mm << G4endl;
  G4cout << "eps_max: " << fman->GetMaximumEpsilonStep()/mm << G4endl;
  //G4cout << "min_chord_step: " << fman-> << G4endl;
  G4cout << "delta_chord: " << finder->GetDeltaChord()/mm << G4endl;
  G4cout << "delta_intersection: " << fman->GetDeltaIntersection()/mm << G4endl;
  G4cout << "delta_one_step: " << fman->GetDeltaOneStep()/mm << G4endl;
  //G4cout << "largest_step: " << fman-> << G4endl;

  G4VIntegrationDriver *driver = fman->GetChordFinder()->GetIntegrationDriver();
  driver->SetVerboseLevel(3);

  G4MagIntegratorStepper *stepper = driver->GetStepper();
  G4cout << "stepper: " << typeid(*stepper).name() << G4endl;

  G4EquationOfMotion *eq = stepper->GetEquationOfMotion();
  G4cout << "equation: " << typeid(*eq).name() << G4endl;






}//PrintField


































