
#set path to lmon executable in build

set build="build"
set Q2rec="macro/Q2rec"

setenv PATH ${PATH}:"`pwd`/$build":"`pwd`/$Q2rec"

setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:"`pwd`/$build"

