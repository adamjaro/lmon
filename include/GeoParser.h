
#ifndef GeoParser_h
#define GeoParser_h

#include <map>
#include <boost/tokenizer.hpp>

class GeoParser {

  public:

    GeoParser() {}

    //load geometry input
    void LoadInput(G4String input);

    //detectors and elements
    unsigned int GetN() const {return fDet.size();}
    const G4String& GetType(unsigned int i) const {return fDet[i].first;}
    const G4String& GetName(unsigned int i) const {return fDet[i].second;}

    //top volume name
    G4String GetTopName();

    //geometry parameters
    const G4String& GetS(G4String name, G4String par);
    G4double GetD(G4String name, G4String par);
    G4int GetI(G4String name, G4String par);
    G4bool GetB(G4String name, G4String par);

    void GetOptD(G4String name, G4String par, G4double& val);
    void GetOptI(G4String name, G4String par, G4int& val);
    void GetOptB(G4String name, G4String par, G4bool& val);

  private:

    typedef boost::tokenizer< boost::char_separator<char> >::iterator token_it;

    void Include(token_it &it); // another geometry input
    void AddNew(token_it &it); // new detector or element
    void AddPar(token_it &it); // new geometry parameter

    template<typename par_type> par_type GetPar(G4String name, G4String par);
    template<typename par_type> void GetOptPar(G4String name, G4String par, par_type& val);

    std::vector< std::pair<G4String, G4String> > fDet; // detectors and components
    std::map<G4String, G4String> fPar; // geometry parameters

};

#endif


