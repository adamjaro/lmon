
//ROOT
#include "TTree.h"
#include "TLorentzVector.h"

//Geant
#include "G4Event.hh"

//local classes
#include "MCEvent.h"
#include "DetUtils.h"

//_____________________________________________________________________________
MCEvent::MCEvent(): Detector(), fNam("MCEvent") {

  ClearEvent();

}//MCEvent

//_____________________________________________________________________________
void MCEvent::BeginEvent(const G4Event *evt) {

  G4PrimaryVertex *pvtx = evt->GetPrimaryVertex();
  if(!pvtx) return;

  //position of generated vertex, mm
  fVx = pvtx->GetX0();
  fVy = pvtx->GetY0();
  fVz = pvtx->GetZ0();

  //G4cout << "MCEvent::BeginEvent: " << fVx << " " << fVy << " " << fVz << G4endl;

  //particles loop
  for(G4int i=0; i<pvtx->GetNumberOfParticle(); i++) {
    G4PrimaryParticle *part = pvtx->GetPrimary(i);

    //read the photon and electron
    G4int pdg = part->GetPDGcode();
    if(pdg == 22) ReadPhoton(part);
    if(pdg == 11) ReadElectron(part);

  }//particles loop

}//BeginEvent

//_____________________________________________________________________________
void MCEvent::ReadPhoton(G4PrimaryParticle *part) {

  //generated photon variables

  //G4cout << "MCEvent::ReadPhoton: " << part->GetPDGcode() << G4endl;

  //energy of generated gamma photon
  fPhotGen = part->GetTotalEnergy();
  fPhotGen = fPhotGen/1e3; // to GeV

  //Lorentz vector for angles
  G4double px = part->GetPx()/1e3; // to GeV
  G4double py = part->GetPy()/1e3;
  G4double pz = part->GetPz()/1e3;

  TLorentzVector vec;
  vec.SetPxPyPzE(px, py, pz, fPhotGen);

  //azimuthal and polar angle
  fPhotTheta = vec.Theta();
  fPhotPhi = vec.Phi();

}//ReadPhoton

//_____________________________________________________________________________
void MCEvent::ReadElectron(G4PrimaryParticle *part) {

  //scattered electron

  //G4cout << "MCEvent::ReadElectron: " << part->GetPDGcode() << G4endl;

  //electron energy
  fElGen = part->GetTotalEnergy();
  fElGen = fElGen/1e3; // to GeV

  //G4cout << "MCEvent::ReadElectron: " << fElGen << G4endl;

}//ReadElectron

//_____________________________________________________________________________
void MCEvent::CreateOutput(TTree *tree) {

  //set MC output branches

  DetUtils u("", tree);

  u.AddBranch("phot_gen", &fPhotGen, "D");
  u.AddBranch("phot_theta", &fPhotTheta, "D");
  u.AddBranch("phot_phi", &fPhotPhi, "D");

  u.AddBranch("vtx_x", &fVx, "D");
  u.AddBranch("vtx_y", &fVy, "D");
  u.AddBranch("vtx_z", &fVz, "D");

  u.AddBranch("el_gen", &fElGen, "D");

}//CreateOutput

//_____________________________________________________________________________
void MCEvent::ClearEvent() {

  fPhotGen = 0.;
  fPhotTheta = 0.;
  fPhotPhi = 0.;

  fVx = -9999.;
  fVy = -9999.;
  fVz = -9999.;

  fElGen = 0.;

}//ClearEvent











