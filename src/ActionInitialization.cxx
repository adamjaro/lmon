
//_____________________________________________________________________________
//
// standard action initialization,
// selects the event generator
//_____________________________________________________________________________

//local headers
#include "ActionInitialization.h"
#include "GeneratorAction.h"
#include "EventAction.h"
#include "LgenReader.h"
#include "RunAction.h"
#include "UniformGen.h"

//_____________________________________________________________________________
void ActionInitialization::Build() const {

  //select the generator
  //SetUserAction(new GeneratorAction);
  SetUserAction(new LgenReader);
  //SetUserAction(new UniformGen);

  SetUserAction(new EventAction);
  SetUserAction(new RunAction);

}//build

