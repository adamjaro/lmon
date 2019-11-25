
#ifndef LgenReader_h
#define LgenReader_h

// generator reader for lgen / DJANGOH events

#include "G4VUserPrimaryGeneratorAction.hh"
#include <fstream>

class G4ParticleDefinition;
class G4Event;

class LgenReader : public G4VUserPrimaryGeneratorAction {

  public:

    LgenReader();
    virtual ~LgenReader() {}

    virtual void GeneratePrimaries(G4Event*);

  private:

    std::ifstream fIn; // lgen input

    G4ParticleDefinition *fGammaDef; // gamma definition for the generator

};

#endif

