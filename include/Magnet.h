
#ifndef Magnet_h
#define Magnet_h

// spectrometer dipole magnet

class GeoParser;

class Magnet {

  public:

    Magnet(const G4String&, GeoParser *geo, G4LogicalVolume*);
    virtual ~Magnet() {}

};

#endif

