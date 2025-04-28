#include <iostream>

#include "Map.h"
#include "Pickup.h"

#pragma once

class Pawn {
protected:
    Map &map;
    int pos_x = 0, pos_y = 0;
    int max_health = 1,health = 1;
    int damage = 1;
    int movement_speed = 1;
    char image = 'P';

public:
    explicit Pawn(Map &map);
    Pawn(Map &map, int pos_x, int pos_y, int max_health, int damage, int movement_speed, char image);

    int get_pos_x() const {return pos_x;}
    int get_pos_y() const {return pos_y;}
    bool set_pos(int x, int y);
    int get_max_health() const {return max_health;}
    void set_max_health(int _max_health)  {max_health = _max_health;}
    int get_health() const {return health;}
    void set_health(int _health)  {health = _health;}

    virtual int get_damage() const {return damage;}
    int get_movement_speed() const {return movement_speed;}
    void set_movement_speed (int _movement_speed) {movement_speed = _movement_speed;}
    char get_image() const {return image;}

    void move_towards(int pos_x, int pos_y);
    bool lose_health(int dmg);

    virtual bool use_item (pickup_type type);
};

