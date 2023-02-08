
#ifndef MCEvent_h
#define MCEvent_h

#include "Detector.h"
#include "Rtypes.h"

#include "MCEvtDat.h"

class MCEvent : public Detector {

  public:

    MCEvent();
    virtual ~MCEvent() {}

    void BeginEvent(const G4Event *evt);

    //Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree) { fDat.CreateOutput(tree); }

  private:

    void ReadEvtDat(const G4Event *evt);

    G4String fNam; // class name

    MCEvtDat fDat; //event data

};

#endif

