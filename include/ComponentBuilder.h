
#ifndef ComponentBuilder_h
#define ComponentBuilder_h

// constructs detectors and components

class ComponentBuilder {

  public:

    ComponentBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det);

  private:

    void AddDetector(unsigned int i); // add detector to all detectors

    G4LogicalVolume *fTop; // top world volume

    GeoParser *fGeo; // geometry parser

    std::vector<Detector*> *fDet; //all detectors

};

#endif

