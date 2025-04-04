#include "Enemy.h"

Enemy::Enemy(Map &map) : Pawn(map) {
    generate_enemy(RANDOM_ENEMY);
}

Enemy::Enemy(Map &map, enemy_type type) : Pawn(map) {
    generate_enemy(type);
}

void Enemy::generate_enemy(enemy_type type) {
    if (type == RANDOM_ENEMY) {
        srand(time(nullptr));
        type = static_cast<enemy_type>(rand() % 2 + 1);
    }

    switch (type) {
        case WARRIOR:
            max_health = health = 15;
            damage = 3;
            movement_speed = 2;
            image = 'W';
            break;

        case MAGE:
            max_health = health = 10;
            damage = 5;
            movement_speed = 3;
            image = 'M';
            break;

        default:
            break;
    }
}

Enemy::Enemy(Map &map, enemy_type type, int pos_x, int pos_y) : Enemy(map, type) {
    this->pos_x = pos_x;
    this->pos_y = pos_y;

    map.set_pos(pos_x, pos_y, image);
}
