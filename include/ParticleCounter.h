
#ifndef ParticleCounter_h
#define ParticleCounter_h

// Counter plane for incoming particles

class GeoParser;
class G4Step;

#include "Detector.h"
#include "G4VSensitiveDetector.hh"

class ParticleCounter: public Detector, public G4VSensitiveDetector {

  public:

    ParticleCounter(const G4String& nam, GeoParser *geo, G4LogicalVolume *top);

    //Detector
    virtual const G4String& GetName() const {return fNam;}
    virtual void CreateOutput(TTree *tree);
    virtual void ClearEvent();

    //called via G4VSensitiveDetector
    virtual G4bool ProcessHits(G4Step *step, G4TouchableHistory*);

  private:

    G4LogicalVolume* GetMotherVolume(G4String mother_nam, G4LogicalVolume *top);

    G4String fNam; //detector name

    G4bool fRemoveTracks; // stop and remove tracks incident on the counter

    //hits array
    std::vector<Int_t> fHitPdg; // particle pdg
    std::vector<Float_t> fHitEn; // hit energy, GeV
    std::vector<Float_t> fHitX; // hit position in x, mm
    std::vector<Float_t> fHitY; // hit position in y, mm
    std::vector<Float_t> fHitZ; // hit position in z, mm

};

#endif

