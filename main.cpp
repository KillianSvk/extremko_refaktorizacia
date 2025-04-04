#include <chrono>
#include <thread>

#include "Game.h"
#include "Map.cpp"
#include "Game.cpp"
#include "Pawn.cpp"
#include "Enemy.cpp"
#include "Player.cpp"
#include "Pickup.cpp"



int main() {

    Game game;
    game.play();

//    game.save();
//    game.load();

    return 0;
};