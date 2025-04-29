#include "Game.h"

Game::Game() = default;

void Game::print() const {
    std::cout << "Score: " << score << '\n';
    map.print();
}

void Game::gain_score() {
    score++;
}

void Game::gain_score(int s) {
    score += s;
}

void Game::play() {
    Player player(map);
    player.set_pos(map.get_size() / 2, map.get_size() - 2);

    bool door_placed = false;
    while (!door_placed) {
        door_placed = map.place_door(player.get_pos_x(), player.get_pos_y());
    }

    std::vector<Enemy> enemies;
    std::vector<Pickup> pickups;
    srand(time(nullptr));

    print_help();

    while (true) {
        if (enemies.empty()) {
            populate_map(enemies, pickups);
        }

        // Player Turn
        if (player_turn(player, enemies, pickups)) {
            break;
        }

        std::cout << "HP: " << player.get_health() << " Moves: " << player.get_movement_left() << " ";
        print();

        // Enemy Turn
        for (auto &enemy: enemies) {

            if (enemy.is_dead()) {
                continue;
            }

            enemy.move_towards(player.get_pos_x(), player.get_pos_y());

            if (enemy.get_pos_x() == player.get_pos_x()
                && enemy.get_pos_y() == player.get_pos_y()) {
                std::cout << "Enemy approached you in the Dungeon \n";
                if (fight(player, enemy)) {
                    std::cout << "Enemy has defeated you \n";
                    break;

                } else {
                    map.set_pos(player.get_pos_x(), player.get_pos_y(), player.get_image());
                }
            }
        }

        if (player.get_health() <= 0) {
            break;
        }
    }

    std::cout << "Game Over \n"
              << "Your final score: " << score << '\n';

}

void Game::populate_enemies(std::vector<Enemy> &enemies, std::vector<std::pair<int, int>> &used_pos) {
    int range_of_num_of_enemies = 3;
    int min_num_of_enemies = 1;
    int num_of_enemies = rand() % range_of_num_of_enemies + min_num_of_enemies;

    for (int i = 0; i < num_of_enemies; ++i) {
        enemies.emplace_back(map);
    }

    bool placed, pos_free;
    int x, y;

    for (auto &enemy: enemies) {
        placed = false;
        while (!placed) {
            pos_free = true;
            x = rand() % map.get_size();
            y = rand() % map.get_size();
            for (auto pos: used_pos) {
                if (x == pos.first && y == pos.second) {
                    pos_free = false;
                    break;
                }
            }

            if (!pos_free) {
                continue;
            }

            placed = enemy.set_pos(x, y);
            used_pos.emplace_back(x, y);
        }
    }
}

void Game::populate_pickups(std::vector<Pickup> &pickups, std::vector<std::pair<int, int>> &used_pos) {
    bool placed, pos_free;
    int x, y;

    int range_of_num_of_pickups = 3;
    int min_num_of_pickups = 1;
    int num_of_pickups = rand() % range_of_num_of_pickups + min_num_of_pickups;

    for (int i = 0; i < num_of_pickups; ++i) {
        pickups.emplace_back(map, RANDOM_PICKUP);
    }

    for (auto &pickup: pickups) {
        placed = false;
        while (!placed) {
            pos_free = true;
            x = rand() % map.get_size();
            y = rand() % map.get_size();
            for (auto pos: used_pos) {
                if (x == pos.first && y == pos.second) {
                    used_pos.emplace_back(x, y);
                    pos_free = false;
                    break;
                }
            }

            if (!pos_free) {
                continue;
            }

            placed = pickup.set_pos(x, y);
        }
    }
}

void Game::populate_map(std::vector<Enemy> &enemies, std::vector<Pickup> &pickups) {
    std::vector<std::pair<int, int>> used_pos = {map.get_door_pos()};
    populate_enemies(enemies, used_pos);
    populate_pickups(pickups, used_pos);
}

