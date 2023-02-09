
#ifndef DetectorData_h 
#define DetectorData_h

#include <vector>
#include <algorithm>

template<class U, class S> class DetectorData {

  private:

    //unit memory representation
    class UnitAttrBase {
    public:
      virtual void CreateOutput(std::string base_nam, TTree* tree) = 0;
      virtual void ClearEvent() = 0;
      virtual void Write() = 0;
      virtual void ConnectInput(std::string base_nam, TTree* tree) = 0;
      virtual unsigned long GetN() = 0;
      virtual void LoadVal(unsigned long i) = 0;
    };

    std::vector<U> fUnitsRead; // unit container for reading from input tree 

  protected:

    //data interface for derived specific implementation

    U fUnitIO; // unit object for input/output operations
    S fStorage; // container holding the unit objects
    std::vector<UnitAttrBase*> fUnitAttr; // unit attributes in its memory representation

    //unit attribute in its memory representation
    template<typename T> class UnitAttr: public UnitAttrBase {
      public:
        UnitAttr(std::string n, T& v): attr_nam(n), val(v) {} // constructor with attribute name and value reference
        void CreateOutput(std::string base_nam, TTree *tree) {
          //create the vector and tree branch from provided base name and attribute name
          vec = new std::vector<T>();
          tree->Branch((base_nam+attr_nam).c_str(), vec);
        }
        void ClearEvent() { vec->clear(); } //clear the vector for next event
        void Write() { vec->push_back(val); } // write the given value to the vector with attribute values
        void ConnectInput(std::string base_nam, TTree *tree) {
          //connect the vector with attribute values to the input tree
          vec = 0x0;
          tree->SetBranchAddress((base_nam+attr_nam).c_str(), &vec);
        }
        unsigned long GetN() { return vec->size(); } // number of attribute values for a given event
        void LoadVal(unsigned long i) { val = vec->at(i); } // load the value at the given position via the reference
      private:
        std::string attr_nam; // attribute name
        T& val; // input/output value
        std::vector<T> *vec; // container for attribute values
    };//UnitAttr

    //_____________________________________________________________________________
    template<typename T> void AddUnitAttr(std::string attr_nam, T& ref) {

      //add Unit attribute of type T with its name attr_nam and reference to data value ref

      fUnitAttr.push_back( new UnitAttr<T>(attr_nam, ref) );

    }//AddUnitAttr

  public:

    //_____________________________________________________________________________
    void CreateOutput(std::string base_nam, TTree *tree) {

      //make the output for the Unit

      //attribute representation loop
      for(UnitAttrBase *i: fUnitAttr) {
        i->CreateOutput(base_nam, tree);
      }//attribute representation loop

    }//CreateOutput

    //_____________________________________________________________________________
    void ClearEvent() {

      //clear run-time Unit objects and memory representation

      fStorage.clear();
      std::for_each(fUnitAttr.begin(), fUnitAttr.end(), std::mem_fun( &UnitAttrBase::ClearEvent ));

    }//ClearEvent

    //_____________________________________________________________________________
    void FinishEvent() {

      //G4cout << "DetectorData::FinishEvent" << G4endl;

      //Unit loop
      for(U i: fStorage) {

        //set the IO member
        fUnitIO = i;

        //write the unit attributes to the tree
        std::for_each(fUnitAttr.begin(), fUnitAttr.end(), std::mem_fun( &UnitAttrBase::Write ));
      }//Unit loop

    }//FinishEvent

    //_____________________________________________________________________________
    void ConnectInput(std::string base_nam, TTree *tree) {

      //connect input for Unit attributes from the tree

      //attribute representation loop
      for(UnitAttrBase *i: fUnitAttr) {
        i->ConnectInput(base_nam, tree);
      }//attribute representation loop

    }//ConnectInput

    //_____________________________________________________________________________
    void LoadInput() {

      //clear the run-time units for the event
      fUnitsRead.clear();

      //unit object loop
      for(unsigned long iu = 0; iu < fUnitAttr.front()->GetN(); iu++) {

        //attribute loop for the unit
        for(UnitAttrBase *i: fUnitAttr) {
          i->LoadVal(iu);
        }//attribute loop for the unit

        //make the unit from the loaded attributes
        fUnitsRead.push_back( U(fUnitIO) );

      }//unit object loop

    }//LoadInput

    unsigned long GetN() { return fUnitsRead.size(); }

    U GetUnit(unsigned long i) { return fUnitsRead[i]; }

};//DetectorData

#endif



















