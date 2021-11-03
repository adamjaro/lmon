
#ifndef VacDrift_h
#define VacDrift_h

// Vacuum drift section between B2 and Q3 magnets

class GeoParser;

#include "Detector.h"

class VacDrift: public Detector {

  public:

    VacDrift(const G4String& nam, GeoParser *geo, G4LogicalVolume *top);

    //Detector
    virtual const G4String& GetName() const {return fNam;}

  private:

    G4String fNam; //component name

};

#endif

