
#ifndef Magnet_h
#define Magnet_h

// spectrometer dipole magnet

class Magnet {

  public:

    Magnet(G4double zpos, G4LogicalVolume*);
    virtual ~Magnet() {}

};

#endif

