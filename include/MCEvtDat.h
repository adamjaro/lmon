
#ifndef MCEvtDat_h
#define MCEvtDat_h

//MC event data

#include "G4VUserEventInformation.hh"

//_____________________________________________________________________________
class MCEvtDat: public G4VUserEventInformation {
  public:

    MCEvtDat(): G4VUserEventInformation(), fTrueQ2(0), fTrueX(0), fTrueY(0) {}
    MCEvtDat(const MCEvtDat& d): G4VUserEventInformation(),
      fTrueQ2(d.fTrueQ2), fTrueX(d.fTrueX), fTrueY(d.fTrueY) {}

    Double_t fTrueQ2; // generator true Q^2
    Double_t fTrueX; // true x
    Double_t fTrueY; // true y

    void Print() const {} // reimplemented
};

#endif

