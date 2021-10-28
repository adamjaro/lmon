
//C++
#include<vector>

//ROOT
#include "TTree.h"
#include "TLorentzVector.h"

//Geant
#include "G4Event.hh"
#include "G4SystemOfUnits.hh"

//local classes
#include "MCEvent.h"
#include "DetUtils.h"

//_____________________________________________________________________________
MCEvent::MCEvent(): Detector(), fNam("MCEvent") {

  ClearEvent();

}//MCEvent

//_____________________________________________________________________________
void MCEvent::BeginEvent(const G4Event *evt) {

  //generator data
  ReadEvtDat(evt);

  //event vertex
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

    //add particle to the output
    fPartPdg.push_back( part->GetPDGcode() );
    fPartPx.push_back( part->GetPx()/GeV );
    fPartPy.push_back( part->GetPy()/GeV );
    fPartPz.push_back( part->GetPz()/GeV );
    fPartEn.push_back( part->GetTotalEnergy()/GeV );

    //G4cout << "MCEvent::BeginEvent: " << part->GetPDGcode() << G4endl;
    //G4cout << part->GetPDGcode() << " " << part->GetPx()/GeV << " " << part->GetPy()/GeV << " " << part->GetPz()/GeV;
    //G4cout << " " << part->GetTotalEnergy()/GeV << G4endl;
    //G4cout << " " << part->GetMass()/GeV << " " << part->GetCharge() << G4endl;
    //G4cout << "MCEvent::BeginEvent: " << part->GetPx()/GeV << " " << part->GetPy()/GeV << " " << part->GetPz()/GeV << G4endl;
    //G4cout << G4endl;

    //read the photon and electron
    G4int pdg = part->GetPDGcode();
    if(pdg == 22) ReadPhoton(part);
    if(pdg == 11) ReadElectron(part);

  }//particles loop

  //G4cout << G4endl;

}//BeginEvent

//_____________________________________________________________________________
void MCEvent::ReadEvtDat(const G4Event *evt) {

  //generator data

  MCEvtDat *dat = dynamic_cast<MCEvtDat*>(evt->GetUserInformation());
  if(!dat) return;

  //load the input data
  fDat.LoadGenVal(*dat);

  //fDat.Print("MCEvent power:", "power_W");
  //G4cout << G4endl;

}//ReadEvtDat

//_____________________________________________________________________________
void MCEvent::ReadPhoton(G4PrimaryParticle *part) {

  //generated photon variables

  //G4cout << "MCEvent::ReadPhoton: " << part->GetPDGcode() << G4endl;

  //energy of generated gamma photon
  fPhotGen = part->GetTotalEnergy();
  fPhotGen = fPhotGen/1e3; // to GeV

  //azimuthal and polar angle
  GetThetaPhi(part, fPhotTheta, fPhotPhi);

}//ReadPhoton

//_____________________________________________________________________________
void MCEvent::ReadElectron(G4PrimaryParticle *part) {

  //scattered electron

  //G4cout << "MCEvent::ReadElectron: " << part->GetPDGcode() << G4endl;

  //electron energy
  fElGen = part->GetTotalEnergy();
  fElGen = fElGen/1e3; // to GeV

  //G4cout << "MCEvent::ReadElectron: " << fElGen << G4endl;

  //electron azimuthal and polar angle
  GetThetaPhi(part, fElTheta, fElPhi);

}//ReadElectron

//_____________________________________________________________________________
void MCEvent::GetThetaPhi(G4PrimaryParticle *part, Double_t &theta, Double_t &phi) {

  //theta and phi angles for generated particle

  //energy and momentum for Lorentz vector
  G4double en = part->GetTotalEnergy()/1e3; // to GeV
  G4double px = part->GetPx()/1e3;
  G4double py = part->GetPy()/1e3;
  G4double pz = part->GetPz()/1e3;

  //Lorentz vector for angles
  TLorentzVector vec;
  vec.SetPxPyPzE(px, py, pz, en);

  //azimuthal and polar angle
  theta = vec.Theta();
  phi = vec.Phi();

}//GetThetaPhi

//_____________________________________________________________________________
void MCEvent::CreateOutput(TTree *tree) {

  //set MC output branches

  tree->Branch("gen_pdg", &fPartPdg);
  tree->Branch("gen_px", &fPartPx);
  tree->Branch("gen_py", &fPartPy);
  tree->Branch("gen_pz", &fPartPz);
  tree->Branch("gen_en", &fPartEn);

  DetUtils u("", tree);

  fDat.CreateOutput(tree);

  u.AddBranch("phot_gen", &fPhotGen, "D");
  u.AddBranch("phot_theta", &fPhotTheta, "D");
  u.AddBranch("phot_phi", &fPhotPhi, "D");

  u.AddBranch("vtx_x", &fVx, "D");
  u.AddBranch("vtx_y", &fVy, "D");
  u.AddBranch("vtx_z", &fVz, "D");

  u.AddBranch("el_gen", &fElGen, "D");
  u.AddBranch("el_theta", &fElTheta, "D");
  u.AddBranch("el_phi", &fElPhi, "D");

}//CreateOutput

//_____________________________________________________________________________
void MCEvent::ClearEvent() {

  fPartPdg.clear();
  fPartPx.clear();
  fPartPy.clear();
  fPartPz.clear();
  fPartEn.clear();

  fPhotGen = 0.;
  fPhotTheta = 0.;
  fPhotPhi = 0.;

  fVx = -9999.;
  fVy = -9999.;
  fVz = -9999.;

  fElGen = 0.;
  fElTheta = 0.;
  fElPhi = 0.;

}//ClearEvent











