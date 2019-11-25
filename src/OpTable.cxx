
//_____________________________________________________________________________
//
// optical and scintillation properties of PbWO4 crystals,
// also provides boundary from crystal to optical photon detector
//_____________________________________________________________________________

//Geant headers
#include "G4MaterialPropertiesTable.hh"
#include "G4Material.hh"
#include "G4SystemOfUnits.hh"
#include "G4LogicalVolume.hh"
#include "G4OpticalSurface.hh"
#include "G4LogicalSkinSurface.hh"
#include "G4LogicalBorderSurface.hh"

//local headers
#include "OpTable.h"

//_____________________________________________________________________________
void OpTable::CrystalTable(G4Material *mat) {

  //scintillation and optical properties

  //already done
  if(mat->GetMaterialPropertiesTable()) return;

  //G4cout << "OpTable::CrystalTable, " << mat->GetMaterialPropertiesTable() << G4endl;

  const G4int ntab = 2;
  G4double scin_en[] = {2.9*eV, 3.*eV}; // 420 nm (the range is 414 - 428 nm)
  G4double scin_fast[] = {1., 1.};

  G4MaterialPropertiesTable *tab = new G4MaterialPropertiesTable();

  tab->AddProperty("FASTCOMPONENT", scin_en, scin_fast, ntab);
  tab->AddConstProperty("FASTTIMECONSTANT", 6*ns);
  tab->AddConstProperty("SCINTILLATIONYIELD", 200/MeV); // 200/MEV nominal  10
  tab->AddConstProperty("RESOLUTIONSCALE", 1.);

  G4double opt_en[] = {1.551*eV, 3.545*eV}; // 350 - 800 nm
  G4double opt_r[] = {2.4, 2.4};
  G4double opt_abs[] = {200*cm, 200*cm};

  tab->AddProperty("RINDEX", opt_en, opt_r, ntab);
  tab->AddProperty("ABSLENGTH", opt_en, opt_abs, ntab);

  mat->SetMaterialPropertiesTable(tab);

}//CrystalTable

//_____________________________________________________________________________
void OpTable::SurfaceTable(G4LogicalVolume *vol) {

  //crystal optical surface

  G4OpticalSurface *surface = new G4OpticalSurface("CrystalSurface", unified, polished, dielectric_metal);
  //G4LogicalSkinSurface *csurf = 
  new G4LogicalSkinSurface("CrystalSurfaceL", vol, surface);

  //surface material
  const G4int ntab = 2;
  G4double opt_en[] = {1.551*eV, 3.545*eV}; // 350 - 800 nm
  G4double reflectivity[] = {0.8, 0.8};
  G4double efficiency[] = {0.9, 0.9};
  G4MaterialPropertiesTable *surfmat = new G4MaterialPropertiesTable();
  surfmat->AddProperty("REFLECTIVITY", opt_en, reflectivity, ntab);
  surfmat->AddProperty("EFFICIENCY", opt_en, efficiency, ntab);
  surface->SetMaterialPropertiesTable(surfmat);
  //csurf->DumpInfo();

}//SurfaceTable

//_____________________________________________________________________________
void OpTable::MakeBoundary(G4VPhysicalVolume *crystal, G4VPhysicalVolume *opdet) {

  //optical boundary between the crystal and optical photons detector

  G4OpticalSurface *surf = new G4OpticalSurface("OpDetS");
  //surf->SetType(dielectric_dielectric); // photons go to the detector, must have rindex defined
  surf->SetType(dielectric_metal); // photon is absorbed when reaching the detector, no material rindex required
  //surf->SetFinish(ground);
  surf->SetFinish(polished);
  //surf->SetModel(unified);
  surf->SetModel(glisur);

  new G4LogicalBorderSurface("OpDetB", crystal, opdet, surf);

  const G4int ntab = 2;
  G4double opt_en[] = {1.551*eV, 3.545*eV}; // 350 - 800 nm
  //G4double reflectivity[] = {0., 0.};
  G4double reflectivity[] = {0.1, 0.1};
  //G4double reflectivity[] = {0.9, 0.9};
  //G4double reflectivity[] = {1., 1.};
  G4double efficiency[] = {1., 1.};

  G4MaterialPropertiesTable *surfmat = new G4MaterialPropertiesTable();
  surfmat->AddProperty("REFLECTIVITY", opt_en, reflectivity, ntab);
  surfmat->AddProperty("EFFICIENCY", opt_en, efficiency, ntab);
  surf->SetMaterialPropertiesTable(surfmat);



}//MakeBoundary






















