
#ifndef VacTaggerWin_h
#define VacTaggerWin_h

// Vacuum section in front of taggers

class GeoParser;

#include "Detector.h"

class VacTaggerWin: public Detector {

  public:

    VacTaggerWin(const G4String& nam, GeoParser *geo, G4LogicalVolume *top);

    //Detector
    virtual const G4String& GetName() const {return fNam;}

  private:

    G4String fNam; //component name

};

#endif

