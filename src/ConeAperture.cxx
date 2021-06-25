
//_____________________________________________________________________________
//
// conical aperture which absorbs all particles hitting its volume,
// no secondaries are created from absorbed particles
//_____________________________________________________________________________

//ROOT
#include "TMath.h"

//Geant
#include "G4Cons.hh"
#include "G4LogicalVolume.hh"
#include "G4SystemOfUnits.hh"
#include "G4NistManager.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"
#include "G4Transform3D.hh"
#include "G4RotationMatrix.hh"

//local classes
#include "GeoParser.h"
#include "ConeAperture.h"

//_____________________________________________________________________________
ConeAperture::ConeAperture(G4String nam, GeoParser *geo, G4LogicalVolume *top):
    Detector(), G4VSensitiveDetector(nam), fNam(nam) {

  G4cout << "  ConeAperture: " << fNam << G4endl;

  //front face of the cone along z, mm
  G4double zpos = geo->GetD(fNam, "zpos") * mm;

  //front face in x, mm
  G4double xpos = 0;
  geo->GetOptD(fNam, "xpos", xpos);

  //cone length
  G4double length = 1*mm;
  geo->GetOptD(fNam, "length", length, GeoParser::Unit(mm));
  //length from z2
  G4double z2;
  if( geo->GetOptD(fNam, "z2", z2, GeoParser::Unit(mm)) ) {
    length = TMath::Abs(z2 - zpos);
  }

  //cone inner radii closer to the IP (r1), further from the IP (r2)
  G4double r1 = 1*mm, r2 = 1*mm;
  geo->GetOptD(fNam, "r1", r1, GeoParser::Unit(mm));
  geo->GetOptD(fNam, "r2", r2, GeoParser::Unit(mm));
  //radii from diameters
  G4double d1, d2;
  if( geo->GetOptD(fNam, "d1", d1, GeoParser::Unit(mm)) ) {
    r1 = d1/2;
  }
  if( geo->GetOptD(fNam, "d2", d2, GeoParser::Unit(mm)) ) {
    r2 = d2/2;
  }
  G4cout << "    r1: " << r1 << G4endl;
  G4cout << "    r2: " << r2 << G4endl;

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

  //aperture vessel in top module
  G4double angle = 0; // rotation in x along the y axis, rad
  geo->GetOptD(fNam, "angle", angle);
  G4RotationMatrix rot_y(G4ThreeVector(0, 1, 0), angle*rad); //is typedef to CLHEP::HepRotation

  //center position
  xpos = xpos -(length/2)*TMath::Tan(angle);
  G4ThreeVector pos(xpos, 0, zpos-length/2.);

  //placement with rotation and center position
  G4Transform3D transform(rot_y, pos); // is HepGeom::Transform3D

  //put the cone to the top volume
  new G4PVPlacement(transform, vol, fNam, top, false, 0);

}//ConeAperture

//_____________________________________________________________________________
G4bool ConeAperture::ProcessHits(G4Step *step, G4TouchableHistory*) {

  if(fIsTransparent) return true;

  //remove the track entering the cone aperture vessel
  G4Track *track = step->GetTrack();
  track->SetTrackStatus(fKillTrackAndSecondaries);

  return true;

}//ProcessHits
















