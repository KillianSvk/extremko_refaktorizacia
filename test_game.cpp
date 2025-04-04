// Copyright 2005, Google Inc.
// All rights reserved.

#include <iostream>
#include "gtest/gtest.h"

#include "Game.h"
#include "Enemy.h"

using namespace ::testing;

// TEST GAME CLASS
TEST(Game, Inicialization) {
    Game game;
    ASSERT_EQ(0, game.get_score());

    game.gain_score();
    ASSERT_EQ(1, game.get_score());

    game.gain_score(5);
    ASSERT_EQ(6, game.get_score());

//    game.print();
}

TEST(Game, AlwaysCanReachDoor) {
    Game game;
    Map *map = game.get_map();

    std::vector<int> path;
    Enemy enemy(*map, MAGE);

    srand(time(nullptr));
    bool enemy_placed = false;
    while (! enemy_placed){
        enemy_placed = enemy.set_pos(rand() % map->get_size(), rand() % map->get_size());
    }

    map->place_door(enemy.get_pos_x(), enemy.get_pos_y());
    std::pair<int, int> door_pos = map->get_door_pos();

//    game.print();
//    std::cout << door_pos.first << "-" << door_pos.second << '\n';

    path = map->find_path(door_pos.first, door_pos.second, enemy.get_pos_x(), enemy.get_pos_y());
    ASSERT_FALSE(path.empty());

}

TEST(Game, GoToEnemy) {
    Game game;
    Map *map = game.get_map();
    Enemy warrior(*map, WARRIOR), mage(*map, MAGE);

    bool enemy_placed = false;
    while (! enemy_placed){
        enemy_placed = warrior.set_pos(rand() % map->get_size(), rand() % map->get_size());
    }

    std::vector<int> path;
    enemy_placed = false;
    while (!enemy_placed && path.empty()){
        enemy_placed = mage.set_pos(rand() % map->get_size(), rand() % map->get_size());
        path = map->find_path(warrior.get_pos_x(), warrior.get_pos_y(), mage.get_pos_x(), mage.get_pos_y());
    }

//    game.print();

    while (warrior.get_pos_x() != mage.get_pos_x()
    || warrior.get_pos_y() != mage.get_pos_y()) {
        warrior.move_towards(mage.get_pos_x(), mage.get_pos_y());
//        game.print();
    }


    ASSERT_TRUE(warrior.get_pos_x() == mage.get_pos_x());
    ASSERT_TRUE(warrior.get_pos_y() == mage.get_pos_y());
}

TEST(Game, PlayerMoveOnMap) {
    Game game;
    Map *map = game.get_map();
    Player player(*map);

    srand(time(nullptr));
    bool placed = false;
    while (! placed) {
        placed = player.set_pos(rand() % map->get_size(), rand() % map->get_size());
    }

    int old_x = player.get_pos_x(), old_y = player.get_pos_y(), times_moved = 0;
    bool moved = player.move(LEFT);
    if (moved) {
        ASSERT_TRUE(old_x - 1 == player.get_pos_x());
        times_moved++;
    } else {
        ASSERT_TRUE(old_x  == player.get_pos_x());
    }

    old_x = player.get_pos_x();
    old_y = player.get_pos_y();
    moved = player.move(RIGHT);
    if (moved) {
        ASSERT_TRUE(old_x + 1 == player.get_pos_x());
        times_moved++;
    } else {
        ASSERT_TRUE(old_x  == player.get_pos_x());
    }

    old_x = player.get_pos_x();
    old_y = player.get_pos_y();
    moved = player.move(UP);
    if (moved) {
        ASSERT_TRUE(old_y - 1 == player.get_pos_y());
        times_moved++;
    } else {
        ASSERT_TRUE(old_y  == player.get_pos_y());
    }

    old_x = player.get_pos_x();
    old_y = player.get_pos_y();
    moved = player.move(DOWN);
    if (moved) {
        ASSERT_TRUE(old_y + 1 == player.get_pos_y());
        times_moved++;
    } else {
        ASSERT_TRUE(old_y  == player.get_pos_y());
    }

    ASSERT_EQ(player.get_movement_speed() - times_moved, player.get_movement_left());
}


TEST(Game, PopulateMap) {
    Game game;
    auto map = game.get_map();
    std::vector<Enemy> enemies;
    std::vector<Pickup> pickups;

    ASSERT_TRUE(enemies.empty());
    ASSERT_TRUE(pickups.empty());

    game.populate_map(enemies, pickups);

    int num_of_enemies = 0;
    for (auto enemy : enemies) {
        ASSERT_FALSE(enemy.is_dead());
        ASSERT_TRUE(map->is_walkable(enemy.get_pos_x(), enemy.get_pos_y()));
        ASSERT_FALSE(map->is_empty(enemy.get_pos_x(), enemy.get_pos_y()));
        num_of_enemies++;
    }
    ASSERT_TRUE(num_of_enemies > 0);
    ASSERT_TRUE(num_of_enemies < 4);

    int num_of_pickups = 0;
    for (auto pickup : pickups) {
        ASSERT_FALSE(pickup.is_picked());
        ASSERT_TRUE(map->is_walkable(pickup.get_pos_x(), pickup.get_pos_y()));
        ASSERT_FALSE(map->is_empty(pickup.get_pos_x(), pickup.get_pos_y()));
        num_of_pickups++;
    }
    ASSERT_TRUE(num_of_pickups >= 0);
    ASSERT_TRUE(num_of_pickups < 4);

}

