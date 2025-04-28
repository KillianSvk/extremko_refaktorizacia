#include "Pawn.h"

Pawn::Pawn(Map &map) : map(map) {
}

Pawn::Pawn(Map &map, int pos_x, int pos_y, int max_health, int damage, int movement_speed, char image)
    :  map(map), pos_x(pos_x), pos_y(pos_y), max_health(max_health), health(max_health), damage(damage), movement_speed(movement_speed), image(image) {
    map.set_pos(pos_x, pos_y, image);
}

void Pawn::move_towards(int to_pos_x, int to_pos_y) {
    std::vector<int> path = map.find_path(pos_x, pos_y, to_pos_x, to_pos_y);

    if (path.size() >= movement_speed * 2) {
        set_pos(path[(movement_speed - 1) * 2], path[(movement_speed - 1) * 2 + 1]);

    }else if (not path.empty()){
        set_pos(path[path.size() - 2], path[path.size() - 1]);
    }
}

bool Pawn::set_pos(int x, int y) {
    if (! map.is_walkable(x,y)) {
        return false;
    }

    map.set_pos(pos_x, pos_y, EMPTY);

    pos_x = x;
    pos_y = y;

    map.set_pos(x, y, image);

    return true;
}

bool Pawn::lose_health(int dmg) {
    health -= dmg;

    if (health <= 0){
        return true;
    }

    return false;
}

bool Pawn::use_item(pickup_type type) {
    if (type == HEALTH_POTION) {
        health += 15;
        if (health > max_health) {
            health = max_health;
        }
        return true;
    }

    if (type == POWER_POTION) {
        damage += 2;
        return true;
    }

    if (type == SPEED_POTION) {
        movement_speed++;
        return true;
    }

    return false;
}
