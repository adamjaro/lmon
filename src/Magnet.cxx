
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
Magnet::Magnet(const G4String& nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam), fRemoveTracks(0) {

  G4cout << "  Magnet: " << fNam << G4endl;

  //center position along z
  G4double zpos = geo->GetD(fNam, "zpos")*mm;

  //magnet shape
  G4double dz = geo->GetD(nam, "dz")*mm;
  G4double inner_r = geo->GetD(nam, "inner_r")*mm;
  G4double outer_r = inner_r + 10.*mm;
  geo->GetOptD(fNam, "outer_r", outer_r, GeoParser::Unit(mm));

  //main volume holding inner magnetic core and outer solid vessel
  G4String main_nam = fNam+"_main";
  G4Tubs *main_shape = new G4Tubs(main_nam, 0., outer_r, dz/2., 0., 360.*deg);

  //main logical volume
  G4Material *vac_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *main_vol = new G4LogicalVolume(main_shape, vac_mat, main_nam);
  main_vol->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //inner magnetic core
  G4String core_nam = fNam+"_core";
  G4Tubs *core_shape = new G4Tubs(core_nam, 0., inner_r, dz/2., 0., 360.*deg);

  //inner volume
  G4String inner_material = "G4_Galactic";
  geo->GetOptS(fNam, "inner_material", inner_material);
  G4cout << "  " << fNam << ", inner_material: " << inner_material << G4endl;
  G4Material *inner_mat = G4NistManager::Instance()->FindOrBuildMaterial(inner_material);
  G4LogicalVolume *core_vol = new G4LogicalVolume(core_shape, inner_mat, core_nam);
  core_vol->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //magnetic field
  G4double dipole_field = geo->GetD(fNam, "field")*tesla; // magnet field
  G4UniformMagField *field = new G4UniformMagField(G4ThreeVector(dipole_field, 0, 0));
  G4FieldManager *fman = new G4FieldManager();
  fman->SetDetectorField(field);
  fman->CreateChordFinder(field);

  //set the field for inner core
  core_vol->SetFieldManager(fman, true);

  //put the inner core to the main volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0), core_vol, core_nam, main_vol, false, 0);

  //outer solid vessel
  G4Tubs *vessel_shape = new G4Tubs(fNam, inner_r, outer_r, dz/2., 0., 360.*deg);
  G4Material *vessel_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Fe");
  G4LogicalVolume *vessel_vol = new G4LogicalVolume(vessel_shape, vessel_mat, fNam);

  //vessel visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 1, 0, 0.7); // green
  vis->SetForceSolid(true);
  vessel_vol->SetVisAttributes(vis);

  //vessel in main volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0), vessel_vol, fNam, main_vol, false, 0);

  //stop and remove tracks incident on magnet vessel if set to true
  geo->GetOptB(fNam, "remove_tracks", fRemoveTracks);
  G4cout << "  " << fNam << ", remove_tracks: " << fRemoveTracks << G4endl;

  //main volume in top
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), main_vol, main_nam, top, false, 0);

}//Magnet

//_____________________________________________________________________________
G4bool Magnet::ProcessHits(G4Step *step, G4TouchableHistory*) {

  if(fRemoveTracks) {
    //remove the track entering the cone aperture vessel
    G4Track *track = step->GetTrack();
    track->SetTrackStatus(fKillTrackAndSecondaries);
  }

  return true;

}//ProcessHits























