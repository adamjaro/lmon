
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(rcalc)

#local library
set (LIB rcalc)

#sources
file(GLOB SRC ${PROJECT_SOURCE_DIR}/src/*.cxx)
include_directories(${PROJECT_SOURCE_DIR}/include)

#ROOT
find_package(ROOT REQUIRED COMPONENTS Core EG Hist Physics RIO Tree MathCore)
include(${ROOT_USE_FILE})

#SWIG
find_package(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

FIND_PACKAGE(PythonLibs)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})

SET_SOURCE_FILES_PROPERTIES(rcalc.i PROPERTIES CPLUSPLUS ON)

#build the library
SWIG_ADD_MODULE(${LIB} python rcalc.i ${SRC})
SWIG_LINK_LIBRARIES(${LIB} ${PYTHON_LIBRARIES} ${ROOT_LIBRARIES})

