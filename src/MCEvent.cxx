
//C++
#include<vector>

//ROOT
#include "TTree.h"

//Geant
#include "G4Event.hh"
#include "G4SystemOfUnits.hh"

//local classes
#include "MCEvent.h"

//_____________________________________________________________________________
MCEvent::MCEvent(): Detector(), fNam("MCEvent") {

  ClearEvent();

}//MCEvent

//_____________________________________________________________________________
void MCEvent::BeginEvent(const G4Event *evt) {

  //generator data
  ReadEvtDat(evt);

  //G4cout << "MCEvent::BeginEvent: " << evt->GetNumberOfPrimaryVertex() << G4endl;

  //vertex loop
  for(G4int iv=0; iv<evt->GetNumberOfPrimaryVertex(); iv++) {

    //event vertex
    G4PrimaryVertex *pvtx = evt->GetPrimaryVertex(iv);

    //particles loop
    for(G4int i=0; i<pvtx->GetNumberOfParticle(); i++) {
      G4PrimaryParticle *part = pvtx->GetPrimary(i);

      //add particle to the output
      fPartPdg.push_back( part->GetPDGcode() );
      fPartPx.push_back( part->GetPx()/GeV );
      fPartPy.push_back( part->GetPy()/GeV );
      fPartPz.push_back( part->GetPz()/GeV );
      fPartEn.push_back( part->GetTotalEnergy()/GeV );

      fPartVx.push_back( pvtx->GetX0()/mm );
      fPartVy.push_back( pvtx->GetY0()/mm );
      fPartVz.push_back( pvtx->GetZ0()/mm );

      //G4cout << "MCEvent::BeginEvent: " << part->GetPDGcode() << G4endl;
      //G4cout << part->GetPDGcode() << " " << part->GetPx()/GeV << " " << part->GetPy()/GeV << " " << part->GetPz()/GeV;
      //G4cout << " " << part->GetTotalEnergy()/GeV << G4endl;
      //G4cout << " " << part->GetMass()/GeV << " " << part->GetCharge() << G4endl;
      //G4cout << "MCEvent::BeginEvent: " << part->GetPx()/GeV << " " << part->GetPy()/GeV << " " << part->GetPz()/GeV << G4endl;
      //G4cout << G4endl;

    }//particles loop

  }//vertex loop

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
void MCEvent::CreateOutput(TTree *tree) {

  //set MC output branches

  tree->Branch("gen_pdg", &fPartPdg);
  tree->Branch("gen_px", &fPartPx);
  tree->Branch("gen_py", &fPartPy);
  tree->Branch("gen_pz", &fPartPz);
  tree->Branch("gen_en", &fPartEn);
  tree->Branch("gen_vx", &fPartVx);
  tree->Branch("gen_vy", &fPartVy);
  tree->Branch("gen_vz", &fPartVz);

  fDat.CreateOutput(tree);

}//CreateOutput

//_____________________________________________________________________________
void MCEvent::ClearEvent() {

  fPartPdg.clear();
  fPartPx.clear();
  fPartPy.clear();
  fPartPz.clear();
  fPartEn.clear();

  fPartVx.clear();
  fPartVy.clear();
  fPartVz.clear();

}//ClearEvent











