
#set path to lmon executable in build

build="build"
Q2rec="macro/Q2rec"

export PATH=$PATH:`pwd`/$build:`pwd`/$Q2rec

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`/$build

