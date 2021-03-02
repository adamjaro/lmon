
#ifndef CaloBuilder_h
#define CaloBuilder_h

//builder for a set of calorimeters

class CaloBuilder {

  public:

    CaloBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det);

  private:

    void AddDetector(unsigned int i); // add detector or component

    G4LogicalVolume *fTop; // top world volume

    GeoParser *fGeo; // geometry parser

    std::vector<Detector*> *fDet; //all detectors

};

#endif
