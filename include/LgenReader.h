
#ifndef LgenReader_h
#define LgenReader_h

// generator reader for lgen / DJANGOH events

#include "globals.hh"
#include "G4VUserPrimaryGeneratorAction.hh"
#include <fstream>

class G4Event;
class G4GenericMessenger;
class GenParticle;

class LgenReader : public G4VUserPrimaryGeneratorAction {

  public:

    LgenReader();
    virtual ~LgenReader();

    virtual void GeneratePrimaries(G4Event*);

  private:

    void OpenInput(); // function to open input file

    std::ifstream fIn; // lgen input
    G4String fInputName; // name of input file

    G4GenericMessenger *fMsg; // messenger for name of input file

    GenParticle *fPhot; // generated bremsstrahlung photon
    GenParticle *fEl; // generated scattered electron
    GenParticle *fBeamEl; // beam electron

};

#endif

