# workspace "{{PROJECT_NAME}}"
cmake_minimum_required(VERSION 3.16)

project({{PROJECT_NAME}} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(OUTPUT_DIR "${CMAKE_BUILD_TYPE}_${CMAKE_SYSTEM_NAME}_${CMAKE_SYSTEM_PROCESSOR}")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin/${OUTPUT_DIR}") # static lib
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin/${OUTPUT_DIR}") # dynamic lib
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin/${OUTPUT_DIR}") # execution

# project "{{PROJECT_NAME}}"
file(GLOB_RECURSE PROJECT_SRC
    "src/**.cpp"
    "src/**.h"
    "src/**.hpp"
)

if(PROJECT_SRC)
    add_executable({{PROJECT_NAME}} ${PROJECT_SRC})
    target_include_directories({{PROJECT_NAME}} PRIVATE "src")
    target_precompile_headers({{PROJECT_NAME}} PRIVATE "src/pch.h")
else()
    message(STATUS "Not found any file . Skip")
endif()
