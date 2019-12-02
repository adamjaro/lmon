
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

  //energy of generated gamma photon
  G4PrimaryParticle *part = evt->GetPrimaryVertex()->GetPrimary();
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

  //G4cout << "MCEvent::BeginEvent " << fPhotGen << " " << px << " " << py << " " << pz << G4endl;
  //G4cout << "MCEvent::BeginEvent " << vec.E() << " " << vec.Theta() << " " << vec.Phi() << G4endl;

}//BeginEvent

//_____________________________________________________________________________
void MCEvent::CreateOutput(TTree *tree) {

  //set MC output branches

  DetUtils u("", tree);

  u.AddBranch("phot_gen", &fPhotGen, "D");
  u.AddBranch("phot_theta", &fPhotTheta, "D");
  u.AddBranch("phot_phi", &fPhotPhi, "D");

}//CreateOutput

//_____________________________________________________________________________
void MCEvent::ClearEvent() {

  fPhotGen = 0.;
  fPhotTheta = 0.;
  fPhotPhi = 0.;

}//ClearEvent











