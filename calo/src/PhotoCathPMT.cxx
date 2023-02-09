
//_____________________________________________________________________________
//
// PMT photocathode on the back of a glass layer
//
//_____________________________________________________________________________

//C++
#include <vector>

//ROOT
#include "TTree.h"

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
#include "G4OpticalPhoton.hh"

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
  G4double cath_thickness = 0.01*mm; // 0.01 mm
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

  //optics for the glass and photocathode
  SetOptics(glass_mat, glass_vol, cath_mat, cath_vol);

  //glass plate in the main PMT volume at the front side (higher z)
  fGlassPhysVol = new G4PVPlacement(0, G4ThreeVector(0, 0, 0.5*(dz-glass_thickness)), glass_vol, glass_shape->GetName(), main_vol, false, 0);

  //optical boundary from the glass to the photocathode
  SetBoundary(cath_phys);

  return main_vol;

}//CreateGeometry

//_____________________________________________________________________________
void PhotoCathPMT::SetOptics(G4Material *mat, G4LogicalVolume *glass_vol, G4Material *cath_mat, G4LogicalVolume *cath_vol) {

  //optical properties for the glass and photocathode

  std::vector<G4double> opt_lam = {350, 800}; // nm
  std::vector<G4double> opt_r = {1.52, 1.52};
  std::vector<G4double> reflectivity = {0.9, 0.9};
  std::vector<G4double> efficiency = {1., 1.};

  //glass material
  G4MaterialPropertiesTable *tab = new G4MaterialPropertiesTable();
  tab->AddProperty("RINDEX", LambdaNMtoEV(opt_lam), opt_r);
  mat->SetMaterialPropertiesTable(tab);

  //glass surface
  G4MaterialPropertiesTable *surfmat = new G4MaterialPropertiesTable();
  surfmat->AddProperty("REFLECTIVITY", LambdaNMtoEV(opt_lam), reflectivity);
  surfmat->AddProperty("EFFICIENCY", LambdaNMtoEV(opt_lam), efficiency);

  G4OpticalSurface *surface = new G4OpticalSurface("GlassSurface", unified, polished, dielectric_metal);
  surface->SetMaterialPropertiesTable(surfmat);
  new G4LogicalSkinSurface("GlassSurfaceL", glass_vol, surface);

  //photocathode material
  std::vector<G4double> cath_abs = {1e-20*m, 1e-20*m};
  G4MaterialPropertiesTable *cath_tab = new G4MaterialPropertiesTable();
  cath_tab->AddProperty("RINDEX", LambdaNMtoEV(opt_lam), opt_r);
  cath_tab->AddProperty("ABSLENGTH", LambdaNMtoEV(opt_lam), cath_abs);
  cath_mat->SetMaterialPropertiesTable(cath_tab);

  //photocathode surface
  std::vector<G4double> cath_eff = {1., 1.};
  std::vector<G4double> cath_ReR = {1.92, 1.92};
  std::vector<G4double> cath_ImR = {1.69, 1.69};
  G4MaterialPropertiesTable *cathmat = new G4MaterialPropertiesTable();
  cathmat->AddProperty("EFFICIENCY", LambdaNMtoEV(opt_lam), cath_eff);
  cathmat->AddProperty("REALRINDEX", LambdaNMtoEV(opt_lam), cath_ReR);
  cathmat->AddProperty("IMAGINARYRINDEX", LambdaNMtoEV(opt_lam), cath_ImR);

  G4OpticalSurface *cath_surf = new G4OpticalSurface("CathSurface", glisur, polished, dielectric_metal);
  cath_surf->SetMaterialPropertiesTable(cathmat);

  new G4LogicalSkinSurface("CathSurfaceL", cath_vol, cath_surf);

}//SetOptics

