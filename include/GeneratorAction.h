
#ifndef GeneratorAction_h
#define GeneratorAction_h

// testing generator for one or two particles

#include "G4VUserPrimaryGeneratorAction.hh"

class G4ParticleGun;
class G4Event;

class GeneratorAction : public G4VUserPrimaryGeneratorAction {

  public:

    GeneratorAction();
    virtual ~GeneratorAction();

    virtual void GeneratePrimaries(G4Event*);

  private:

    G4ParticleGun *fGun; // G4 gun
    G4ParticleGun *fGun2;

};

#endif

