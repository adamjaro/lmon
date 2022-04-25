
//_____________________________________________________________________________
//
// MAPS tracking layer, basic implementation
//
//_____________________________________________________________________________

//C++
#include <map>
#include <vector>
#include <string>

//ROOT
#include "TTree.h"

//Geant
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4Step.hh"
#include "G4VisAttributes.hh"
#include "G4PVReplica.hh"

//local headers
#include "TrkMapsBasic.h"
#include "GeoParser.h"
#include "ColorDecoder.h"

using namespace std;

//_____________________________________________________________________________
TrkMapsBasic::TrkMapsBasic(const G4String& nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "TrkMapsBasic: " << fNam << G4endl;

  G4double dz = geo->GetD(fNam, "dz")*mm; // full layer thickness along z, mm
  G4double dxy = geo->GetD(fNam, "dxy")*mm; // full pixel size in x and y, mm
  G4int nx = geo->GetI(fNam, "nx"); // number of pixels along x
  G4int ny = geo->GetI(fNam, "ny"); // number of pixels along y

  //G4cout << nx << " " << ny << " " << geo->GetS(fNam, "nx") << G4endl;

  //tracker layer
  G4double layx = nx*dxy;
  G4double layy = ny*dxy;
  G4cout << "  " << nam << ", layx, layy (mm): " << layx << ", " << layy << G4endl;
  G4Box *lays = new G4Box(nam+"_lay", layx/2., layy/2., dz/2.);

  //layer volume
  G4Material *laym = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *layv = new G4LogicalVolume(lays, laym, lays->GetName());

  //layer visibility
  ColorDecoder lay_vis("1:0:0:0.3");
  layv->SetVisAttributes(lay_vis.MakeVis(geo, fNam, "lay_vis"));

  //mother volume for the layer
  G4LogicalVolume *mother_vol = top;
  G4String mother_nam;
  if( geo->GetOptS(fNam, "place_into", mother_nam) ) {
    mother_vol = GetMotherVolume(mother_nam, top);
  }

  //center position for the layer in x, y and z, mm
  G4double xpos=0, ypos=0, zpos=0;
  geo->GetOptD(fNam, "xpos", xpos, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "ypos", ypos, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "zpos", zpos, GeoParser::Unit(mm));
  G4ThreeVector lay_pos(xpos, ypos, zpos);

  //layer rotation along y, rad
  G4double rotate_y = 0; // rotation along y axis
  geo->GetOptD(fNam, "rotate_y", rotate_y, GeoParser::Unit(rad));
  G4RotationMatrix lay_rot(G4ThreeVector(0, 1, 0), rotate_y); //CLHEP::HepRotation

  //layer in its mother volume
  G4Transform3D lay_transform(lay_rot, lay_pos); //HepGeom::Transform3D
  new G4PVPlacement(lay_transform, layv, lays->GetName(), mother_vol, false, 0);

  //row holding individual pixels
  G4Box *row_shape = new G4Box(nam+"_row", layx/2., dxy/2., dz/2.);
  G4LogicalVolume *row_vol = new G4LogicalVolume(row_shape, laym, row_shape->GetName());
  row_vol->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //rows in tracker layer
  new G4PVReplica(row_shape->GetName(), row_vol, layv, kYAxis, ny, dxy);

  //sensitive pixels in each row
  G4Box *pix_shape = new G4Box(nam, dxy/2., dxy/2., dz/2.);

  //silicon material for pixels
  G4Material *pix_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Si");

  //pixel volume
  G4LogicalVolume *pix_vol = new G4LogicalVolume(pix_shape, pix_mat, nam);
  ColorDecoder pix_vis("1:0:0:3");
  pix_vol->SetVisAttributes(pix_vis.MakeVis(geo, fNam, "pix_vis"));

  //pixels in row
  new G4PVReplica(nam, pix_vol, row_vol, kXAxis, nx, dxy);

}//TrkMapsBasic

//_____________________________________________________________________________
G4bool TrkMapsBasic::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //signal in hits
  fHits.AddSignal(step);

  return true;

}//ProcessHits

//_____________________________________________________________________________
void TrkMapsBasic::CreateOutput(TTree *tree) {

  fHits.CreateOutput(fNam, tree);

}//CreateOutput

//_____________________________________________________________________________
void TrkMapsBasic::ClearEvent() {

  fHits.ClearEvent();

}//ClearEvent

//_____________________________________________________________________________
void TrkMapsBasic::FinishEvent() {

  fHits.FinishEvent();

}//FinishEvent

//_____________________________________________________________________________
G4LogicalVolume* TrkMapsBasic::GetMotherVolume(G4String mother_nam, G4LogicalVolume *top) {

  for(size_t i=0; i<top->GetNoDaughters(); i++) {

    G4LogicalVolume *dv = top->GetDaughter(i)->GetLogicalVolume();

    if( dv->GetName() == mother_nam ) {
      return dv;
    }
  }

  return 0x0;

}//GetMotherVolume
































