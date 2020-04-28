
//_____________________________________________________________________________
//
// generator with uniform range of energy
//
//_____________________________________________________________________________

//Geant headers
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"

//local headers
#include "UniformGen.h"

//_____________________________________________________________________________
UniformGen::UniformGen() : G4VUserPrimaryGeneratorAction(), fGun(0) {

  //minimal and maximal energy, in GeV
  fEmin = 1;
  fEmax = 18;
  //fEmin = 0.01;
  //fEmax = 0.02;

  fGun = new G4ParticleGun(1); //number of particles

  G4String nam = "gamma";
  G4ParticleDefinition *particle = G4ParticleTable::GetParticleTable()->FindParticle(nam);
  fGun->SetParticleDefinition(particle);
  fGun->SetParticleMomentumDirection(G4ThreeVector(0, 0, -1));

  //uniform random generator for energy values
  fRand = new CLHEP::HepRandom();

}//UniformGen

//_____________________________________________________________________________
UniformGen::~UniformGen() {

  delete fGun;

}//~UniformGen

//_____________________________________________________________________________
void UniformGen::GeneratePrimaries(G4Event *evt) {

  G4double en = 0;
  while(en < fEmin) {
    en = fEmax * fRand->flat();
  }
  fGun->SetParticleEnergy(en*GeV);

  fGun->GeneratePrimaryVertex(evt);

}//GeneratePrimaries




















