
//_____________________________________________________________________________
//
// Graphite filter against synchrotron radiation for luminosity photon detector
//
//_____________________________________________________________________________

//Geant headers
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4SystemOfUnits.hh"
#include "G4PVPlacement.hh"
#include "G4VisAttributes.hh"

//local classes
#include "GraphiteFilter.h"
#include "GeoParser.h"

//_____________________________________________________________________________
GraphiteFilter::GraphiteFilter(const G4String& nam, GeoParser *geo, G4LogicalVolume *top) {

  G4cout << "  GraphiteFilter: " << nam << G4endl;

  //front face position along z
  G4double zpos = geo->GetD(nam, "zpos") * mm;

  //length along z
  G4double zsiz = geo->GetD(nam, "zsiz") * mm;

  //size in x and y, mm
  G4double xsiz = 200;
  G4double ysiz = 200;
  geo->GetOptD(nam, "xsiz", xsiz);
  geo->GetOptD(nam, "ysiz", ysiz);

  //box shape for the filter
  G4Box *shape = new G4Box(nam, (xsiz*mm)/2., (ysiz*mm)/2., zsiz/2.);

  //graphite material
  G4Material *mat = G4NistManager::Instance()->FindOrBuildMaterial("G4_GRAPHITE");

  //logical volume
  G4LogicalVolume *vol = new G4LogicalVolume(shape, mat, nam);

  //visibility
  G4VisAttributes *vis = new G4VisAttributes();
  vis->SetColor(0.8, 0.8, 0.4); // dark yellow
  vis->SetLineWidth(1); // 2
  vol->SetVisAttributes(vis);

  //put the filter to the top volume
  new G4PVPlacement(0, G4ThreeVector(0, 0, zpos-zsiz/2), vol, nam, top, false, 0);

}//GraphiteFilter























