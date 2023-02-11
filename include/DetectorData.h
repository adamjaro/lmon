
//_____________________________________________________________________________
//
// Base class to write and read a data collection to a TTree.
//
// Objects of class Unit U holding the data are stored in Storage S container
// for writing to the tree. Derived class representing the collection
// of the Unit objects implements method to fill the Storage.
//
// The Unit objects are loaded and read from the current tree entry
// by LoadInput, GetN and GetUnit functions defined directly here.
//
//_____________________________________________________________________________

#ifndef DetectorData_h 
#define DetectorData_h

//C++
#include <vector>
#include <algorithm>
#include <string>

//ROOT
#include "TTree.h"

template<class U, class S=std::vector<U>> class DetectorData {

  public:

    //_____________________________________________________________________________
    void CreateOutput(std::string base_nam, TTree *tree) {

      //make the output for the Unit storage

      //attribute representation loop
      for(UnitAttrBase *i: fUnitAttr) i->CreateOutput(base_nam, tree);

    }//CreateOutput

    //_____________________________________________________________________________
    void ClearEvent() {

      //clear run-time Unit objects and memory representation

      fStorage.clear();
      std::for_each(fUnitAttr.begin(), fUnitAttr.end(), std::mem_fun( &UnitAttrBase::ClearEvent ));

    }//ClearEvent

    //_____________________________________________________________________________
    void FinishEvent() {

      //write all the Unit objects in the Storage to the tree

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
      for(UnitAttrBase *i: fUnitAttr) i->ConnectInput(base_nam, tree);

    }//ConnectInput

    //_____________________________________________________________________________
    void LoadInput() {

      //load all Unit objects at a given tree entry

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

    unsigned long GetN() { return fUnitsRead.size(); } // get number of units read at a current tree entry
    U& GetUnit(unsigned long i) { return fUnitsRead[i]; } // get unit object at position i

  protected:

    //_____________________________________________________________________________
    template<typename T> void AddUnitAttr(std::string attr_nam, T& ref) {

      //add Unit attribute of type T with its name attr_nam and reference to data value ref

      fUnitAttr.push_back( new UnitAttr<T>(attr_nam, ref) );

    }//AddUnitAttr

    //data interface for derived specific implementation
    U fUnitIO; // unit object for input/output operations
    S fStorage; // container holding the unit objects

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

    std::vector<UnitAttrBase*> fUnitAttr; // unit attributes in its memory representation

    std::vector<U> fUnitsRead; // unit container for reading from input tree

};//DetectorData

#endif



















