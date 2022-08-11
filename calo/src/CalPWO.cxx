

//_____________________________________________________________________________
//
// PbWO4 calorimeter, module consists of individual crystal cells
//
//_____________________________________________________________________________

//C++

//ROOT

//Geant
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4SubtractionSolid.hh"

//local classes
#include "CalPWO.h"
#include "GeoParser.h"
#include "ColorDecoder.h"

//_____________________________________________________________________________
CalPWO::CalPWO(const G4String& nam, GeoParser *geo, G4LogicalVolume *top) : Detector(),
  G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "CalPWO: " << fNam << G4endl;

  //module size, must accommodate for wrapping, crystal, photon detector and number of cells, explained below
  G4double modx = geo->GetD(fNam, "modx")*mm; // full size in x, mm
  G4double mody = geo->GetD(fNam, "mody")*mm; // full size in y, mm
  G4double modz = geo->GetD(fNam, "modz")*mm; // full size in z, mm

  //module volume
  G4Box *mod_shape = new G4Box(fNam+"_mod", modx/2., mody/2., modz/2.);
  G4Material *mod_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Air"); // default module material
  G4LogicalVolume *mod_vol = new G4LogicalVolume(mod_shape, mod_mat, mod_shape->GetName());

  //module visibility
  ColorDecoder mod_vis("0:0:1:2");
  mod_vol->SetVisAttributes(mod_vis.MakeVis(geo, fNam, "mod_vis"));

  //module center position
  G4double mod_xpos=0., mod_ypos=0., mod_zpos=0.;
  geo->GetOptD(fNam, "xpos", mod_xpos, GeoParser::Unit(mm)); // center position in x, mm
  geo->GetOptD(fNam, "ypos", mod_ypos, GeoParser::Unit(mm)); // center position in y, mm
  geo->GetOptD(fNam, "zpos", mod_zpos, GeoParser::Unit(mm)); // center position in z, mm

  //module in its mother volume
  new G4PVPlacement(0, G4ThreeVector(mod_xpos, mod_ypos, mod_zpos), mod_vol, mod_vol->GetName(), top, false, 0);

  //crystal size
  G4double crystal_xy = geo->GetD(fNam, "crystal_xy")*mm; // crystal full size in x and y, mm
  G4double crystal_z = geo->GetD(fNam, "crystal_z")*mm; // crystal full length in z, mm

  //wrapping thickness
  G4double wrapping_thickness = geo->GetD(fNam, "wrapping_thickness")*mm; // wrapping thickness, mm

  //photon detector thickness in z
  //G4double phot_z = geo->GetD(fNam, "phot_z")*mm; // photon detector thickness in z, mm

  //cell holding the wrapped crystal and photon detector
  G4double cell_xy = crystal_xy + 2.*wrapping_thickness; // factor of 2 for wrapping on all sides

  //cell volume, modz = wrapping_thickness + crystal_z + phot_z must hold
  G4Box *cell_shape = new G4Box(fNam+"_cell", cell_xy/2., cell_xy/2., modz/2.);
  G4LogicalVolume *cell_vol = new G4LogicalVolume(cell_shape, mod_mat, cell_shape->GetName()); // default volume material
  cell_vol->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //number of cells in module along x and y
  G4int nx = geo->GetI(fNam, "nx"); // num cells in x
  G4int ny = geo->GetI(fNam, "ny"); // num cells in y

  //cells in module, modx = nx*cell_xy must hold and the same for y
  G4int cell_cnt = 0; // cell count in module
  for(G4int ix=0; ix<nx; ix++) {
    for(G4int iy=0; iy<ny; iy++) {

      //cell position in x and y
      G4double cell_posx = -modx/2. + cell_xy/2. + ix*cell_xy;
      G4double cell_posy = -mody/2. + cell_xy/2. + iy*cell_xy;

      //put the cell in the module
      new G4PVPlacement(0, G4ThreeVector(cell_posx, cell_posy, 0), cell_vol, cell_vol->GetName(), mod_vol, false, cell_cnt++);
    }//iy
  }//ix

  //crystal volume, sensitive volume for energy deposition in the crystal
  G4Box *crystal_shape = new G4Box(fNam, crystal_xy/2., crystal_xy/2., crystal_z/2.);
  G4Material *crystal_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_PbWO4");
  G4LogicalVolume *crystal_vol = new G4LogicalVolume(crystal_shape, crystal_mat, fNam);

  //crystal visibility
  ColorDecoder crystal_vis("1:0:0:2");
  crystal_vol->SetVisAttributes(crystal_vis.MakeVis(geo, fNam, "crystal_vis"));

  //crystal in cell, at the front z of the cell with space for wrapping
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0.5*(modz-crystal_z)-wrapping_thickness), crystal_vol, fNam, cell_vol, false, 0);

  //wrapping volume, along the sides and the front (larger z) of the crystal
  G4Box *wrapping_outer = new G4Box(fNam+"_wrapping_outer", cell_xy/2., cell_xy/2., (crystal_z+wrapping_thickness)/2.);
  G4SubtractionSolid *wrapping_shape
    = new G4SubtractionSolid(fNam+"_wrapping", wrapping_outer, crystal_shape, 0, G4ThreeVector(0, 0, -wrapping_thickness/2.));

  //wrapping material and logical volume
  G4Material *wrapping_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_TEFLON");
  G4LogicalVolume *wrapping_vol = new G4LogicalVolume(wrapping_shape, wrapping_mat, wrapping_shape->GetName());

  //wrapping visibility
  ColorDecoder wrapping_vis("0:1:0:2");
  wrapping_vol->SetVisAttributes(wrapping_vis.MakeVis(geo, fNam, "wrapping_vis"));

  //wrapping volume in the cell, directly at the front (larger z) of the cell
  new G4PVPlacement(0, G4ThreeVector(0, 0, 0.5*(modz-crystal_z-wrapping_thickness)), wrapping_vol, fNam, cell_vol, false, 0);

}//CalPWO


































