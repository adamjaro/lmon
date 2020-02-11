
//_____________________________________________________________________________
//
// generator particle for generator readers,
// loads momentum and vertex information from a specific generator format
// and generates itself into the primary vertex
//_____________________________________________________________________________

//C++ 
#include <sstream>
#include <boost/tokenizer.hpp>

//Geant 
#include "G4ParticleDefinition.hh"
#include "G4ParticleTable.hh"
#include "G4PrimaryVertex.hh"
#include "G4ParticleMomentum.hh"
#include "G4SystemOfUnits.hh"
#include "G4PrimaryParticle.hh"

//local classes
#include "GenParticle.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
GenParticle::GenParticle(G4int pdg): fPdg(pdg), fPx(0), fPy(0), fPz(0), fVx(0), fVy(0), fVz(0) {

  // constructor for a given pdg

  fDef = G4ParticleTable::GetParticleTable()->FindParticle(pdg);

  fMass = fDef->GetPDGMass();
  fCharge = fDef->GetPDGCharge();

}//GenParticle

//_____________________________________________________________________________
GenParticle::GenParticle(const std::string &txlin): fVx(0), fVy(0), fVz(0) {

  // constructor from a TX track line

  //G4cout << "GenParticle::GenParticle: " << txlin << G4endl;

  //split the track line
  tokenizer< char_separator<char> > trkline(txlin, char_separator<char>(" "));
  tokenizer< char_separator<char> >::iterator trk_it = trkline.begin();

  //get the momentum
  for(int i=0; i<2; i++) ++trk_it;
  stringstream ss;
  ss << *(trk_it++) << " " << *(trk_it++) << " " << *(trk_it++);
  ss >> fPz >> fPy >> fPx;

  //get pdg
  for(int i=0; i<3; i++) ++trk_it;
  ss.str("");
  ss.clear();
  ss << *(trk_it++);
  ss >> fPdg;

  //definition from the pdg
  fDef = G4ParticleTable::GetParticleTable()->FindParticle(fPdg);

  //mass and charge from the definition
  fMass = fDef->GetPDGMass();
  fCharge = fDef->GetPDGCharge();

  //G4cout << "GenParticle::GenParticle: " << fPx << " " << fPy << " " << fPz << " " << fPdg << G4endl;

}//GenParticle

//_____________________________________________________________________________
void GenParticle::GenerateToVertex(G4PrimaryVertex *vtx) {

  //generate particle to the vertex

  //particle momentum and energy
  G4ParticleMomentum momentum(fPx*GeV, fPy*GeV, fPz*GeV);
  G4ParticleMomentum momentum_direction = momentum.unit();
  G4double mmag = momentum.mag();
  G4double energy = sqrt( mmag*mmag + fMass+fMass ) - fMass;

  //create the primary to put to the vertex
  G4PrimaryParticle *part = new G4PrimaryParticle(fDef);
  part->SetKineticEnergy(energy);
  part->SetMomentumDirection(momentum_direction);

  //mass and charge from the definition
  part->SetMass(fMass);
  part->SetCharge(fCharge);

  //no polarization
  part->SetPolarization(0, 0, 0);

  //put to the vertex
  vtx->SetPrimary(part);

}//GenerateToVertex

//_____________________________________________________________________________
G4PrimaryVertex* GenParticle::MakePrimaryVertex() {

  //create primary vertex from particle position

  return new G4PrimaryVertex(fVx*mm, fVy*mm, fVz*mm, 0);

}//MakePrimaryVertex

//_____________________________________________________________________________
void GenParticle::ReadFromPythia6(tokenizer< char_separator<char> >::iterator &trk_it) {

  //read particle momentum and vertex position from event in Pythia6 format

  //momentum
  stringstream ss;
  ss << *(trk_it++) << " " << *(trk_it++) << " " << *(trk_it++);
  ss >> fPz >> fPy >> fPx;

  //skip the energy and mass
  ++trk_it;
  ++trk_it;

  //get vertex position
  ss.str("");
  ss.clear();
  ss << *(trk_it++) << " " << *(trk_it++) << " " << *(trk_it++);
  ss >> fVz >> fVy >> fVx;

  //G4cout << "GenParticle::ReadFromPythia6: " << fPx << " " << fPy << " " << fPz;
  //G4cout << " " << fVx << " " << fVy << " " << fVz << G4endl;

}//ReadFromPythia6































