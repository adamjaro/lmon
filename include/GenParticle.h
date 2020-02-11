
#ifndef GenParticle_h
#define GenParticle_h

// generator particle

//class G4PrimaryVertex;

class GenParticle {

  public:

    GenParticle(G4int pdg); // constructor for a given pdg
    GenParticle(const std::string &txlin); // constructor from a TX track line

    virtual ~GenParticle() {}

    void GenerateToVertex(G4PrimaryVertex *vtx);
    G4PrimaryVertex* MakePrimaryVertex();

    void ReadFromPythia6(boost::tokenizer< boost::char_separator<char> >::iterator &trk_it);

    G4int GetPdg() const {return fPdg;}

  private:

    G4int fPdg; // pdg code for the definition

    G4ParticleDefinition *fDef; // definition from G4

    G4double fMass; // mass from the definition
    G4double fCharge; // charge from the definition

    G4double fPx; // momentum in x, GeV
    G4double fPy; // momentum in y, GeV
    G4double fPz; // momentum in z, GeV

    G4double fVx; // vertex position in x, mm
    G4double fVy; // vertex position in y, mm
    G4double fVz; // vertex position in z, mm

};

#endif

