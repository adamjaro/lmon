
//_____________________________________________________________________________
//
// Central electron beampipe
//
//_____________________________________________________________________________

//Geant
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Tubs.hh"
#include "G4Cons.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4PVPlacement.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"
#include "G4ThreeVector.hh"

//local classes
#include "CenBeampipeEl.h"
#include "GeoParser.h"

using namespace std;

//_____________________________________________________________________________
CenBeampipeEl::CenBeampipeEl(const G4String& nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), fNam(nam) {

  G4cout << "CenBeampipeEl: " << fNam << G4endl;

  Central(geo, top);
  NegativeZ(geo, top);
  PositiveZ(geo, top);
  LargePosZ(geo, top);

}//CenBeampipeEl

//_____________________________________________________________________________
void CenBeampipeEl::Central(GeoParser *geo, G4LogicalVolume *top) {

  //central cylindrical section

  G4double zmin = -800.*mm;
  G4double zmax = 670.*mm;
  G4double diameter = 63.5254*mm;

  G4double wall_thickness = 0.757*mm;

  G4double length = zmax - zmin;
  G4double zpos = (zmax+zmin)/2;

  G4String nam_outer = fNam+"_cen_outer";
  G4Tubs *shape_outer = new G4Tubs(nam_outer, 0., diameter/2, length/2, 0., 360.*deg);
  G4Material *vac = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol_outer = new G4LogicalVolume(shape_outer, vac, nam_outer);
  vol_outer->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //Berylium wall
  G4String nam_wall = fNam+"_cen_wall";
  G4Tubs *shape_wall = new G4Tubs(nam_wall, (diameter/2)-wall_thickness, diameter/2, length/2, 0., 360.*deg);
  G4Material *mat_wall = G4NistManager::Instance()->FindOrBuildMaterial("G4_Be");
  G4LogicalVolume *vol_wall = new G4LogicalVolume(shape_wall, mat_wall, nam_wall);
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0), vol_wall, nam_wall, vol_outer, false, 0);

  G4VisAttributes *vis_wall = new G4VisAttributes();
  vis_wall->SetColor(0.5, 0.5, 0.5); // gray
  vis_wall->SetForceSolid(true);
  vol_wall->SetVisAttributes(vis_wall);

  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol_outer, nam_outer, top, false, 0);

}//Central

//_____________________________________________________________________________
void CenBeampipeEl::NegativeZ(GeoParser *geo, G4LogicalVolume *top) {

  //conical section at negative z

  G4double zmin = -4560.17*mm;
  G4double zmax = -800.*mm;
  G4double d_zmin = 99.2*mm; // diameter at zmin
  G4double d_zmax = 63.5254*mm; // at zmax

  G4double wall_thickness = 2.*mm;

  G4double length = zmax - zmin;
  G4double zpos = (zmax+zmin)/2;

  G4String nam_outer = fNam+"_neg_outer";

  G4Cons *shape_outer = new G4Cons(nam_outer, 0, d_zmin/2, 0, d_zmax/2, length/2, 0, 360*deg);
  G4Material *vac = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol_outer = new G4LogicalVolume(shape_outer, vac, nam_outer);
  vol_outer->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //Wall
  G4String nam_wall = fNam+"_neg_wall";
  G4Cons *shape_wall = new G4Cons(nam_wall, (d_zmin/2)-wall_thickness, d_zmin/2, (d_zmax/2)-wall_thickness, d_zmax/2, length/2, 0, 360*deg);
  G4Material *mat_wall = G4NistManager::Instance()->FindOrBuildMaterial("G4_Be");
  G4LogicalVolume *vol_wall = new G4LogicalVolume(shape_wall, mat_wall, nam_wall);
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0), vol_wall, nam_wall, vol_outer, false, 0);

  G4VisAttributes *vis_wall = new G4VisAttributes();
  vis_wall->SetColor(0.5, 0.5, 0.5); // gray
  vis_wall->SetForceSolid(true);
  vol_wall->SetVisAttributes(vis_wall);

  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol_outer, nam_outer, top, false, 0);

}//NegativeZ

//_____________________________________________________________________________
void CenBeampipeEl::PositiveZ(GeoParser *geo, G4LogicalVolume *top) {

  //conical section at positive z

  G4double zmin = 670.*mm;
  G4double zmax = 4484.25*mm;
  G4double d_zmin = 63.5254*mm; // diameter at zmin
  G4double d_zmax = 63.5254*mm; // at zmax

  G4double wall_thickness = 2.*mm;

  G4double length = zmax - zmin;
  G4double zpos = (zmax+zmin)/2;

  G4String nam_outer = fNam+"_pos_outer";

  G4Cons *shape_outer = new G4Cons(nam_outer, 0, d_zmin/2, 0, d_zmax/2, length/2, 0, 360*deg);

  G4Material *vac = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol_outer = new G4LogicalVolume(shape_outer, vac, nam_outer);
  vol_outer->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //Wall
  G4String nam_wall = fNam+"_pos_wall";
  G4Cons *shape_wall = new G4Cons(nam_wall, (d_zmin/2)-wall_thickness, d_zmin/2, (d_zmax/2)-wall_thickness, d_zmax/2, length/2, 0, 360*deg);
  G4Material *mat_wall = G4NistManager::Instance()->FindOrBuildMaterial("G4_Be");
  G4LogicalVolume *vol_wall = new G4LogicalVolume(shape_wall, mat_wall, nam_wall);
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0), vol_wall, nam_wall, vol_outer, false, 0);

  G4VisAttributes *vis_wall = new G4VisAttributes();
  vis_wall->SetColor(0.5, 0.5, 0.5); // gray
  vis_wall->SetForceSolid(true);
  vol_wall->SetVisAttributes(vis_wall);

  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol_outer, nam_outer, top, false, 0);

}//PositiveZ

//_____________________________________________________________________________
void CenBeampipeEl::LargePosZ(GeoParser *geo, G4LogicalVolume *top) {

  //conical extension to large positive z

  G4double zmin = 4484.25*mm;
  G4double zmax = 15000.*mm;
  G4double d_zmin = 63.5254*mm; // diameter at zmin
  G4double d_zmax = 63.5254*mm; // at zmax

  G4double wall_thickness = 2.*mm;

  G4double length = zmax - zmin;
  G4double zpos = (zmax+zmin)/2;

  G4String nam_outer = fNam+"_large_pos_outer";

  G4Cons *shape_outer = new G4Cons(nam_outer, 0, d_zmin/2, 0, d_zmax/2, length/2, 0, 360*deg);

  G4Material *vac = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol_outer = new G4LogicalVolume(shape_outer, vac, nam_outer);
  vol_outer->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //Wall
  G4String nam_wall = fNam+"_large_pos_wall";
  G4Cons *shape_wall = new G4Cons(nam_wall, (d_zmin/2)-wall_thickness, d_zmin/2, (d_zmax/2)-wall_thickness, d_zmax/2, length/2, 0, 360*deg);
  G4Material *mat_wall = G4NistManager::Instance()->FindOrBuildMaterial("G4_Be");
  G4LogicalVolume *vol_wall = new G4LogicalVolume(shape_wall, mat_wall, nam_wall);
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0), vol_wall, nam_wall, vol_outer, false, 0);

  G4VisAttributes *vis_wall = new G4VisAttributes();
  vis_wall->SetColor(0.5, 0.5, 0.5); // gray
  vis_wall->SetForceSolid(true);
  vol_wall->SetVisAttributes(vis_wall);

  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol_outer, nam_outer, top, false, 0);

}//LargePosZ






