bool Game::player_turn(Player &player, std::vector<Enemy> &enemies, std::vector<Pickup> &pickups) {
    player.reset_movement();
    std::string player_input;
    int door_x, door_y;

    while (player.get_movement_left() > 0) {
        door_x = map.get_door_pos().first;
        door_y = map.get_door_pos().second;

        std::cout << "HP: " << player.get_health() << "  Moves: " << player.get_movement_left() << "  ";
        print();

        std::cin >> player_input;

        // Check Player Input
        if (player_input == "w") {
            player.move(UP);

        } else if (player_input == "s") {
            player.move(DOWN);

        } else if (player_input == "a") {
            player.move(LEFT);

        } else if (player_input == "d") {
            player.move(RIGHT);

        } else if (player_input == "u" || player_input == "use") {
            if (not player_use_item(player)) {
                continue;
            }

        } else if (player_input == "help") {
            print_help();

        } else if (player_input == "save") {
            if (save(player, enemies, pickups)) {
                std::cout << "Game saved successfully" << '\n';

            } else {
                std::cout << "Unable to save the game" << '\n';

            }
            continue;

        } else if (player_input == "load") {
            if (load(player, enemies, pickups)) {
                std::cout << "Game loaded successfully" << '\n';

            } else {
                std::cout << "Unable to load the game" << '\n';

            }
            continue;

        } else if (player_input == "x") {
            return true;

        } else {
            std::cout << "That did not work, try something else or write \"help\"" << '\n';
        }

        for (auto &pickup: pickups) {
            if (!pickup.is_picked()
                && pickup.get_pos() == player.get_pos()) {

                player.pickup(pickup);
                std::cout << "You found " << pickup.description() << ", on the ground \n";
            }
        }

        for (auto &enemy: enemies) {
            if (!enemy.is_dead()
                && enemy.get_pos() == player.get_pos()) {
                std::cout << "You approached enemy in the Dungeon \n";
                fight(player, enemy);
            }
        }

        // New Level (Map)
        if (player.get_pos_x() == door_x
            && player.get_pos_y() == door_y) {
            map = Map();
            // Door Top
            if (player_input == "w") {
                for (int i = 0; i < map.get_size() / 2; ++i) {
                    if (player.set_pos(map.get_size() / 2 + i, map.get_size() - 2)) {
                        break;
                    }
                    if (player.set_pos(map.get_size() / 2 - i, map.get_size() - 2)) {
                        break;
                    }
                }

            // Door Bottom
            } else if (player_input == "s") {
                for (int i = 0; i < map.get_size() / 2; ++i) {
                    if (player.set_pos(map.get_size() / 2 + i, 1)) {
                        break;
                    }
                    if (player.set_pos(map.get_size() / 2 - i, 1)) {
                        break;
                    }
                }

            // Door Left
            } else if (player_input == "a") {
                for (int i = 0; i < map.get_size() / 2; ++i) {
                    if (player.set_pos(map.get_size() - 2, i)) {
                        break;
                    }
                    if (player.set_pos(map.get_size() - 2, -i)) {
                        break;
                    }
                }

            // Door right
            } else if (player_input == "d") {
                for (int i = 0; i < map.get_size() / 2; ++i) {
                    if (player.set_pos(1, map.get_size() / 2 + i)) {
                        break;
                    }
                    if (player.set_pos(1, map.get_size() / 2 - i)) {
                        break;
                    }
                }
            }

            bool door_placed = false;
            while (!door_placed) {
                door_placed = map.place_door(player.get_pos_x(), player.get_pos_y());
            }
            enemies.clear();
            pickups.clear();
            populate_map(enemies, pickups);
            score++;
            std::cout << "You entered a new Level" << '\n';
        }
    }

    return false;

}


