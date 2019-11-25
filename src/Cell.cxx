
//_____________________________________________________________________________
//
// cell in composite calorimeter,
// crystal of PbWO4 in carbon fiber casing,
// optical photon detector is on its end
//_____________________________________________________________________________

//C++
#include <vector>

//ROOT
#include "TTree.h"

//Geant
#include "G4LogicalVolume.hh"
#include "G4Box.hh"
#include "G4SubtractionSolid.hh"
#include "G4SystemOfUnits.hh"
#include "G4NistManager.hh"
#include "G4VisAttributes.hh"
#include "G4PVPlacement.hh"
#include "G4VPhysicalVolume.hh"
#include "G4OpticalPhoton.hh"
#include "G4Scintillation.hh"
#include "G4Cerenkov.hh"

//local headers
#include "Cell.h"
#include "CompCal.h"
#include "OpTable.h"
#include "OpDet.h"

//_____________________________________________________________________________
Cell::Cell(const G4String& nam, G4int ix, G4int iy, G4int ncells, G4double zpos, G4double ypos, G4LogicalVolume *top, CompCal& d):
  Detector(), G4VSensitiveDetector(nam), fNam(nam), det(d) {

  G4cout << "  Cell::Cell: " << fNam << G4endl;

  //alveole size
  G4double asiz = 3*cm;

  //crystal size
  G4double csiz = 2.6*cm; //for alveole thickness 0.2 cm

  //cell length
  G4double zlen = 35*cm;

  //cell alveole shape
  G4String alv_nam = fNam+"_alv";
  G4Box *alv_out = new G4Box(alv_nam+"_out", asiz/2., asiz/2, zlen/2.);
  G4Box *alv_in = new G4Box(alv_nam+"_in", csiz/2., csiz/2, zlen/2.);
  G4SubtractionSolid *alv_s = new G4SubtractionSolid(alv_nam, alv_out, alv_in);

  //Carbon fiber for the alveole, according to TestEm10 example, Materials.cc
  if( !G4Material::GetMaterial("CarbonFiber", false) ) {
    G4Element *elC = new G4Element("Carbon", "C", 6., 12.01*g/mole);
    G4Material *alv_m = new G4Material("CarbonFiber", 0.145*g/cm3, 1);
    alv_m->AddElement(elC, 1);
    //G4cout << *(G4Material::GetMaterialTable()) << G4endl;
  }

  //alveole volume
  G4LogicalVolume *alv_l = new G4LogicalVolume(alv_s, G4Material::GetMaterial("CarbonFiber"), alv_nam);

  //do not show the alveole
  alv_l->SetVisAttributes( G4VisAttributes::GetInvisible() );

  //crystal material
  G4Material *crystal_m = G4NistManager::Instance()->FindOrBuildMaterial("G4_PbWO4");

  //scintillation and optical properties for the crystal
  OpTable *optab = new OpTable();
  optab->CrystalTable(crystal_m);

  //crystal shape and volume, same name as the cell for sensitive volume
  G4Box *crystal_s = new G4Box(fNam, csiz/2., csiz/2, zlen/2.);
  G4LogicalVolume *crystal_l = new G4LogicalVolume(crystal_s, crystal_m, fNam);

  //crystal optical surface
  optab->SurfaceTable(crystal_l);

  //drawing the crystal
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(1, 0, 0, 0.5);
  //vis->SetForceSolid(true);
  crystal_l->SetVisAttributes(vis);

  //cell x and y center points
  G4double xcen = -asiz/2. * (ncells-1.) + ix*asiz;

  G4double y0 = asiz/2. * (ncells-1.);
  if(ypos > 0.01) {
    y0 = y0 + ncells*asiz/2. + ypos;
  } else if (ypos < -0.01) {
    y0 = y0 - ncells*asiz/2. + ypos;
  }

  G4double ycen = y0 - iy*asiz;

  //cell alveole in top volume
  new G4PVPlacement(0, G4ThreeVector(xcen, ycen, zpos-zlen/2.), alv_l, alv_nam, top, false, 0);

  //crystal in top volume
  G4VPhysicalVolume *csens = new G4PVPlacement(0, G4ThreeVector(xcen, ycen, zpos-zlen/2.), crystal_l, fNam, top, false, 0);

  //attach optical photon detector, 1.7x1.7 cm
  fOpDet = new OpDet(fNam+"_OpDet", 1.7*cm, zpos-zlen, xcen, ycen, top);
  optab->MakeBoundary(csens, fOpDet->GetPhysicalVolume());

  //indices to identify scintillation and Cerenkov processes
  G4Scintillation scin;
  fScinType = scin.GetProcessType();
  fScinSubType = scin.GetProcessSubType();
  G4Cerenkov cer;
  fCerenkovType = cer.GetProcessType();
  fCerenkovSubType = cer.GetProcessSubType();

  ClearEvent();

}//Cell