TEST(Game, SaveLoad) {
    Game game;
    Player player(*game.get_map());
    std::vector<Enemy> enemies;
    std::vector<Pickup> pickups;
    game.populate_map(enemies, pickups);
    game.save(player, enemies, pickups);

    Game game2;
    Player player2(*game2.get_map());
    std::vector<Enemy> enemies2;
    std::vector<Pickup> pickups2;
    game2.load(player2, enemies2, pickups2);

    ASSERT_EQ(player.get_pos_x(), player2.get_pos_x());
    ASSERT_EQ(player.get_pos_y(), player2.get_pos_y());
    ASSERT_EQ(player.get_items(), player2.get_items());
    ASSERT_EQ(player.get_max_health(), player2.get_max_health());
    ASSERT_EQ(player.get_health(), player2.get_health());
    ASSERT_EQ(player.get_movement_speed(), player2.get_movement_speed());
    ASSERT_EQ(player.get_movement_left(), player2.get_movement_left());

    for (int i = 0; i < enemies.size(); ++i) {
        ASSERT_EQ(enemies[i].is_dead(), enemies2[i].is_dead());
        ASSERT_EQ(enemies[i].get_image(), enemies2[i].get_image());
        ASSERT_EQ(enemies[i].get_pos_x(), enemies2[i].get_pos_x());
        ASSERT_EQ(enemies[i].get_pos_y(), enemies2[i].get_pos_y());
        ASSERT_EQ(enemies[i].get_health(), enemies2[i].get_health());

    }

    for (int i = 0; i < pickups.size(); ++i) {
        ASSERT_EQ(pickups[i].get_type(), pickups2[i].get_type());
        ASSERT_EQ(pickups[i].get_pos_x(), pickups2[i].get_pos_x());
        ASSERT_EQ(pickups[i].get_pos_y(), pickups2[i].get_pos_y());
    }

}

// TEST MAP

TEST(Map, Inicialization) {
    Map map(false);
    ASSERT_EQ(NULL, map.get_door_pos().first);
    ASSERT_EQ(NULL, map.get_door_pos().second);

}

TEST(Map, WalkableAndEmpty) {
    Map map(false);
    ASSERT_FALSE(map.is_walkable(0,0));
    ASSERT_TRUE(map.is_walkable(1,1));

    ASSERT_FALSE(map.is_empty(0,0));
    ASSERT_TRUE(map.is_empty(1,1));

    Enemy enemy(map,RANDOM_ENEMY,1,1);
    ASSERT_FALSE(map.is_empty(1,1));
    ASSERT_TRUE(map.is_walkable(1,1));
}

TEST(Map, Doors) {
    Map map;
    ASSERT_EQ(NULL, map.get_door_pos().first);
    ASSERT_EQ(NULL, map.get_door_pos().second);

    srand(time(nullptr));
    bool placed = false;
    Player player(map);
    while (! placed) {
        placed = player.set_pos(rand() % map.get_size(), rand() % map.get_size());
    }

    map.place_door(player.get_pos_x(), player.get_pos_y());
    ASSERT_FALSE(map.find_path(map.get_door_pos().first, map.get_door_pos().second, player.get_pos_x(), player.get_pos_y()).empty());

}


// TEST PAWNS
TEST(Pawn, DefaultInicialization) {
    Map map;
    Pawn pawn(map);
    ASSERT_EQ(0, pawn.get_pos_x());
    ASSERT_EQ(0, pawn.get_pos_y());
    ASSERT_EQ(1, pawn.get_max_health());
    ASSERT_EQ(1, pawn.get_health());
    ASSERT_EQ(1, pawn.get_damage());
    ASSERT_EQ(1, pawn.get_movement_speed());
    ASSERT_EQ('P', pawn.get_image());
}

TEST(Pawn, Inicialization) {
    Map map;
    Pawn pawn(map, 1, 2, 3, 4 ,5, 'H');
    ASSERT_EQ(1, pawn.get_pos_x());
    ASSERT_EQ(2, pawn.get_pos_y());
    ASSERT_EQ(3, pawn.get_max_health());
    ASSERT_EQ(3, pawn.get_health());
    ASSERT_EQ(4, pawn.get_damage());
    ASSERT_EQ(5, pawn.get_movement_speed());
    ASSERT_EQ('H', pawn.get_image());
}