bool Game::fight(Player &player, Enemy &enemy) {
    std::string player_input;
    srand(time(nullptr));
    int chance;
    help_fight();

    while (true) {
        std::cout << "Player: " << player.get_health() << "HP \n"
                  << "Enemy: " << enemy.get_health() << "HP \n";

        std::cin >> player_input;

        // Player Turn
        if (player_input == "a" || player_input == "attack") {
            enemy.lose_health(player.get_damage());
            std::cout << "You attacked enemy for " << player.get_damage() << '\n';
            if (enemy.get_health() <= 0) {
                break;
            }

        } else if (player_input == "u" || player_input == "use") {
            if (not player_use_item(player)) {
                continue;
            }

        } else if (player_input == "help") {
            help_fight();

        } else {
            std::cout << "This doesnt work try something else or type \"help\" for controls \n";
            continue;
        }

        // Enemy Turn
        chance = rand() % 100;
        if (chance <= 80) {
            player.lose_health(enemy.get_damage());
            std::cout << "Enemy attacked you for " << enemy.get_damage() << " dmg \n";

        } else if (chance <= 90) {
            enemy.use_item(HEALTH_POTION);
            std::cout << "Enemy used HEALTH POTION \n";

        } else {
            enemy.use_item(POWER_POTION);
            std::cout << "Enemy used POWER POTION \n";

        }

        if (player.get_health() <= 0) {
            return true;
        }

        std::cout << '\n';
    }

    std::cout << "You have defeated an enemy \n";
    enemy.die();

    chance = rand() % 100;
    if (chance <= 130) {
        Pickup pickup(map, RANDOM_PICKUP);
        player.pickup(pickup);
        std::cout << "You found " << pickup.description() << ", on enemy \n";
    }

    player.reset_damage();
    score++;
    return false;
}

bool Game::player_use_item(Player &player) {
    std::string player_input;

    player.print_items();
    std::cout << "BACK (b) \n";

    std::cin >> player_input;

    if (player_input == "b" || player_input == "back") {
        return false;

    } else if (player_input == "p") {
        if (player.use_item(POWER_POTION)) {
            std::cout << "You used POWER POTION \n";
            player.use_movement();
            return true;
        }

    } else if (player_input == "s") {
        if (player.use_item(SPEED_POTION)) {
            std::cout << "You used SPEED POTION \n";
            player.use_movement();
            return true;
        }

    } else if (player_input == "h") {
        if (player.use_item(HEALTH_POTION)) {
            std::cout << "You used HEALTH POTION \n";
            player.use_movement();
            return true;
        }
    }

    std::cout << "You dont have this item \n";
    return false;
}

void Game::print_help() const {
    std::cout << "Controls: " << '\n'
              << "    UP - w" << '\n'
              << "    DOWN - s" << '\n'
              << "    LEFT - a" << '\n'
              << "    RIGHT - d" << '\n'
              << "    USE ITEM - u/use" << '\n'
              << '\n'
              << "    SAVE GAME - save" << '\n'
              << "    LOAD GAME - load" << '\n'
              << "    EXIT - x" << '\n';
}

void Game::help_fight() const {
    std::cout << "Controls: " << '\n'
              << "    ATTACK - a/attack" << '\n'
              << "    USE ITEM - u/use" << '\n';
}

void Game::save_game_score(std::ofstream &file) const {
    file << score << '\n';
    file << '\n';
}

void Game::save_map(std::ofstream &file)  {
    file << map.get_door_pos().first << " " << map.get_door_pos().second << '\n';
    file << map.get_size() << '\n';
    file << map.get_map();
    file << '\n';
}

void Game::save_player(std::ofstream &file, Player &player) {
    file << player.get_pos_x() << " " << player.get_pos_y() << '\n';
    file << player.get_max_health() << " " << player.get_health() << '\n';
    file << player.get_movement_speed() << " " << player.get_movement_left() << '\n';
    file << player.get_items();
    file << '\n';
}

void Game::save_enemies(std::ofstream &file, std::vector<Enemy> &enemies) {
    file << std::to_string(enemies.size()) << '\n';
    for (auto &enemy: enemies) {
        file << enemy.get_pos_x() << " " << enemy.get_pos_y() << '\n';
        file << enemy.get_image() << '\n';
    }
    file << '\n';
}

void Game::save_pickups(std::ofstream &file, std::vector<Pickup> &pickups) {
    file << std::to_string(pickups.size()) << '\n';
    for (auto &pickup: pickups) {
        file << pickup.get_pos_x() << " " << pickup.get_pos_y() << '\n';
        file << std::to_string(pickup.get_type()) << '\n';
    }
    file << '\n';
}

bool Game::save(Player &player, std::vector<Enemy> &enemies, std::vector<Pickup> &pickups) {
    std::ofstream file;
    file.open("save.txt");

    if (!file) {
        return false;
    }

    save_game_score(file);
    save_map(file);
    save_player(file, player);
    save_enemies(file, enemies);
    save_pickups(file, pickups);

    file.close();
    return true;
}

