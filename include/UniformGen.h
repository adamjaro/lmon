
#ifndef UniformGen_h
#define UniformGen_h

// generator with uniform range of energy

#include "G4VUserPrimaryGeneratorAction.hh"

class G4ParticleGun;
class G4Event;

#include "CLHEP/Random/Random.h"

class UniformGen : public G4VUserPrimaryGeneratorAction {

  public:

    UniformGen();
    virtual ~UniformGen();

    virtual void GeneratePrimaries(G4Event*);

  private:

    G4double fEmin; // minimal energy
    G4double fEmax; // maximal energy

    G4ParticleGun *fGun; // particle gun generator
    CLHEP::HepRandom *fRand; // random generator for the energy

};

#endif

