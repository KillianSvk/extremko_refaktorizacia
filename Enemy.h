#include "Pawn.h"
#include "Pickup.h"

#pragma once

enum enemy_type {RANDOM_ENEMY, WARRIOR, MAGE};

class Enemy : public Pawn {
private:
    bool dead = false;
    void generate_enemy(enemy_type type);

public:
    Enemy(Map &map);
    Enemy(Map &map, enemy_type type);
    Enemy(Map &map, enemy_type type, int pos_x, int pos_y);

    void die(){dead = true;}
    bool is_dead() const {return dead;}
};

