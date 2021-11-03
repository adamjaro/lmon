
//_____________________________________________________________________________
//
// Vacuum between B2 magnet and luminosity exit window
//
//_____________________________________________________________________________

//ROOT
#include "TMath.h"

//Geant
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4GenericTrap.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4PVPlacement.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"
#include "G4ThreeVector.hh"

//local classes
#include "VacB2lumiWin.h"
#include "GeoParser.h"

using namespace std;

//_____________________________________________________________________________
VacB2lumiWin::VacB2lumiWin(const G4String& nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), fNam(nam) {

  G4cout << "VacB2lumiWin: " << fNam << G4endl;

  //given by beam pipe to tagger
  G4double win_xmin = geo->GetD(fNam, "win_xmin")*mm;

  //full size in y at the front of exit window volume
  G4double win_ysiz = geo->GetD(fNam, "ysiz")*mm;

  G4double win_z = -18500*mm; // z of front of exit window volume
  G4double win_xmax = 100*mm; // given by angular apperture to exit window

  //end of B2BeR magnet
  //full size in x and y at the end of B2eR, equal to inner diameter
  G4double b2b_end_xy = geo->GetD(fNam, "b2b_end_xy")*mm; 
  G4double b2b_end_z = -14865*mm; // z position of B2BeR end

  //derived quantities
  G4double zsiz = TMath::Abs(win_z - b2b_end_z); //vacuum element full size in z
  G4double zpos = (win_z + b2b_end_z)/2; // z position of the vacuum element

  //vertices for the trapezoid
  vector<G4TwoVector> ver(8);

  ver[0].set(win_xmin, -win_ysiz/2);

  ver[1].set(win_xmin, win_ysiz/2);

  ver[2].set(win_xmax, win_ysiz/2);

  ver[3].set(win_xmax, -win_ysiz/2);

  //plane at the end of B2BeR
  ver[4].set(-b2b_end_xy/2, -win_ysiz/2);

  ver[5].set(-b2b_end_xy/2, win_ysiz/2);

  ver[6].set(b2b_end_xy/2, win_ysiz/2);

  ver[7].set(b2b_end_xy/2, -win_ysiz/2);

  G4GenericTrap *shape = new G4GenericTrap(fNam, zsiz/2, ver);

  //logical volume
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0, 0, 1);
  //vis->SetForceSolid(true);
  vis->SetForceWireframe();
  vol->SetVisAttributes(vis);

  //placement in top
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos), vol, fNam, top, false, 0);

}//VacB2lumiWin

















