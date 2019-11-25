
//C++ headers
#include <iostream>

//Geant headers
#include "G4UIExecutive.hh"
#include "Randomize.hh"
#include "G4RunManager.hh"
#include "G4VisExecutive.hh"
#include "G4UImanager.hh"
#include "FTFP_BERT.hh"
#include "G4OpticalPhysics.hh"

//local headers
#include "DetectorConstruction.h"
#include "ActionInitialization.h"

//_____________________________________________________________________________
int main(int argc, char* argv[]) {

  //interactive or batch execution
  G4String macro;
  if( argc == 2 ) {
    macro = argv[1];
  }

  //UI session
  G4String session;
  G4UIExecutive *ui = 0x0;
  if( !macro.size() ) {
    ui = new G4UIExecutive(argc, argv, session);
  }

  //random engine
  G4Random::setTheEngine(new CLHEP::RanecuEngine);

  //default run manager
  G4RunManager *runManager = new G4RunManager;

  //detector construction
  runManager->SetUserInitialization(new DetectorConstruction);

  //physics
  FTFP_BERT *physicsList = new FTFP_BERT;
  //G4OpticalPhysics *opt = new G4OpticalPhysics();
  //physicsList->RegisterPhysics(opt); // uncomment to turn optics on
  runManager->SetUserInitialization(physicsList);

  //action
  runManager->SetUserInitialization(new ActionInitialization);

  //visualization
  G4VisExecutive *visManager = new G4VisExecutive;
  visManager->Initialize();

  //user interface manager
  G4UImanager *UImanager = G4UImanager::GetUIpointer();

  //UI session for interactive or batch mode
  if ( macro.size() > 0 ) {
    // batch mode
    G4String command = "/control/execute ";
    UImanager->ApplyCommand(command+macro);
  } else {
    //interactive
    UImanager->ApplyCommand("/control/execute init_vis.mac");
    if (ui->IsGUI()) {
      UImanager->ApplyCommand("/control/execute gui.mac");
    }
    ui->SessionStart();
    delete ui;
  }

  //job termination
  delete visManager;
  delete runManager;

  return 0;

}//main





























