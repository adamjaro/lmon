
//_____________________________________________________________________________
//
// PMT photocathode on the back of a glass layer
//
//_____________________________________________________________________________

//C++

//ROOT

//Geant
#include "G4NistManager.hh"
#include "G4Tubs.hh"
#include "G4SystemOfUnits.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"
#include "G4MaterialPropertiesTable.hh"
#include "G4OpticalSurface.hh"
#include "G4LogicalSkinSurface.hh"
#include "G4LogicalBorderSurface.hh"
#include "G4VProcess.hh"

//local classes
#include "PhotoCathPMT.h"
#include "GeoParser.h"
#include "ColorDecoder.h"

//_____________________________________________________________________________
PhotoCathPMT::PhotoCathPMT(const G4String& nam, GeoParser *, G4LogicalVolume *top) : Detector(),
  G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "PhotoCathPMT: " << fNam << G4endl;

  //the photocathode is a part of another detector when top is not defined
  if(!top) return;

}//PhotoCathPMT

//_____________________________________________________________________________
G4LogicalVolume* PhotoCathPMT::CreateGeometry(G4double radius, G4double dz, G4VisAttributes *vmain, G4VisAttributes *vcath) {

  //main volume for the glass plate and photocathode layer
  G4Tubs *main_shape = new G4Tubs(fNam+"_main", 0, radius, dz/2., 0, CLHEP::twopi);
  G4Material *main_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_AIR"); // default material
  G4LogicalVolume *main_vol = new G4LogicalVolume(main_shape, main_mat, main_shape->GetName()); //main logical volume
  main_vol->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //photocathode layer as sensitive volume for photon counts
  G4double cath_thickness = 2.*mm; // 0.01 mm
  G4Tubs *cath_shape = new G4Tubs(fNam, 0, radius, cath_thickness/2., 0, CLHEP::twopi);
  G4Material *cath_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Ag");
  G4LogicalVolume *cath_vol = new G4LogicalVolume(cath_shape, cath_mat, fNam);

  //photocathode visibility
  cath_vol->SetVisAttributes( vcath );

  //photocathode layer in the main PMT volume at the back side (lower z)
  G4VPhysicalVolume *cath_phys = new G4PVPlacement(0, G4ThreeVector(0, 0, -0.5*dz+0.5*cath_thickness), cath_vol, fNam, main_vol, false, 0);

  //glass plate
  G4double glass_thickness = dz-cath_thickness;
  G4Tubs *glass_shape = new G4Tubs(fNam+"_glass", 0, radius, glass_thickness/2., 0, CLHEP::twopi);
  G4Material *glass_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_GLASS_PLATE");
  G4LogicalVolume *glass_vol = new G4LogicalVolume(glass_shape, glass_mat, glass_shape->GetName());

  //glass plate visibility
  glass_vol->SetVisAttributes( vmain );

  //optics for the glass
  SetOptics(glass_mat, glass_vol);

  //glass plate in the main PMT volume at the front side (higher z)
  fGlassPhysVol = new G4PVPlacement(0, G4ThreeVector(0, 0, 0.5*(dz-glass_thickness)), glass_vol, glass_shape->GetName(), main_vol, false, 0);

  //optical boundary from the glass to the photocathode
  SetBoundary(cath_phys);

  return main_vol;

}//CreateGeometry

//_____________________________________________________________________________
void PhotoCathPMT::SetOptics(G4Material *mat, G4LogicalVolume *glass_vol) {

  //optical properties for the glass

  const G4int ntab = 2;
  G4double opt_en[] = {1.551*eV, 3.545*eV}; // 350 - 800 nm
  G4double opt_r[] = {2.4, 2.4};
  G4double reflectivity[] = {0.8, 0.8};
  G4double efficiency[] = {0.9, 0.9};

  //glass material
  G4MaterialPropertiesTable *tab = new G4MaterialPropertiesTable();
  tab->AddProperty("RINDEX", opt_en, opt_r, ntab);
  mat->SetMaterialPropertiesTable(tab);

  //glass surface
  G4MaterialPropertiesTable *surfmat = new G4MaterialPropertiesTable();
  surfmat->AddProperty("REFLECTIVITY", opt_en, reflectivity, ntab);
  surfmat->AddProperty("EFFICIENCY", opt_en, efficiency, ntab);

  G4OpticalSurface *surface = new G4OpticalSurface("GlassSurface", unified, polished, dielectric_metal);
  surface->SetMaterialPropertiesTable(surfmat);
  new G4LogicalSkinSurface("GlassSurfaceL", glass_vol, surface);

  //photocathode surface
  //new G4LogicalSkinSurface("CathSurfaceL", cath_vol, surface);

}//SetOptics

//_____________________________________________________________________________
void PhotoCathPMT::SetBoundary(G4VPhysicalVolume *cath_phys) {

  //optical boundary from the glass to the photocathode

  G4OpticalSurface *surf = new G4OpticalSurface("GlassCathS");
  //surf->SetType(dielectric_dielectric); // photons go to the detector, must have rindex defined
  surf->SetType(dielectric_metal); // photon is absorbed when reaching the detector, no material rindex required
  surf->SetFinish(ground);
  //surf->SetFinish(polished);
  surf->SetModel(unified);
  //surf->SetModel(glisur);

  new G4LogicalBorderSurface("GlassCathB", fGlassPhysVol, cath_phys, surf);

  const G4int ntab = 2;
  //G4double opt_en[] = {1.551*eV, 3.545*eV}; // 350 - 800 nm
  G4double opt_en[] = {1.*eV, 4.*eV};
  //G4double reflectivity[] = {0., 0.};
  G4double reflectivity[] = {0.1, 0.1};
  //G4double reflectivity[] = {0.9, 0.9};
  //G4double reflectivity[] = {1., 1.};
  G4double efficiency[] = {1., 1.};
  //G4double efficiency[] = {0., 0.};

  G4MaterialPropertiesTable *surfmat = new G4MaterialPropertiesTable();
  surfmat->AddProperty("REFLECTIVITY", opt_en, reflectivity, ntab);
  surfmat->AddProperty("EFFICIENCY", opt_en, efficiency, ntab);
  surf->SetMaterialPropertiesTable(surfmat);

}//SetBoundary

//_____________________________________________________________________________
G4bool PhotoCathPMT::ProcessHits(G4Step *step, G4TouchableHistory*) {

  G4String procname = step->GetPostStepPoint()->GetProcessDefinedStep()->GetProcessName();

  G4cout << "PhotoCathPMT::ProcessHits " << procname << G4endl;

  return true;

}//ProcessHits




















