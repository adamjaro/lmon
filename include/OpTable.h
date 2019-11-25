
#ifndef OpTable_h
#define OpTable_h

// optical and scintillation properties of PbWO4 crystals

class OpTable {

  public:

    void CrystalTable(G4Material *mat);
    void SurfaceTable(G4LogicalVolume *vol);
    void MakeBoundary(G4VPhysicalVolume *crystal, G4VPhysicalVolume *opdet);

};

#endif

