#include <memory>
#include "Pickup.h"

std::unique_ptr<PickupBase> Pickup::create_pickup(Map &map, pickup_type type) {
    if (type == RANDOM_PICKUP) {
        type = static_cast<pickup_type>(1 + rand() % 3);
    }

    switch (type) {
        case HEALTH_POTION: return std::make_unique<HealthPotion>(map);
        case POWER_POTION: return std::make_unique<PowerPotion>(map);
        case SPEED_POTION: return std::make_unique<SpeedPotion>(map);
        default: throw std::runtime_error("Invalid pickup type");
    }
}

Pickup::Pickup(Map &map, pickup_type type) : pickup_impl(create_pickup(map, type)) {}

Pickup::Pickup(Map &map, pickup_type type, int pos_x, int pos_y) : pickup_impl(create_pickup(map, type)) {
    pickup_impl->set_pos(pos_x, pos_y);
}

pickup_type Pickup::get_type() const {
    return pickup_impl->get_type();
}

std::string Pickup::description() const {
    return pickup_impl->description();
}

bool Pickup::set_pos(int x, int y) {
    return pickup_impl->set_pos(x, y);
}

std::pair<int, int> Pickup::get_pos() const {
    return pickup_impl->get_pos();
}

void Pickup::pickup() {
    pickup_impl->pickup();
}

bool Pickup::is_picked() const {
    return pickup_impl->is_picked();
}