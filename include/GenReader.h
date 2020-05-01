
#ifndef GenReader_h
#define GenReader_h

// generator reader

#include "G4VUserPrimaryGeneratorAction.hh"

class G4VPrimaryGenerator;

class GenReader : public G4VUserPrimaryGeneratorAction {

  public:

    GenReader();
    virtual ~GenReader();

    virtual void GeneratePrimaries(G4Event*);

  private:

    G4String fGenType; // generator reader type

    G4GenericMessenger *fMsg; // messenger for generator reader type

    G4VPrimaryGenerator *fGen; // generator reader

    G4VPrimaryGenerator *fGenPy; // pythia reader
    G4VPrimaryGenerator *fGenTX; // TX reader

};

#endif

