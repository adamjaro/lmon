
#set path to lmon executable in build

set build="build"

setenv PATH ${PATH}:"`pwd`/$build":"`pwd`/$build/analysis":"`pwd`/analysis_tasks/run_macros"

setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:"`pwd`/$build":"`pwd`/$build/analysis_tasks"

