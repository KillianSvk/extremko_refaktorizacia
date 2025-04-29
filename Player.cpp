#include "Player.h"

Player::Player(Map &map) : Pawn(map) {
    image = PLAYER;
    health = max_health = 30;
    movement_left = movement_speed = 4;
    current_damage = damage = 5;

    inventory[HEALTH_POTION] = 0;
    inventory[SPEED_POTION] = 0;
    inventory[POWER_POTION] = 0;
}

Player::Player(Map &map, int pos_x, int pos_y) : Player(map) {

    set_pos(pos_x, pos_y);
}

bool Player::move(direction direction) {
    if (movement_left <= 0) {
        return false;
    }
    // left, right, down, up
    std::vector<std::pair<int, int>> directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

    if (map.is_walkable(pos_x + directions[direction].first, pos_y +directions[direction].second)) {
        set_pos(pos_x + directions[direction].first, pos_y + directions[direction].second);
        movement_left--;
        return true;
    }

    std::cout << "Can't go there, try another way" << '\n';
    return false;
}

bool Player::pickup(Pickup &pickup) {
    if (pickup.is_picked()) {
        return false;
    }

    inventory[pickup.get_type()]++;
    pickup.pickup();
    return true;
}
std::string Player::get_items() {
    std::string string;
    for (auto item: inventory) {
        string += std::to_string(item.first) + " " + std::to_string(item.second) + "\n";
    }
    return string;
}

void Player::set_items(int num_health, int num_speed, int num_power) {
    inventory[HEALTH_POTION] = num_health;
    inventory[SPEED_POTION] = num_speed;
    inventory[POWER_POTION] = num_power;
}

void Player::print_items() const {
    for (auto item: inventory) {
        Pickup pickup(map, static_cast<pickup_type>(item.first));
        std::cout << pickup.description() << " - #" << item.second << '\n';
    }
}

bool Player::use_item(pickup_type type) {
    if (inventory[type] > 0) {
        Pickup pickup(map, type);
        pickup.pickup_impl->apply_effect(*this); // Call the effect on the player
        inventory[type]--;
        return true;
    }
    return false;
}