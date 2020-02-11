
#ifndef BeamMagnet_h
#define BeamMagnet_h

// beamline dipole magnet

class BeamMagnet {

  public:

    BeamMagnet(G4double zpos, G4LogicalVolume*);
    virtual ~BeamMagnet() {}

};

#endif

