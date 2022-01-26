
#set path to lmon executable in build

set build="build"

setenv PATH ${PATH}:"`pwd`/$build":"`pwd`/$build/analysis"

setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:"`pwd`/$build"

