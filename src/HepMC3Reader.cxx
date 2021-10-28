
//_____________________________________________________________________________
//
// generator reader for HepMC3 ascii
//
//_____________________________________________________________________________

//C++
#include <vector>

//HepMC3
#include "HepMC3/ReaderAscii.h"
#include "HepMC3/GenParticle.h"

//Geant
#include "G4GenericMessenger.hh"
#include "G4Event.hh"
#include "G4PrimaryVertex.hh"
#include "G4PrimaryParticle.hh"
#include "G4SystemOfUnits.hh"

//local classes
#include "HepMC3Reader.h"
#include "MCEvtDat.h"

using namespace std;
using namespace HepMC3;

//_____________________________________________________________________________
HepMC3Reader::HepMC3Reader() : G4VPrimaryGenerator(), fInputName(""),
  fRead(nullptr), fIev(0) {

  //command for input name
  fMsg = new G4GenericMessenger(this, "/lmon/input/hepmc/");
  fMsg->DeclareProperty("name", fInputName);


}//HepMC3Reader

//_____________________________________________________________________________
void HepMC3Reader::GeneratePrimaryVertex(G4Event *evt) {

  //open at the first call
  if(fRead == nullptr) OpenInput();

  if( (++fIev)%100000 == 0 ) {
    G4cout << "HepMC3Reader::GeneratePrimaryVertex, event number: " << fIev << G4endl;
  }

  //read the event
  GenEvent mc(Units::GEV,Units::MM);
  fRead->read_event(mc);

  //event attributes
  MCEvtDat *dat = new MCEvtDat();

  shared_ptr<DoubleAttribute> flux_photon_per_s = mc.attribute<DoubleAttribute>("Flux_[photon/s]");
  shared_ptr<DoubleAttribute> power_W = mc.attribute<DoubleAttribute>("Power_[W]");
  if(flux_photon_per_s) {
    dat->SetVal("flux_photon_per_s", flux_photon_per_s->value());
  }
  if(power_W) {
    dat->SetVal("power_W", power_W->value());
  }

  evt->SetUserInformation(dat);

  //primary vertex
  const FourVector pos = mc.event_pos();
  G4PrimaryVertex *vtx = new G4PrimaryVertex(pos.x()*mm, pos.y()*mm, pos.z()*mm, 0);

  //particles in event
  for(auto p: mc.particles()) {

    const FourVector vec = p->momentum();

    //create the G4 particle
    G4PrimaryParticle *gp = new G4PrimaryParticle(p->pid(), vec.px()*GeV, vec.py()*GeV, vec.pz()*GeV, vec.e()*GeV);
    gp->SetPolarization(0, 0, 0);
    vtx->SetPrimary(gp);

    //G4cout << vec.px() << " " << vec.py() << " " << vec.pz() << " " << vec.e() << " " << p->pid() << G4endl;

  }//particles in event

  //put the vertex to the event
  evt->AddPrimaryVertex(vtx);

}//GeneratePrimaryVertex

//_____________________________________________________________________________
void HepMC3Reader::OpenInput() {

  G4cout << "HepMC3Reader::OpenInput: " << fInputName << G4endl;

  fRead = make_shared<ReaderAscii>(fInputName.data());


}//OpenInput






















