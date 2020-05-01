
#ifndef TxReader_h
#define TxReader_h

// generator reader for TX (Starlight) format

#include "globals.hh"
#include "G4VPrimaryGenerator.hh"
#include <fstream>

class G4Event;
class G4GenericMessenger;

class TxReader : public G4VPrimaryGenerator {

  public:

    TxReader();
    virtual ~TxReader() {}

    virtual void GeneratePrimaryVertex(G4Event *evt);

  private:

    void OpenInput(); // function to open TX input

    //vertex coordinates and number of tracks
    void ReadVertex(const std::string& line, G4double& vx, G4double& vy, G4double& vz, int& ntrk);

    std::ifstream fIn; // TX input
    G4String fInputName; // name of TX input

    G4int fSelPdg; // select the particle to generate according to its pdg

    G4GenericMessenger *fMsg; // messenger for name of input file

    int fIev; // event number for progress printout

};

#endif

