
#ifndef SolenoidBeAST_h
#define SolenoidBeAST_h

//central solenoid with BeAST field map

class BeastMagneticField;
class GeoParser;

#include "G4MagneticField.hh"

class SolenoidBeAST {

  public:

    SolenoidBeAST(G4String nam, GeoParser *geo, G4LogicalVolume*);

    G4LogicalVolume *GetLogicalVolume() const {return fVol;}

  private:

    class Field: public G4MagneticField {
      virtual void GetFieldValue(const G4double p[4], G4double *B) const;
      BeastMagneticField *fMap; // field map
      public:
        Field(BeastMagneticField *map): fMap(map) {}
    };

    G4LogicalVolume *fVol; // solenoid logical volume

    G4VSolid *CylWithCutout(G4String nam, G4double r, G4double len, G4double zs, G4double r1);

};

#endif

