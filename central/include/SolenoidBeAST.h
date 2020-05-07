
#ifndef SolenoidBeAST_h
#define SolenoidBeAST_h

//central solenoid with BeAST field map

class BeastMagneticField;
class GeoParser;

#include "G4MagneticField.hh"

class SolenoidBeAST {

  public:

    SolenoidBeAST(G4String nam, GeoParser *geo, G4LogicalVolume*);

  private:

    class Field: public G4MagneticField {
      virtual void GetFieldValue(const G4double p[4], G4double *B) const;
      BeastMagneticField *fMap; // field map
      public:
        Field(BeastMagneticField *map): fMap(map) {}
    };

};

#endif

