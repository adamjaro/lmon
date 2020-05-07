
#ifndef CentralBuilder_h
#define CentralBuilder_h

//constructs central detectors and components

class CentralBuilder {

  public:

    CentralBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det);

  private:

    void AddDetector(unsigned int i); // add detector or component

    G4LogicalVolume *fTop; // top world volume

    GeoParser *fGeo; // geometry parser

    std::vector<Detector*> *fDet; //all detectors

};

#endif

