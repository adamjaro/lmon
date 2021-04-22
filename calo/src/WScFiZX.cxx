
//_____________________________________________________________________________
//
// W/ScFi originally created by Zhiwan Xu (UCLA)
//
//_____________________________________________________________________________

//C++
#include "math.h"

//ROOT
#include "TTree.h"

//Geant
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4Step.hh"
#include "G4VisAttributes.hh"
#include "G4PVReplica.hh"
#include "CLHEP/Vector/RotationY.h"

//local classes
#include "WScFiZX.h"
#include "DetUtils.h"
#include "GeoParser.h"

//_____________________________________________________________________________
WScFiZX::WScFiZX(const G4String& nam, GeoParser *, G4LogicalVolume *top) : Detector(),
  G4VSensitiveDetector(nam), fNam(nam), fCheckOverlaps(false) {

  G4cout << "  WScFiZX: " << fNam << G4endl;

  fBirksCoefficient = 0.126*mm/MeV;

  G4double calorSizeXY  = 600.*mm;
  G4double calorEMZ=17.0*cm;

  const double offset=0.5;//in mm
  const double dist=1.0;
  const double tot_len=600.0;
  const double h=0.5*sqrt(3)*dist;

  const int nx1=int((tot_len-2*offset)/(dist/2))+1;
  const int ny1=int((tot_len-offset)/(2*h))+1;
  const int ny2=int((tot_len-offset-h)/(2*h))+1;

  const double x0=-((tot_len/2.0)-offset);
  const double y01=((tot_len/2.0)-offset);
  const double y02=((tot_len/2.0)-offset-h);

  G4double vrot = 10.0*degree;
  G4double hrot = 1.0*degree;

  //G4Material* defaultMaterial = G4Material::GetMaterial("Galactic");
  //G4Material* gapMaterial2 =G4Material::GetMaterial("G4_POLYSTYRENE");
  G4Material* defaultMaterial = G4NistManager::Instance()->FindOrBuildMaterial("G4_Galactic");
  G4Material* gapMaterial2 = G4NistManager::Instance()->FindOrBuildMaterial("G4_POLYSTYRENE");
  G4Material* EMCal_abs_mat=new G4Material("EMCal_fiber_mat",12.4*g/cm3,2);
  G4double a=183.85*g/mole;
  G4Element* elW=new G4Element("Tungsten","W",74.,a);
  EMCal_abs_mat->AddElement(elW,96.0*perCent);
  EMCal_abs_mat->AddMaterial(gapMaterial2,4.0*perCent);


  //EM
  G4LogicalVolume* calorEM;
  G4VSolid* calorimeterEM = new G4Box("CalorimeterEM_", calorSizeXY/2, calorSizeXY/2, calorEMZ/2);
  calorEM=new G4LogicalVolume(calorimeterEM,defaultMaterial, fNam+"_CalorEM");
  G4RotationMatrix *rX = new G4RotationMatrix(CLHEP::HepRotationX(vrot)); 
  G4RotationMatrix *rY = new G4RotationMatrix(CLHEP::HepRotationY(hrot)); 
  G4RotationMatrix *rXY = new G4RotationMatrix((*rX) * (*rY));
  new G4PVPlacement(rXY,G4ThreeVector(0.,0.,calorEMZ/2),calorEM, fNam+"_CalorimeterEM", top,false,0,fCheckOverlaps);
    
  //absorber
  G4LogicalVolume* absorberEMLV;
  G4VSolid* absorberEM = new G4Box(fNam+"_AbsoEM_solid",            // its name
                                     calorSizeXY/2, calorSizeXY/2, calorEMZ/2); // its size
  absorberEMLV = new G4LogicalVolume(absorberEM,EMCal_abs_mat, fNam+"_AbsoEM");
  new G4PVPlacement(0,G4ThreeVector(0.,0.,0.),absorberEMLV, fNam+"_AbsoEM_p",calorEM,false,0,fCheckOverlaps);
    
  G4VSolid* gapEM = new G4Tubs(fNam+"_GapEM",             // its name
                               0.0, 0.235*mm, calorEMZ/2,0.0,360.0 * deg); // its size//0.0 * deg, 360.0 * deg
    
  //Fibers
  G4LogicalVolume* gapEMLV;
  gapEMLV = new G4LogicalVolume(gapEM,gapMaterial2, fNam);
  int copynono=0;
  double step_x=(dist/2.0)*mm;
  double step_y=(2.0*h)*mm;
  //G4cout<<"Nx: "<<nx1<<" Ny1: "<<ny1<<" Ny2: "<<ny2<<" step_x: "<<step_x<<" step_y: "<<step_y<<" x0: "<<x0<<" y01: "<<y01<<" y02: "<<y02<<G4endl;

  for(int i=0;i<nx1;i++){
    G4double pos_x=x0*mm+i*step_x;
    G4double pos_y=0.0;
    //if(i==(nFibAr-1)) continue;
    // if(i%2==0) pos_x=(-29.95+i*(0.05))*cm;
    // if(i%2!=0) pos_x=(-29.9+i*(0.05))*cm;
    // pos_x=(-29.95+i*(0.1))*cm;
    int jend=(i%2==0) ? ny1 : ny2;
    for(int j=0;j<jend;j++){
            
            
      if(i%2==0) pos_y=y01*mm-j*step_y;
      if(i%2!=0) pos_y=y02*mm-j*step_y;
      new G4PVPlacement(0,G4ThreeVector(pos_x,pos_y, 0.),gapEMLV,fNam+"_EMGapPhysical",absorberEMLV,false,copynono,fCheckOverlaps);
      //new G4PVPlacement(0,G4ThreeVector(pos_x,pos_y, 0.),gapEMLV,"EMGapPhysical",absorberEMLV,0,copynono);//first try
      copynono++;
      //G4cout<<"Point # "<<copynono<<" x: "<<pos_x<<" y: "<<pos_y<<G4endl;

    }
  }

  G4VisAttributes* calorEMvis= new G4VisAttributes(G4Colour(1,0,1));//magenta calorimeter
  G4VisAttributes* gapEMvis= new G4VisAttributes(G4Colour(1,1,0));//yellow gap
  G4VisAttributes* absEMvis= new G4VisAttributes(G4Colour(0,1,1));//cyan absorber
    
  calorEMvis->SetVisibility(true);
  calorEMvis->SetForceWireframe (true);
  gapEMvis->SetVisibility(false);
  gapEMvis->SetForceSolid (true);
  absEMvis->SetVisibility(true);
  absEMvis->SetForceWireframe(true);
  calorEM->SetVisAttributes(calorEMvis);
  gapEMLV->SetVisAttributes(gapEMvis);
  absorberEMLV->SetVisAttributes(absEMvis);


}//WScFiZX

