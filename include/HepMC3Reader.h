
#ifndef HepMC3Reader_h
#define HepMC3Reader_h

// generator reader for HepMC3 ascii

#include "G4VPrimaryGenerator.hh"

namespace HepMC3 {
  class ReaderAscii;
}

class HepMC3Reader : public G4VPrimaryGenerator {

  public:

    HepMC3Reader();
    virtual ~HepMC3Reader() {}

    virtual void GeneratePrimaryVertex(G4Event*);

  private:

    void OpenInput(); // open the input file

    G4GenericMessenger *fMsg; // messenger for name of input file
    G4String fInputName; // name of input file

    std::shared_ptr<HepMC3::ReaderAscii> fRead; // HepMC3 reader

    unsigned long fIev; // index of current event

    std::map<std::string, std::string> fHepmcAttrib; // event attributes

};

#endif

