#include "PowerPotion.h"

PowerPotion::PowerPotion(Map &map) : PickupBase(map) {}

std::string PowerPotion::description() const {
    return "POWER POTION (p): gives +2 attack for one fight";
}

pickup_type PowerPotion::get_type() const {
    return POWER_POTION;
}