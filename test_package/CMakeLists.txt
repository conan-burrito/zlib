cmake_minimum_required(VERSION 3.6)
project(PackageTest VERSION 1.0.0 LANGUAGES C)

set(CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(ZLIB CONFIG)

add_executable(example example.c)
target_link_libraries(example zlib::zlib)
set_target_properties(example PROPERTIES OUTPUT_NAME "test")