//_____________________________________________________________________________
G4bool Cell::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //hit in this cell

  //G4cout << "Cell::ProcessHits, " << fNam << G4endl;

  //increment deposited energy in the cell
  fE += step->GetTotalEnergyDeposit();

  //do not consider optical photon hits since now
  if(step->GetTrack()->GetDynamicParticle()->GetParticleDefinition() == G4OpticalPhoton::OpticalPhotonDefinition()) {
    return true;
  }

  //first point in the detector in the event
  if(det.fZ > 9998.) {
    if(step->GetTrack()->GetTotalEnergy() > 100) {
    //if(1) {

      const G4ThreeVector point = step->GetPreStepPoint()->GetPosition();

      det.fX = point.x();
      det.fY = point.y();
      det.fZ = point.z();

      det.fXyzE = step->GetTrack()->GetTotalEnergy();
    }
  }

  //number of optical photons in the event from secondary tracks
  const std::vector<const G4Track*> *sec = step->GetSecondaryInCurrentStep();
  std::vector<const G4Track*>::const_iterator i;
  for(i = sec->begin(); i != sec->end(); i++) {
    if((*i)->GetParentID() <= 0) continue;

    //all optical photons
    if((*i)->GetDynamicParticle()->GetParticleDefinition() != G4OpticalPhoton::OpticalPhotonDefinition()) continue;
    fNphot++;

    //identify the process
    G4int ptype = (*i)->GetCreatorProcess()->GetProcessType();
    G4int pstype = (*i)->GetCreatorProcess()->GetProcessSubType();
    //scintillation photons
    if(ptype == fScinType && pstype == fScinSubType) fNscin++;
    //Cerenkov photons
    if(ptype == fCerenkovType && pstype == fCerenkovSubType) fNcerenkov++;

  }//secondary tracks loop

  return true;

}//ProcessHits

//_____________________________________________________________________________
void Cell::CreateOutput(TTree *tree) {

  AddBranch("_en", &fE, tree);

  AddBranch("_nphot", &fNphot, tree);
  AddBranch("_nscin", &fNscin, tree);
  AddBranch("_ncerenkov", &fNcerenkov, tree);

}//WriteHeader

//_____________________________________________________________________________
void Cell::ClearEvent() {

  fE = 0.;

  fNphot = 0;
  fNscin = 0;
  fNcerenkov = 0;

}//ClearEvent

//_____________________________________________________________________________
void Cell::Add(std::vector<Detector*> *vec) {

  //add this cell and its parts to sensitive detectors
  vec->push_back(this);
  vec->push_back(fOpDet);

}//Add

//_____________________________________________________________________________
void Cell::AddBranch(const std::string& nam, Double_t *val, TTree *tree) {

  //add branch for one Double_t variable

  std::string name = fNam + nam; // branch name from detector name and variable name
  std::string leaf = name + "/D"; // leaflist for Double_t
  tree->Branch(name.c_str(), val, leaf.c_str()); // create the branch

}//AddBranch

//_____________________________________________________________________________
void Cell::AddBranch(const std::string& nam, ULong64_t *val, TTree *tree) {

  //add branch for one ULong64_t variable

  std::string name = fNam + nam; // branch name from detector name and variable name
  std::string leaf = name + "/l"; // leaflist for Double_t
  tree->Branch(name.c_str(), val, leaf.c_str()); // create the branch

}//AddBranch




































