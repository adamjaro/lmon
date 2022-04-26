
#set path to lmon executable in build

build="build"

export PATH=$PATH:`pwd`/$build:`pwd`/$build"/analysis":`pwd`"/analysis_tasks/run_macros"

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`/$build:`pwd`/$build"/analysis_tasks"

