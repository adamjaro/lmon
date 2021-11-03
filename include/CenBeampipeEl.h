
#ifndef CenBeampipeEl_h
#define CenBeampipeEl_h

// Central electron beampipe

class GeoParser;

#include "Detector.h"

class CenBeampipeEl: public Detector {

  public:

    CenBeampipeEl(const G4String& nam, GeoParser *geo, G4LogicalVolume *top);

    //Detector
    virtual const G4String& GetName() const {return fNam;}

  private:

    G4String fNam; //segment name

    void Central(GeoParser *geo, G4LogicalVolume *top);
    void NegativeZ(GeoParser *geo, G4LogicalVolume *top);
    void PositiveZ(GeoParser *geo, G4LogicalVolume *top);
    void LargePosZ(GeoParser *geo, G4LogicalVolume *top);

};

#endif

