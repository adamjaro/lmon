
#ifndef MCEvtDat_h
#define MCEvtDat_h

//MC event data

class TTree;
#include "Rtypes.h"

#include "G4VUserEventInformation.hh"

//_____________________________________________________________________________
class MCEvtDat: public G4VUserEventInformation {
  public:

    MCEvtDat();
    MCEvtDat(const MCEvtDat& d);

    void ConnectInput(TTree *t);
    void LoadGenVal(const MCEvtDat& d);
    void CreateOutput(TTree *t);

    void SetVal(const std::string& nam, Double_t val);

    void Print() const {} // reimplemented
    void Print(std::string msg, std::string dat);

  private:

    std::map<std::string, Double_t*> fGenVal;

};

#endif

