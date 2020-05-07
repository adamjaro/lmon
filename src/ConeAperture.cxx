
//_____________________________________________________________________________
//
// conical aperture which absorbs all particles hitting its volume,
// no secondaries are created from absorbed particles
//_____________________________________________________________________________

//Geant
#include "G4Cons.hh"
#include "G4LogicalVolume.hh"
#include "G4SystemOfUnits.hh"
#include "G4NistManager.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"

//local classes
#include "GeoParser.h"
#include "ConeAperture.h"

//_____________________________________________________________________________
ConeAperture::ConeAperture(G4String nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  ConeAperture: " << fNam << G4endl;

  //front face of the cone along z
  G4double zpos = geo->GetD(fNam, "zpos") * mm;

  //cone length
  G4double length = geo->GetD(fNam, "length") * mm;

  //cone radii
  G4double r1 = geo->GetD(fNam, "r1") * mm; // inner radius closer to the IP
  G4double r2 = geo->GetD(fNam, "r2") * mm; // inner radious further from the IP
  G4double dr = geo->GetD(fNam, "dr") * mm; // cone radial thickness

  //conical shape
  G4Cons *shape = new G4Cons(fNam, r2, r2+dr, r1, r1+dr, length/2, 0, 360*deg);

  //transparency for particles
  fIsTransparent = false;
  geo->GetOptB(fNam, "transparent", fIsTransparent);

  //logical volume
  G4String mat_name = "G4_Al";
  if(fIsTransparent) {
    mat_name = "G4_Galactic";
  }
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial(mat_name);
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, fNam);

  //vessel visibility
  G4VisAttributes *vis_vessel = new G4VisAttributes();
  vis_vessel->SetColor(0.5, 0.5, 0.5); // gray
  vis_vessel->SetLineWidth(2);
  vis_vessel->SetForceSolid(true);
  //vis_vessel->SetForceAuxEdgeVisible(true);
  vol->SetVisAttributes(vis_vessel);

  //put the cone to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos-length/2.), vol, fNam, top, false, 0);

}//ConeAperture

//_____________________________________________________________________________
G4bool ConeAperture::ProcessHits(G4Step *step, G4TouchableHistory*) {

  if(fIsTransparent) return true;

  //remove the track entering the cone aperture vessel
  G4Track *track = step->GetTrack();
  track->SetTrackStatus(fKillTrackAndSecondaries);

  return true;

}//ProcessHits
















