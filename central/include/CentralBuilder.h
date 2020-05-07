
#ifndef CentralBuilder_h
#define CentralBuilder_h

//constructs central detectors and components

class CentralBuilder {

  public:

    CentralBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det);

  private:

    G4LogicalVolume *fTop; // top world volume

    GeoParser *fGeo; // geometry parser

    std::vector<Detector*> *fDet; //all detectors

};

#endif

