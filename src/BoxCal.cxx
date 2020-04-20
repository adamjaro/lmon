
//_____________________________________________________________________________
//
// simple calorimeter,
// box of PbWO4 with optical photon detector on its end
//_____________________________________________________________________________

//C++
#include <string>

//ROOT
#include "TTree.h"

//Geant
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4VPhysicalVolume.hh"
#include "G4Step.hh"
#include "G4VisAttributes.hh"
#include "G4OpticalPhoton.hh"
#include "G4RunManager.hh"
#include "G4Scintillation.hh"
#include "G4Cerenkov.hh"

//local headers
#include "BoxCal.h"
#include "OpDet.h"
#include "OpTable.h"
#include "GeoParser.h"

//_____________________________________________________________________________
BoxCal::BoxCal(const G4String& nam, GeoParser *geo, G4LogicalVolume *top): Detector(),
  G4VSensitiveDetector(nam), fNam(nam), fSens(0) {

  G4cout << "  BoxCal: " << fNam << G4endl;

  G4double zpos = geo->GetD(fNam, "zpos") * mm;
  G4double ypos = geo->GetD(fNam, "ypos") * mm;

  //nist material manager for detector PbW04
  G4NistManager *nist = G4NistManager::Instance();
  G4Material *det_m = nist->FindOrBuildMaterial("G4_PbWO4");

  //scintillation and optical properties
  OpTable *optab = new OpTable();
  optab->CrystalTable(det_m);

  //detector shape
  G4double xysiz = 20*cm;
  G4double zsiz = 35*cm;

  //crystal volume
  G4Box *det_s = new G4Box(nam, xysiz/2., xysiz/2., zsiz/2.);
  //logical name must be same as detector name to allow for sensitivity
  G4LogicalVolume *det_l = new G4LogicalVolume(det_s, det_m, fNam);

  //crystal optical surface
  optab->SurfaceTable(det_l);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(1, 0, 0);
  //vis->SetLineWidth(2);
  det_l->SetVisAttributes(vis);

  //put detector to the top volume, center along y up or down
  G4double ymid = 0;
  if(ypos > 0.1*cm) {
    ymid = xysiz/2. + ypos;
  } else if(ypos < -0.1*cm) {
    ymid = -1*xysiz/2. + ypos;
  }
  fSens = new G4PVPlacement(0, G4ThreeVector(0, ymid, zpos-zsiz/2.), det_l, nam, top, false, 0);

  //include optical photon detector, 10x10 cm
  fOpDet = new OpDet(nam+"_OpDet", 10*cm, zpos-zsiz, 0, ymid, top);
  optab->MakeBoundary(fSens, fOpDet->GetPhysicalVolume());

  //indices to identify scintillation and Cerenkov processes
  G4Scintillation scin;
  fScinType = scin.GetProcessType();
  fScinSubType = scin.GetProcessSubType();
  G4Cerenkov cer;
  fCerenkovType = cer.GetProcessType();
  fCerenkovSubType = cer.GetProcessSubType();

}//BoxCal

//_____________________________________________________________________________
G4bool BoxCal::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //hit in this detector

  //G4cout << "BoxCal::ProcessHits" << G4endl;

  //increment energy deposit in the detector in the event
  fEdep += step->GetTotalEnergyDeposit();

  //do not consider optical photon hits
  if(step->GetTrack()->GetDynamicParticle()->GetParticleDefinition() == G4OpticalPhoton::OpticalPhotonDefinition()) {
    return true;
  }

  //first point in the detector in the event
  if(fZ > 9998.) {

    const G4ThreeVector point = step->GetPreStepPoint()->GetPosition();

    fX = point.x();
    fY = point.y();
    fZ = point.z();
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
void BoxCal::ClearEvent() {

  //G4cout << "BoxCal::ClearEvent" << G4endl;

  //clear event variables
  fEdep = 0;
  fX = 9999.;
  fY = 9999.;
  fZ = 9999.;

  fNphot = 0;
  fNscin = 0;
  fNcerenkov = 0;

}//ClearEvent

//_____________________________________________________________________________
void BoxCal::CreateOutput(TTree *tree) {

  AddBranch("_en", &fEdep, tree);
  AddBranch("_x", &fX, tree);
  AddBranch("_y", &fY, tree);
  AddBranch("_z", &fZ, tree);

  AddBranch("_nphot", &fNphot, tree);
  AddBranch("_nscin", &fNscin, tree);
  AddBranch("_ncerenkov", &fNcerenkov, tree);

}//CreateOutput

//_____________________________________________________________________________
void BoxCal::Add(std::vector<Detector*> *vec) {

  //add this detector and its parts to sensitive detectors
  vec->push_back(this);
  vec->push_back(fOpDet);

}//Add

//_____________________________________________________________________________
void BoxCal::AddBranch(const std::string& nam, Double_t *val, TTree *tree) {

  //add branch for one Double_t variable

  std::string name = fNam + nam; // branch name from detector name and variable name
  std::string leaf = name + "/D"; // leaflist for Double_t
  tree->Branch(name.c_str(), val, leaf.c_str()); // create the branch

}//AddBranch

//_____________________________________________________________________________
void BoxCal::AddBranch(const std::string& nam, ULong64_t *val, TTree *tree) {

  //add branch for one ULong64_t variable

  std::string name = fNam + nam; // branch name from detector name and variable name
  std::string leaf = name + "/l"; // leaflist for Double_t
  tree->Branch(name.c_str(), val, leaf.c_str()); // create the branch

}//AddBranch




























