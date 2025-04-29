#include <iostream>
#include <algorithm>
#include <fstream>
#include <cstdio>
#include <cstring>
#include <sstream>

#include "Map.h"
#include "Enemy.h"
#include "Player.h"
#include "Pickup.h"

#pragma once

class Game{
private:
    int score = 0;
    Map map;

    std::pair<int, int> get_pair_from_str(const std::string&);

    bool player_turn(Player &player, std::vector<Enemy> &enemies, std::vector<Pickup> &pickup);
    bool player_use_item(Player &player);
    bool fight(Player &player, Enemy &enemy);
    void populate_enemies(std::vector<Enemy> &enemies);
    void populate_pickups(std::vector<Pickup> &pickups);


public:
    Game();
    ~Game() = default;

    int get_score() const {return score;}
    Map* get_map() {return &map;}

    void print() const;
    void print_help() const;
    void help_fight() const;
    void gain_score();
    void gain_score(int s);
    void play();
    void populate_map(std::vector<Enemy> &enemies, std::vector<Pickup> &pickups);
    bool save(Player &player, std::vector<Enemy> &enemies, std::vector<Pickup> &pickups);
    bool load(Player &player, std::vector<Enemy> &enemies, std::vector<Pickup> &pickups);
};
