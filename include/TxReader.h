
#ifndef TxReader_h
#define TxReader_h

// generator reader for TX (Starlight) format

#include "globals.hh"
#include "G4VUserPrimaryGeneratorAction.hh"
#include <fstream>

class G4ParticleDefinition;
class G4Event;
class G4GenericMessenger;

class TxReader : public G4VUserPrimaryGeneratorAction {

  public:

    TxReader();
    virtual ~TxReader() {}

    virtual void GeneratePrimaries(G4Event*);

  private:

    void OpenInput(); // function to open TX input

    std::ifstream fIn; // TX input
    G4String fInputName; // name of TX input

    G4GenericMessenger *fMsg; // messenger for name of input file

    G4ParticleDefinition *fGammaDef; // gamma definition for the generator

};

#endif

