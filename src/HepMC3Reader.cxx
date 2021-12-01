
//_____________________________________________________________________________
//
// generator reader for HepMC3 ascii
//
//_____________________________________________________________________________

//C++
#include <vector>
#include <map>

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

  //event attributes, name in hepmc (first) and name in event output (second)
  fHepmcAttrib.insert(make_pair("truex", "true_x"));
  fHepmcAttrib.insert(make_pair("truey", "true_y"));
  fHepmcAttrib.insert(make_pair("trueQ2", "true_Q2"));
  fHepmcAttrib.insert(make_pair("trueW2", "true_W2"));
  fHepmcAttrib.insert(make_pair("true_el_pT", "true_el_pT"));
  fHepmcAttrib.insert(make_pair("true_el_theta", "true_el_theta"));
  fHepmcAttrib.insert(make_pair("true_el_phi", "true_el_phi"));
  fHepmcAttrib.insert(make_pair("true_el_E", "true_el_E"));
  fHepmcAttrib.insert(make_pair("true_el_Q2", "true_el_Q2"));
  fHepmcAttrib.insert(make_pair("Flux_[photon/s]", "flux_photon_per_s"));
  fHepmcAttrib.insert(make_pair("Power_[W]", "power_W"));

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

  //loop over hepmc attributes
  map<string, string>::const_iterator iatt = fHepmcAttrib.cbegin();
  for(; iatt != fHepmcAttrib.cend(); iatt++) {

    shared_ptr<DoubleAttribute> attrib = mc.attribute<DoubleAttribute>( (*iatt).first );

    if(attrib) {
      dat->SetVal((*iatt).second, attrib->value());
    }
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






















