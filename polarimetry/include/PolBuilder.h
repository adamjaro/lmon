
#ifndef PolBuilder_h
#define PolBuilder_h

//builder for polarimetry

#include <map>

class PolBuilder {

  public:

    PolBuilder(G4LogicalVolume *top, GeoParser *geo, std::vector<Detector*> *det);

  private:

    void AddDetector(unsigned int i); // add detector or component

    G4LogicalVolume *fTop; // top world volume

    GeoParser *fGeo; // geometry parser

    std::vector<Detector*> *fDet; //all detectors

    //factory function for detectors and components
    template<class det> Detector* MakeDet(G4String nam, GeoParser *geo, G4LogicalVolume *vol) {
      return new det(nam, geo, vol);
    }
    typedef Detector* (PolBuilder::*MakeDetPtr)(G4String, GeoParser*, G4LogicalVolume*);

    std::map<G4String, MakeDetPtr> fComp; // component definitions
    std::map<G4String, MakeDetPtr> fDets; // detector definitions

};

#endif
