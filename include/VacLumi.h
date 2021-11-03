
#ifndef VacLumi_h
#define VacLumi_h

// Vacuum section in luminosity system

class GeoParser;

#include "Detector.h"

class VacLumi: public Detector {

  public:

    VacLumi(const G4String& nam, GeoParser *geo, G4LogicalVolume *top);

    //Detector
    virtual const G4String& GetName() const {return fNam;}

  private:

    G4String fNam; //component name

};

#endif

