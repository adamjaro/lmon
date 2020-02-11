
//_____________________________________________________________________________
//
// testing generator for one or two particles
//
//_____________________________________________________________________________

//Geant headers
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"

//local headers
#include "GeneratorAction.h"

//_____________________________________________________________________________
GeneratorAction::GeneratorAction() : G4VUserPrimaryGeneratorAction(), fGun(0), fGun2(0) {

  fGun = new G4ParticleGun(1); //number of particles

  //G4String nam = "gamma";
  G4String nam = "e-";
  G4ParticleDefinition *particle = G4ParticleTable::GetParticleTable()->FindParticle(nam);
  fGun->SetParticleDefinition(particle);
  fGun->SetParticleMomentumDirection(G4ThreeVector(0, 0, -1));
  //fGun->SetParticlePosition(G4ThreeVector(0, 0.2*cm, 0));
  fGun->SetParticleEnergy(9*GeV); // 10*MeV  1*GeV  4.5*GeV

  fGun2 = new G4ParticleGun(1);
  G4ParticleDefinition *p2 = G4ParticleTable::GetParticleTable()->FindParticle("e-");
  fGun2->SetParticleDefinition(p2);
  fGun2->SetParticleMomentumDirection(G4ThreeVector(0, 0, -1));
  //fGun2->SetParticlePosition(G4ThreeVector(0, -0.2*cm, 0));
  fGun2->SetParticleEnergy(18*GeV);

}//GeneratorAction

//_____________________________________________________________________________
GeneratorAction::~GeneratorAction() {

  delete fGun;

}//~GeneratorAction

//_____________________________________________________________________________
void GeneratorAction::GeneratePrimaries(G4Event *evt) {

  fGun->GeneratePrimaryVertex(evt);
  fGun2->GeneratePrimaryVertex(evt);

}//GeneratePrimaries




















