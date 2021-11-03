
#ifndef VacB2lumiWin_h
#define VacB2lumiWin_h

// Vacuum between B2 magnet and luminosity exit window

class GeoParser;

#include "Detector.h"

class VacB2lumiWin: public Detector {

  public:

    VacB2lumiWin(const G4String& nam, GeoParser *geo, G4LogicalVolume *top);

    //Detector
    virtual const G4String& GetName() const {return fNam;}

  private:

    G4String fNam; //component name

};

#endif

