#include "HealthPotion.h"
#include "Player.h"

HealthPotion::HealthPotion(Map &map) : PickupBase(map) {}

std::string HealthPotion::description() const {
    return "HEALTH POTION (h): heals 15 HP";
}

pickup_type HealthPotion::get_type() const {
    return HEALTH_POTION;
}

void HealthPotion::apply_effect(Player &player) {
    player.set_health(player.get_health() + 15);
    if (player.get_health() > player.get_max_health()) {
        player.set_health(player.get_max_health());
    }

}
