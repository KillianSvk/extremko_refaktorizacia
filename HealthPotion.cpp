#include "HealthPotion.h"

HealthPotion::HealthPotion(Map &map) : PickupBase(map) {}

std::string HealthPotion::description() const {
    return "HEALTH POTION (h): heals 15 HP";
}

pickup_type HealthPotion::get_type() const {
    return HEALTH_POTION;
}