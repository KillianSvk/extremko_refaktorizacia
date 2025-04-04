#include <map>

#include "Pawn.h"
#include "Pickup.h"

#pragma once

enum direction {LEFT, RIGHT, UP, DOWN};

class Player : public Pawn{
private:
    int movement_left;
    int current_damage;
    std::map<int, int> inventory;

public:
    Player(Map &map);
    Player(Map &map, int pos_x, int pos_y);

    int get_movement_left() const {return movement_left;};
    void set_movement_left(int _movement_left) {movement_left = _movement_left;};
    int get_damage() const override {return current_damage;}
    void reset_movement(){movement_left = movement_speed;};
    void reset_damage(){current_damage = damage;};
    std::string get_items ();
    void set_items (int num_health, int num_speed, int num_power);
    void print_items() const;

    bool move(direction direction);
    void use_movement() {movement_left--;}
    bool pickup(Pickup &pickup);
    bool use_item(pickup_type type) override;

};



