#include <random>
#include <ctime>

#include "Map.h"

#pragma once

enum pickup_type {RANDOM_PICKUP, HEALTH_POTION, POWER_POTION, SPEED_POTION};

class Pickup {
private:
    Map &map;
    pickup_type type;
    int pos_x, pos_y;
    char image = 15;
    bool picked = false;

    void generate_pickup(pickup_type _type);

public:
    Pickup(Map &map, pickup_type _type);
    Pickup(Map &map, int pos_x, int pos_y);
    Pickup(Map &map, pickup_type _type, int pos_x, int pos_y);

    [[nodiscard]] pickup_type get_type() const {return type;};
    [[nodiscard]] std::string description() const;
    bool set_pos(int x, int y);
    int get_pos_x() const{return pos_x;}
    int get_pos_y() const{return pos_y;}
    void pickup() {picked = true;}
    bool is_picked() const{return picked;}
};



