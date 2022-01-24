
//_____________________________________________________________________________
//
// Visibility configuration from input string
//
//_____________________________________________________________________________

//Boost
#include <boost/tokenizer.hpp>

//Geant
#include "G4VisAttributes.hh"

//local classes
#include "ColorDecoder.h"
#include "GeoParser.h"

using namespace std;
using namespace boost;

//_____________________________________________________________________________
G4VisAttributes *ColorDecoder::MakeVis(GeoParser *geo, G4String nam, G4String par) {

  G4String col(fCol); // red:green:blue:alpha 
  geo->GetOptS(nam, par, col);

  char_separator<char> sep(":");
  tokenizer< char_separator<char> > clin(col, sep);
  tokenizer< char_separator<char> >::iterator it = clin.begin();

  stringstream st;
  for(int i=0; i<4; i++) {
    st << *(it++) << " ";
  }

  G4double red=0, green=0, blue=0, alpha=0;
  st >> red >> green >> blue >> alpha;

  G4VisAttributes *vis = new G4VisAttributes();
  if(alpha < 1.1) {
    vis->SetColor(red, green, blue, alpha);
    vis->SetForceSolid(true);
  } else {
    vis->SetColor(red, green, blue);
    vis->SetForceAuxEdgeVisible(true);
  }

  return vis;

}//MakeVis

