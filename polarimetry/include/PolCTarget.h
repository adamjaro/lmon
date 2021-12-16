
#ifndef PolCTarget_h
#define PolCTarget_h

// carbon target

#include "Detector.h"

class G4VPhysicalVolume;
class GeoParser;

class PolCTarget : public Detector {

  public:

    PolCTarget(const G4String&, GeoParser *geo, G4LogicalVolume *top);
    virtual ~PolCTarget() {}

    //Detector
    virtual const G4String& GetName() const {return fNam;}

  private:

    G4String fNam; // component name

    G4VisAttributes *ColorDecoder(GeoParser *geo);

};

#endif



