TEST(Pawn, TakingDamage) {
    Map map;
    Enemy warrior(map, WARRIOR), mage(map, MAGE);
    ASSERT_EQ(15, warrior.get_health());
    warrior.lose_health(mage.get_damage());

    ASSERT_EQ(10, warrior.get_health());
    warrior.lose_health(mage.get_damage());

    ASSERT_TRUE(warrior.lose_health(mage.get_damage()));
}

TEST(Enemy, WarriorInicialization) {
    Map map;
    Enemy enemy(map, WARRIOR);
    ASSERT_EQ(15, enemy.get_max_health());
    ASSERT_EQ(15, enemy.get_health());
    ASSERT_EQ(3, enemy.get_damage());
    ASSERT_EQ(2, enemy.get_movement_speed());
    ASSERT_EQ('W', enemy.get_image());
}

TEST(Player, Inicialization) {
    Map map(false);
    Player player(map, 1, 1);
    ASSERT_EQ(30, player.get_max_health());
    ASSERT_EQ(30, player.get_health());
    ASSERT_EQ(5, player.get_damage());
    ASSERT_EQ(4, player.get_movement_speed());
    ASSERT_EQ(4, player.get_movement_left());
    ASSERT_EQ(PLAYER, player.get_image());

    std::stringstream stream(player.get_items());
    std::string line;
    while (std::getline(stream, line)) {
        ASSERT_EQ(0, int(line[2]) - 48);
    }

}

TEST(Player, PotionsPickup) {
    Map map(false);
    Player player(map, 1, 1);

    std::stringstream stream(player.get_items());
    std::string line;
    while (std::getline(stream, line)) {
        ASSERT_EQ(0, int(line[2]) - 48);
    }

    Pickup pickup(map, HEALTH_POTION, 1,1);
    ASSERT_TRUE(player.pickup(pickup));

    std::stringstream stream2(player.get_items());
    while (std::getline(stream2, line)) {
        if (int(line[0]) - 48 == int(HEALTH_POTION)) {
            ASSERT_EQ(1, int(line[2]) - 48);

        } else {
            ASSERT_EQ(0, int(line[2]) -48);
        }
    }

    Pickup speed_potion(map, SPEED_POTION);
    ASSERT_TRUE(player.pickup(speed_potion));

    std::stringstream stream3(player.get_items());
    while (std::getline(stream2, line)) {
        if (int(line[0]) - 48 == int(SPEED_POTION)) {
            ASSERT_EQ(1, int(line[2]) - 48);

        } else {
            ASSERT_EQ(0, int(line[2]) -48);
        }
    }

    ASSERT_FALSE(player.pickup(speed_potion));
    std::stringstream stream4(player.get_items());
    while (std::getline(stream2, line)) {
        if (int(line[0]) - 48 == int(SPEED_POTION)) {
            ASSERT_EQ(1, int(line[2]) - 48);

        } else {
            ASSERT_EQ(0, int(line[2]) -48);
        }
    }
}

TEST(Player, PotionHeal) {
    Map map(false);
    Player player(map);
    Pickup healing_potion(map, HEALTH_POTION);

    ASSERT_TRUE(player.get_max_health() == player.get_health());

    Enemy enemy(map, MAGE);
    player.lose_health(enemy.get_damage());

    ASSERT_TRUE(player.get_max_health() - enemy.get_damage() == player.get_health());
    ASSERT_FALSE(player.use_item(HEALTH_POTION));
    ASSERT_TRUE(player.get_max_health() - enemy.get_damage() == player.get_health());

    ASSERT_TRUE(player.pickup(healing_potion));
    ASSERT_TRUE(player.use_item(HEALTH_POTION));
    ASSERT_TRUE(player.get_max_health() == player.get_health());
}

TEST(Player, PotionSpeed) {
    Map map(false);
    Player player(map, 1, 1);
    Pickup speed_potion(map, SPEED_POTION);

    ASSERT_TRUE(player.get_movement_speed() == player.get_movement_left());

    for (int i = 0; i < 4; ++i) {
        player.move(DOWN);
    }

    ASSERT_EQ (0, player.get_movement_left());

    int old_speed = player.get_movement_speed();
    player.pickup(speed_potion);
    ASSERT_TRUE(player.use_item(SPEED_POTION));

    ASSERT_EQ (0, player.get_movement_left());
    player.reset_movement();
    ASSERT_EQ(old_speed + 1, player.get_movement_left());

}

TEST(Player, PotionPower) {
    Map map(false);
    Player player(map, 1, 1);
    Pickup power_potion(map, POWER_POTION);

    int old_damage = player.get_damage();
    ASSERT_TRUE(player.pickup(power_potion));
    ASSERT_TRUE(player.use_item(POWER_POTION));

    ASSERT_EQ(old_damage + 2, player.get_damage());

    player.reset_damage();
    ASSERT_EQ(old_damage, player.get_damage());
}


// save