
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
#include "G4VIntegrationDriver.hh"
#include "G4ChordFinder.hh"
#include "G4DormandPrinceRK78.hh"
#include "G4DormandPrince745.hh"
#include "G4DormandPrinceRK56.hh"
#include "G4MagErrorStepper.hh"
#include "G4ClassicalRK4.hh"
//#include "G4TDormandPrince45.hh"
#include "G4Mag_UsualEqRhs.hh"
#include "G4IntegrationDriver.hh"

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

  //inner radii closer to the IP (r1) and further from the IP (r2)
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
  G4QuadrupoleMagField *field = 0x0;
  G4double angle = 0*deg; // deg, field angle
  if( geo->GetOptD(fNam, "angle", angle, GeoParser::Unit(deg)) ) {
    G4RotationMatrix *rot = new G4RotationMatrix(G4ThreeVector(0, 0, 1), angle); //is typedef to CLHEP::HepRotation
    field = new G4QuadrupoleMagField(grad, G4ThreeVector(0, 0, 0), rot);
  } else {
    field = new G4QuadrupoleMagField(grad);
  }

  G4FieldManager *fman = new G4FieldManager();
  fman->SetDetectorField(field);

  //alternative stepper
  //fman->SetMinimumEpsilonStep(5e-2);
  //fman->SetMaximumEpsilonStep(0.1);
  //G4ClassicalRK4 *stepper = new G4ClassicalRK4(new G4Mag_UsualEqRhs(field));
  //G4VIntegrationDriver *driver = new G4IntegrationDriver<G4ClassicalRK4>(5e-2*mm, stepper);
  //G4ChordFinder *finder = new G4ChordFinder(driver);
  //fman->SetChordFinder(finder);

  fman->CreateChordFinder(field);
  PrintField(fman);
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

//_____________________________________________________________________________
void BeamQuadrupole::PrintField(G4FieldManager *fman) {

  G4ChordFinder *finder = fman->GetChordFinder();

  G4cout << "BeamQuadrupole:" << G4endl;
  G4cout << "eps_min: " << fman->GetMinimumEpsilonStep()/mm << G4endl;
  G4cout << "eps_max: " << fman->GetMaximumEpsilonStep()/mm << G4endl;
  //G4cout << "min_chord_step: " << fman-> << G4endl;
  G4cout << "delta_chord: " << finder->GetDeltaChord()/mm << G4endl;
  G4cout << "delta_intersection: " << fman->GetDeltaIntersection()/mm << G4endl;
  G4cout << "delta_one_step: " << fman->GetDeltaOneStep()/mm << G4endl;
  //G4cout << "largest_step: " << fman-> << G4endl;

  G4cout << "finder: " << typeid(*fman->GetChordFinder()).name() << G4endl;

  G4VIntegrationDriver *driver = fman->GetChordFinder()->GetIntegrationDriver();
  G4cout << "driver: " << typeid(*driver).name() << G4endl;
  //driver->SetVerboseLevel(3);

  G4MagIntegratorStepper *stepper = driver->GetStepper();
  G4cout << "stepper: " << typeid(*stepper).name() << G4endl;
  //G4DormandPrince745
  //G4DormandPrinceRK78
  //G4DormandPrinceRK56
  //G4MagErrorStepper
  //G4ClassicalRK4
  //G4MagIntegratorStepper
  //G4TDormandPrince45
  //G4cout << "cast: " << dynamic_cast<G4TDormandPrince45*>(stepper) << G4endl;
  //G4cout << "cast: " << dynamic_cast<G4TDormandPrince45<G4Mag_UsualEqRhs>*>(stepper) << G4endl;

  G4EquationOfMotion *eq = stepper->GetEquationOfMotion();
  G4cout << "equation: " << typeid(*eq).name() << G4endl;






}//PrintField














