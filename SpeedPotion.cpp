#include "SpeedPotion.h"
#include "Player.h"

SpeedPotion::SpeedPotion(Map &map) : PickupBase(map) {}

std::string SpeedPotion::description() const {
    return "SPEED POTION (s): gives +1 max movement speed";
}

pickup_type SpeedPotion::get_type() const {
    return SPEED_POTION;
}

void SpeedPotion::apply_effect(Player &player) {
    player.set_movement_speed(player.get_movement_speed() + 1);
   }
