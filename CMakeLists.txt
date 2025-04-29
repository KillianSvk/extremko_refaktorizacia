cmake_minimum_required(VERSION 3.6.2)
project(extremko_refaktorizacia)

set(CMAKE_CXX_STANDARD 17)

find_package(Threads)

set(SOURCE_FILES

        Game.cpp
        Map.cpp
        Pawn.cpp
        Enemy.cpp
        Player.cpp
        Pickup.cpp
        SpeedPotion.cpp
        HealthPotion.cpp
        PickupBase.cpp
        PowerPotion.cpp

        test_game.cpp

        GoogleTest/gtest-death-test.cc
        GoogleTest/gtest-filepath.cc
        GoogleTest/gtest-port.cc
        GoogleTest/gtest-printers.cc
        GoogleTest/gtest-test-part.cc
        GoogleTest/gtest-typed-test.cc
        GoogleTest/gtest.cc
        GoogleTest/gtest_main.cc
)

include_directories(GoogleTest)
add_executable(extremko_refaktorizacia ${SOURCE_FILES})
target_link_libraries(extremko_refaktorizacia ${CMAKE_THREAD_LIBS_INIT})