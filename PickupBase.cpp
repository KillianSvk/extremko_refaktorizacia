#include "PickupBase.h"

PickupBase::PickupBase(Map &map) : map(map), pos_x(std::numeric_limits<int>::min()), pos_y(std::numeric_limits<int>::min()) {}

bool PickupBase::set_pos(int x, int y) {
    if (!map.is_walkable(x, y)) {
        return false;
    }
    pos_x = x;
    pos_y = y;
    map.set_pos(x, y, PICKUP);
    return true;
}

std::pair<int, int> PickupBase::get_pos() const {
    return {pos_x, pos_y};
}

void PickupBase::pickup() {
    picked = true;
}

bool PickupBase::is_picked() const {
    return picked;
}