//_____________________________________________________________________________
void PhotoCathPMT::SetBoundary(G4VPhysicalVolume *cath_phys) {

  //optical boundary from the glass to the photocathode

  G4OpticalSurface *surf = new G4OpticalSurface("GlassCathS");
  surf->SetType(dielectric_dielectric); // photons go to the detector, must have rindex defined
  surf->SetFinish(polished);
  surf->SetModel(unified);
  //surf->SetModel(glisur);

  new G4LogicalBorderSurface("GlassCathB", fGlassPhysVol, cath_phys, surf);

  std::vector<G4double> opt_lam = {350, 800}; // nm
  std::vector<G4double> reflectivity = {0.9, 0.9};
  std::vector<G4double> efficiency = {1., 1.};

  G4MaterialPropertiesTable *surfmat = new G4MaterialPropertiesTable();
  surfmat->AddProperty("REFLECTIVITY", LambdaNMtoEV(opt_lam), reflectivity);
  surfmat->AddProperty("EFFICIENCY", LambdaNMtoEV(opt_lam), efficiency);
  surf->SetMaterialPropertiesTable(surfmat);

}//SetBoundary

//_____________________________________________________________________________
std::vector<G4double> PhotoCathPMT::LambdaNMtoEV(const std::vector<G4double>& lambda) {

  //converting wavelength (lambda) in nm to energy (en) in eV
  /*

    E = h nu,  nu = c/lambda

    E = h c / lambda

        h = 6.625 x 10^-34 J s
        c = 3 x 10^8 m/s
        1 J = 1.602 x 10^-19 eV
        1 m = 10^9 nm

        h c = ((6.625 x 3)/ 1.602) x 10^-34 x 10^8 x 10^19 x 10^9 = 10^2 x ((6.625 x 3)/ 1.602) = 1240.637 eV nm 

    E (eV) = 1240.637 / lambda (nm)

  */

  //energy in eV
  std::vector<G4double> en;

  //wavelength (nm) loop
  for(auto i: lambda) {

    en.push_back( (1240.637/i)*eV );

  }//wavelength (nm) loop

  return en;

}//LambdaNMtoEV

//_____________________________________________________________________________
G4bool PhotoCathPMT::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //track in step
  G4Track *track = step->GetTrack();

  //optical photons only
  if( track->GetDefinition() != G4OpticalPhoton::OpticalPhotonDefinition() ) return false;

  //only absorbed photons
  if( track->GetTrackStatus() <= 0 ) return false;

  //point in current step
  G4StepPoint *point = step->GetPostStepPoint();

  //hit time, ns
  G4double time = point->GetGlobalTime()/ns;

  //hit position
  G4ThreeVector hpos = point->GetPosition();
  G4double hit_x = hpos.x()/mm;
  G4double hit_y = hpos.y()/mm;
  G4double hit_z = hpos.z()/mm;

/*
  //global pmt position
  const G4TouchableHandle& hnd = point->GetTouchableHandle();
  G4ThreeVector origin(0, 0, 0);
  G4ThreeVector gpos = hnd->GetHistory()->GetTopTransform().Inverse().TransformPoint(origin);
  G4double pmt_x = gpos.x()/mm;
  G4double pmt_y = gpos.y()/mm;
  G4double pmt_z = gpos.z()/mm;
*/

  //add the hit
  PhotoHits::Hit& hit = fHits.CreateHit();
  hit.pos_x = hit_x;
  hit.pos_y = hit_y;
  hit.pos_z = hit_z;
  hit.time = time;

  PhotoHitsV2::Hit& hit2 = fHitsV2.CreateHit();
  hit2.pos_x = hit_x;
  hit2.pos_y = hit_y;
  hit2.pos_z = hit_z;
  hit2.time = time;

  return true;

}//ProcessHits

//_____________________________________________________________________________
void PhotoCathPMT::CreateOutput(TTree *tree) {

  fHits.CreateOutput(fNam, tree);
  fHitsV2.CreateOutput(fNam, tree);

}//CreateOutput

//_____________________________________________________________________________
void PhotoCathPMT::ClearEvent() {

  fHits.ClearEvent();
  fHitsV2.ClearEvent();

}//ClearEvent

//_____________________________________________________________________________
void PhotoCathPMT::FinishEvent() {

  fHits.FinishEvent();
  fHitsV2.FinishEvent();

}//FinishEvent














