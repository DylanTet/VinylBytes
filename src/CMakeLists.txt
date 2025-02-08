project(vinyl_bytes)

include_directories(${PROJECT_SOURCE_DIR}/include)

add_subdirectory(rfid_scanner)

add_executable(main main.cpp)

