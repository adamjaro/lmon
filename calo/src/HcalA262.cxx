
//_____________________________________________________________________________
//
// Lead-scintillator calorimeter for ZEUS according to NIM A262 (1987) 229-242
//
//_____________________________________________________________________________

//C++

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

//local classes
#include "HcalA262.h"
#include "DetUtils.h"

//_____________________________________________________________________________
HcalA262::HcalA262(const G4String& nam, GeoParser*, G4LogicalVolume *top) : Detector(),
  G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  HcalA262: " << fNam << G4endl;

  G4double modxy = 660*mm; // module transverse size
  fNem = 16; // number of layers in EM section
  G4int nHAD = 81; // number of layers in HAD section for 5 lambda_I
  //G4double modxy = 20*mm; // module transverse size
  //G4int nEM = 1; // number of layers in EM section
  //G4int nHAD = 2; // number of layers in HAD section
  G4int nlay = fNem + nHAD;

  G4double abso_z = 10*mm; // absorber thickness along z
  G4double scin_z = 2.5*mm; // scintillator thickness along z
  G4double spacer_z = 3.5*mm; // spacer size along z
  G4double layer_z = abso_z + spacer_z; // total layer thickness along z

  //calorimeter top module
  G4double modz = nlay*layer_z; // module length along z
  G4String modnam = fNam+"_mod"; // module name

  //box shape for the module
  G4Box *mods = new G4Box(modnam, modxy/2, modxy/2, modz/2);

  //module default material
  G4Material *mod_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");

  //module logical volume
  G4LogicalVolume *modv = new G4LogicalVolume(mods, mod_mat, modnam);
  modv->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //module visibility
  G4VisAttributes *modvis = new G4VisAttributes();
  modvis->SetColor(0, 0, 1); // blue
  //modv->SetVisAttributes(modvis);

  //put the module to the top
  new G4PVPlacement(0, G4ThreeVector(0, 0, modz/2), modv, modnam, top, false, 0);

  //layer with absorber and scintillator plates
  G4String lay_nam = fNam+"_layer"; //layer name

  //layer shape
  G4Box *lay_shape = new G4Box(lay_nam, modxy/2, modxy/2, layer_z/2);

  //layer logical volume
  G4LogicalVolume *lay_vol = new G4LogicalVolume(lay_shape, mod_mat, lay_nam);
  lay_vol->SetVisAttributes(modvis);

  //put the layers to the module
  new G4PVReplica(lay_nam, lay_vol, modv, kZAxis, nlay, layer_z);

  //absorber plates
  G4String abso_nam = fNam+"_abso"; //absorber name

  //absorber plate
  G4Box *abso_shape = new G4Box(abso_nam, modxy/2, modxy/2, abso_z/2);

  //absorber material
  G4Material *abso_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_Pb");

  //absorber logical volume
  G4LogicalVolume *abso_vol = new G4LogicalVolume(abso_shape, abso_mat, abso_nam);

  //absorber visibility
  G4VisAttributes *abso_vis = new G4VisAttributes();
  abso_vis->SetColor(0, 1, 0, 0.5);
  abso_vis->SetForceSolid(true);
  abso_vol->SetVisAttributes(abso_vis);
  //abso_vol->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //put the absorber to the layer
  new G4PVPlacement(0, G4ThreeVector(0, 0, (abso_z - layer_z)/2.), abso_vol, abso_nam, lay_vol, false, 0);

  //scintillator plates
  G4Box *scin_shape = new G4Box(fNam, modxy/2, modxy/2, scin_z/2);

  //predefined scintillator material as a placeholder
  G4Material *scin_mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_PLASTIC_SC_VINYLTOLUENE");

  //scintillator logical volume
  G4LogicalVolume *scin_vol = new G4LogicalVolume(scin_shape, scin_mat, fNam);

  //scintillator visibility
  G4VisAttributes *scin_vis = new G4VisAttributes();
  scin_vis->SetColor(1, 1, 0, 0.5); // yellow
  scin_vis->SetForceSolid(true);
  scin_vol->SetVisAttributes(scin_vis);

  //put the scintillator plate to the layer
  new G4PVPlacement(0, G4ThreeVector(0, 0, (layer_z - spacer_z)/2.), scin_vol, fNam, lay_vol, false, 0);

}//HcalA262

//_____________________________________________________________________________
G4bool HcalA262::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //deposited energy in step
  G4double edep = step->GetTotalEnergyDeposit()/GeV;

  //scintillator location
  const G4TouchableHandle& hnd = step->GetPreStepPoint()->GetTouchableHandle();

  //separate the deposition into the EM and HAD sections
  if( hnd->GetCopyNumber(1) < fNem ) {
    fEdepEM += edep;
  } else {
    fEdepHAD += edep;
  }

  //if( step->GetTotalEnergyDeposit() < 1e-5 ) return true;

  //G4cout << hnd->GetCopyNumber() << " " << hnd->GetCopyNumber(1) << " " << step->GetTotalEnergyDeposit()/GeV << G4endl;

  return true;

}//ProcessHits

//_____________________________________________________________________________
void HcalA262::ClearEvent() {

  fEdepEM = 0;
  fEdepHAD = 0;

}//ClearEvent
/*
//_____________________________________________________________________________
void HcalA262::FinishEvent() {

  G4cout << fEdepEM << " " << fEdepHAD << G4endl;

}//FinishEvent
*/
//_____________________________________________________________________________
void HcalA262::CreateOutput(TTree *tree) {

  DetUtils u(fNam, tree);

  u.AddBranch("_edep_EM", &fEdepEM, "D");
  u.AddBranch("_edep_HAD", &fEdepHAD, "D");

}//CreateOutput














