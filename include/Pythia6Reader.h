
#ifndef Pythia6Reader_h
#define Pythia6Reader_h

// generator reader for Pythia6 ascii (Lund) events

#include "globals.hh"
#include "G4VPrimaryGenerator.hh"
#include <fstream>
#include <set>

class G4Event;
class G4GenericMessenger;
class GenParticle;

class Pythia6Reader : public G4VPrimaryGenerator {

  public:

    Pythia6Reader();
    virtual ~Pythia6Reader();

    virtual void GeneratePrimaryVertex(G4Event*);

  private:

    void OpenInput(); // function to open input file

    void AddSelectPdg(G4int);

    std::ifstream fIn; // ascii input
    G4String fInputName; // name of input file

    G4GenericMessenger *fMsg; // messenger for name of input file

    std::vector<GenParticle> fParticles; // generated particles in event

    std::set<G4int> fSelPdg; // codes for particles selected to generate

};

#endif

