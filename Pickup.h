#pragma once
#include "PickupBase.h"
#include "HealthPotion.h"
#include "PowerPotion.h"
#include "SpeedPotion.h"
#include <memory>
#include <stdexcept>

class Pickup {
private:
    std::unique_ptr<PickupBase> pickup_impl;

    static std::unique_ptr<PickupBase> create_pickup(Map &map, pickup_type type);

public:
    Pickup(Map &map, pickup_type type);
    Pickup(Map &map, pickup_type type, int pos_x, int pos_y);

    pickup_type get_type() const;
    std::string description() const;
    bool set_pos(int x, int y);
    std::pair<int, int> get_pos() const;
    void pickup();
    bool is_picked() const;
};