
#ifndef BeamDrift_h
#define BeamDrift_h

// Beam drift section between B2 and Q3 magnets

class GeoParser;

#include "Detector.h"

class BeamDrift: public Detector {

  public:

    BeamDrift(G4String nam, GeoParser *geo, G4LogicalVolume *top);

    //Detector
    virtual const G4String& GetName() const {return fNam;}

  private:

    G4String fNam; //component name

};

#endif