//_____________________________________________________________________________
G4bool WScFiZX::ProcessHits(G4Step *step, G4TouchableHistory*) {

  //deposited energy in step (GeV)
  fEdep += BirksCorrectedEnergyDeposit(step);

  return true;

}//ProcessHits

//_____________________________________________________________________________
G4double WScFiZX::BirksCorrectedEnergyDeposit(G4Step *step) {

  //deposited energy in step, MeV
  G4double edep_step = step->GetTotalEnergyDeposit()/MeV;

  //Birks attenuation
  G4double step_length = step->GetStepLength()*mm;
  G4double particle_charge = step->GetTrack()->GetDefinition()->GetPDGCharge();

  //value of fBirksCoefficient is in mm/MeV
  G4double edep = edep_step;
  if( std::abs(edep_step*step_length*particle_charge) > 1e-12 ) {

    edep = edep_step/(1. + fBirksCoefficient*edep_step/step_length);
  }

  return edep/GeV; //to GeV

}//BirksCorrectedEnergyDeposit

//_____________________________________________________________________________
void WScFiZX::ClearEvent() {

  fEdep = 0;

}//ClearEvent

//_____________________________________________________________________________
void WScFiZX::CreateOutput(TTree *tree) {

  DetUtils u(fNam, tree);

  u.AddBranch("_edep", &fEdep, "D");

}//CreateOutput













