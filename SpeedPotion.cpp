#include "SpeedPotion.h"

SpeedPotion::SpeedPotion(Map &map) : PickupBase(map) {}

std::string SpeedPotion::description() const {
    return "SPEED POTION (s): gives +1 max movement speed";
}

pickup_type SpeedPotion::get_type() const {
    return SPEED_POTION;
}