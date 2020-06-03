
#ifndef GraphiteFilter_h
#define GraphiteFilter_h

// graphite filter for luminosity photon detector

class GeoParser;

class GraphiteFilter {

  public:

    GraphiteFilter(const G4String&, GeoParser *geo, G4LogicalVolume*);

};

#endif