std::pair<int, int> Game::get_pair_from_str(const std::string &line) {
    std::istringstream tmp_stream(line);
    std::string tmp;
    int first, second, j = 0;
    while (tmp_stream >> tmp) {
        if (j == 0) {
            first = std::stoi(tmp);
            j++;
        } else if (j == 1) {
            second = std::stoi(tmp);
        }
    }

    return {first, second};
}

void Game::load_score(std::ifstream &file) {
    std::string line;

    std::getline(file, line);
    score = std::stoi(line);
}

void Game::load_map(std::ifstream &file) {
    std::string line;

    std::getline(file, line);
    map.set_door_pos(get_pair_from_str(line));

    // Map
    std::getline(file, line);
    int j = std::stoi(line);
    std::string new_map;
    for (int k = 0; k < j; ++k) {
        std::getline(file, line);
        new_map += line;
        new_map += '\n';
    }
    map.set_map(j, new_map);
}

void Game::load_player(std::ifstream &file, Player &player) {
    std::string line;
    int first, second, third;

    // Pos
    std::getline(file, line);
    player.set_pos(get_pair_from_str(line).first, get_pair_from_str(line).second);
    // Health
    std::getline(file, line);
    first = get_pair_from_str(line).first;
    second = get_pair_from_str(line).second;
    player.set_max_health(first);
    player.set_health(second);
    // Speed
    std::getline(file, line);
    first = get_pair_from_str(line).first;
    second = get_pair_from_str(line).second;
    player.set_movement_speed(first);
    player.set_movement_left(second);
    // Items
    std::getline(file, line);
    first = get_pair_from_str(line).second;
    std::getline(file, line);
    second = get_pair_from_str(line).second;
    std::getline(file, line);
    third = get_pair_from_str(line).second;
    player.set_items(first, second, third);
}

void Game::load_enemies(std::ifstream &file, std::vector<Enemy> &enemies) {
    std::string line;
    int first, second;

    std::getline(file, line);
    int j = std::stoi(line);
    for (int k = 0; k < j; ++k) {
        std::getline(file, line);
        first = get_pair_from_str(line).first;
        second = get_pair_from_str(line).second;
        std::getline(file, line);
        char c = line.c_str()[0];
        switch (c) {
            case 'W':
                enemies.emplace_back(map, WARRIOR, first, second);
                break;
            case 'M':
                enemies.emplace_back(map, MAGE, first, second);
                break;
            default:
                break;
        }
    }
}

void Game::load_pickups(std::ifstream &file, std::vector<Pickup> &pickups) {
    std::string line;
    int first, second, third;

    std::getline(file, line);
    int j = std::stoi(line);
    for (int k = 0; k < j; ++k) {
        std::getline(file, line);
        first = get_pair_from_str(line).first;
        second = get_pair_from_str(line).second;
        std::getline(file, line);
        third = std::stoi(line);
        switch (third) {
            case 0:
                pickups.emplace_back(map, RANDOM_PICKUP, first, second);
                break;
            case 1:
                pickups.emplace_back(map, HEALTH_POTION, first, second);
                break;
            case 2:
                pickups.emplace_back(map, POWER_POTION, first, second);
                break;
            case 3:
                pickups.emplace_back(map, SPEED_POTION, first, second);
                break;
            default:
                break;
        }

    }

}

bool Game::load(Player &player, std::vector<Enemy> &enemies, std::vector<Pickup> &pickups) {
    std::ifstream file("save.txt");

    if (!file) {
        return false;
    }

    int i = 0;
    std::string line;

    while (true) {
        if (i == 0) {
            load_score(file);

            std::getline(file, line);
            i++;
        }

        else if (i == 1) {
            load_map(file);

            std::getline(file, line);
            i++;
        }

        else if (i == 2) {
            load_player(file, player);

            std::getline(file, line);
            i++;

        } else if (i == 3) {
            load_enemies(file, enemies);

            std::getline(file, line);
            i++;

        } else if (i == 4) {
            load_pickups(file, pickups);

            std::getline(file, line);
            i++;

        } else {
            break;
        }
    }

    file.close();
    return true;
}
