
#ifndef GeoParser_h
#define GeoParser_h

#include <map>
#include <boost/tokenizer.hpp>

class GeoParser {

  public:

    GeoParser(G4String input);

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

    //units for optional parameters
    class Unit {
      public:
        Unit(): apply(false), u(0) {}
        Unit(G4double uu): apply(true), u(uu) {}
      private:
        bool apply; // flag to indicate that the unit was provided
        G4double u; // unit for the parameter
        friend class GeoParser;
    };

    //optional parameters
    G4bool GetOptD(G4String name, G4String par, G4double& val, const Unit& un = Unit());
    G4bool GetOptI(G4String name, G4String par, G4int& val);
    G4bool GetOptB(G4String name, G4String par, G4bool& val);
    G4bool GetOptS(G4String name, G4String par, G4String& val);

  private:

    typedef boost::tokenizer< boost::char_separator<char> >::iterator token_it;

    void LoadInput(G4String input); // load geometry input

    void Include(token_it &it); // another geometry input
    void AddNew(token_it &it); // new detector or element
    void AddConst(token_it &it); // new constant
    void AddPar(token_it &it); // new geometry parameter

    G4String Evaluate(G4String val);

    template<typename par_type> par_type GetPar(G4String name, G4String par);
    template<typename par_type> bool GetOptPar(G4String name, G4String par, par_type& val);

    std::vector< std::pair<G4String, G4String> > fDet; // detectors and components
    std::map<G4String, G4String> fPar; // geometry parameters
    std::map<std::string, std::string> fConst; // constants for geometry

    G4String fIncDir; // include directory for geometry inputs

};

#endif


