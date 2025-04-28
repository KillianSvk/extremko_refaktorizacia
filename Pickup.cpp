
#include "Pickup.h"

Pickup::Pickup(Map &map, pickup_type _type) : map(map), type(_type) {
    generate_pickup(_type);
    pos_x = NULL; pos_y = NULL;
}

Pickup::Pickup(Map &map,int pos_x, int pos_y) : map(map), pos_x(pos_x), pos_y(pos_y) {
    generate_pickup(RANDOM_PICKUP);
    set_pos(pos_x, pos_y);
}


Pickup::Pickup(Map &map, pickup_type _type, int pos_x, int pos_y) : map(map), type(_type), pos_x(pos_x), pos_y(pos_y) {
    set_pos(pos_x, pos_y);
}

void Pickup::generate_pickup(pickup_type _type) {
    int chance;
    if (_type == RANDOM_PICKUP) {
        srand(time(nullptr));
        chance = rand() % 3 + 1;
    } else {
        chance = _type;
    }

    switch (chance) {
        case 1:
            type = HEALTH_POTION;
            break;

        case 2:
            type = POWER_POTION;
            break;

        case 3:
            type = SPEED_POTION;
            break;

        default:
//            type = HEALTH_POTION;
            break;
    }
}

bool Pickup::set_pos(int x, int y) {
    if (! map.is_walkable(x,y)) {
        return false;
    }

    pos_x = x;
    pos_y = y;
    map.set_pos(x, y, PICKUP);
    return true;
}

std::string Pickup::description() const {
    if (type == HEALTH_POTION) {
        return "HEALTH POTION (h): heals 15 HP";
    }
    if (type == POWER_POTION) {
        return "POWER POTION (p): gives +2 attack for one fight";
    }
    if (type == SPEED_POTION) {
        return "SPEED POTION (s): gives +1 max movement speed";
    }

}
