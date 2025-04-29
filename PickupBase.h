#pragma once
#include "Map.h"
#include <string>
#include <utility>

enum pickup_type { RANDOM_PICKUP, HEALTH_POTION, POWER_POTION, SPEED_POTION };

class PickupBase {
protected:
    Map &map;
    int pos_x, pos_y;
    char image = 15;
    bool picked = false;

public:
    PickupBase(Map &map);
    virtual ~PickupBase() = default;

    virtual std::string description() const = 0;
    virtual pickup_type get_type() const = 0;

    bool set_pos(int x, int y);
    std::pair<int, int> get_pos() const;
    void pickup();
    bool is_picked() const;
};