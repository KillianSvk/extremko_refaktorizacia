#include "Map.h"

Map::Map(bool have_obstacles) {
    srand(time(nullptr));
    map_size = rand() % 7 + 10;

    for (int i = 0; i < map_size; ++i) {
        for (int j = 0; j < map_size; ++j) {
            if (i == 0 || i == map_size - 1 || j == 0 || j == map_size - 1) {
                map[i].push_back(WALL);

            } else {
                map[i].push_back(' ');
            }
        }
    }

    // Create Obstacles
    if (have_obstacles) {
        int num_of_obstacles = rand() % 5 + 2;
        int obstacle_size;
        for (int i = 0; i < num_of_obstacles; ++i) {
            obstacle_size = rand() % 2 + 1;
            create_obstacle(obstacle_size);
        }
    }
}

bool Map::place_door(int x, int y) {
    std::vector<std::pair<int, int>> possible_door_pos;
    // Top Wall
    for (int i = 1; i < map_size - 1; ++i) {
        possible_door_pos.emplace_back(i, 0);
    }
    // Bottom Wall
    for (int i = 1; i < map_size - 1; ++i) {
        possible_door_pos.emplace_back(i, map_size - 1);
    }
    // Right Wall
    for (int i = 1; i < map_size - 1; ++i) {
        possible_door_pos.emplace_back(map_size - 1, i);
    }
    // Left Wall
    for (int i = 1; i < map_size - 1; ++i) {
        possible_door_pos.emplace_back(0, i);
    }

    auto rng = std::default_random_engine {};
    std::shuffle(possible_door_pos.begin(), possible_door_pos.end(), rng);

    bool no_path = true;
    std::pair<int, int> pos;
    int door_x, door_y;
    while (not possible_door_pos.empty() && no_path) {
        pos = possible_door_pos.back();
        door_x = pos.first, door_y = pos.second;
        map[door_y][door_x] = EMPTY;
        no_path = find_path(x, y, door_x, door_y).empty();
        map[door_y][door_x] = WALL;
        possible_door_pos.pop_back();
    }

    if (possible_door_pos.empty()) {
        return false;
    }

    map[door_y][door_x] = DOOR;
    door_pos = std::pair<int, int>(door_x, door_y);
    return true;
}

void Map::print() const {
    for (int i = 0; i < map_size; ++i) {
        for (int j = 0; j < map_size; ++j) {
            std::cout << map[i][j] << " ";
        }
        std::cout << '\n';
    }
}

void Map::create_obstacle(int size) {
    int pos_x = rand() % (map_size - 2) + 1;
    int pos_y = rand() % (map_size - 2) + 1;

    for (int x = pos_x; x < pos_x + size; ++x) {
        for (int y = pos_y; y < pos_y + size; ++y) {
            map[y][x] = WALL;
        }
    }
}


bool Map::is_walkable(int x, int y) const {
    if (x < 0 || x > map_size - 1 || y < 0 || y > map_size - 1) {
        return false;
    }

    if (map[y][x] == WALL) {
        return false;
    }

    return true;
}

bool Map::is_empty(int x, int y) const {
    if (x < 0 || x > map_size - 1 || y < 0 || y > map_size - 1) {
        return false;
    }

    if (map[y][x] == EMPTY) {
        return true;
    }

    return false;
}

bool Map::set_pos(int x, int y, char image) {
    if (!is_walkable(x, y)){
        return false;
    }

    map[y][x] = image;
    return true;
}

bool Map::set_pos(int x, int y, special_characters image) {
    if (!is_walkable(x, y)){
        return false;
    }

    map[y][x] = image;
    return true;
}

std::vector<int> Map::find_path(int start_pos_x, int start_pos_y, int end_pos_x, int end_pos_y) const {
    std::pair<int, std::vector<int>> distance_map[map_size][map_size];
    for (int i = 0; i < map_size; ++i) {
        for (int j = 0; j < map_size; ++j) {
            distance_map[i][j] = std::pair<int, std::vector<int>>(std::numeric_limits<int>::max(), {});
        }
    }

    std::vector<int> neighbors;
    std::vector<std::vector<int>> paths;
    std::vector<int> path;
    neighbors.push_back(start_pos_x);
    neighbors.push_back(start_pos_y);
    neighbors.push_back(0);

    paths.emplace_back();

    int x = neighbors.at(0), y = neighbors.at(1);
    while (!neighbors.empty()) {
        x = neighbors.at(0);
        y = neighbors.at(1);
        neighbors.erase(neighbors.begin(), neighbors.begin() + 3);

        path = paths.at(0);
        paths.erase(paths.begin());

        if (distance_map[y][x].first <= path.size() || ! is_walkable(x, y)) {
            continue;
        }

        distance_map[y][x].first = path.size();
        distance_map[y][x].second = path;

        std::vector<std::pair<int, int>> directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (auto direction : directions) {
            if (is_walkable(x + direction.first, y + direction.second)) {
            neighbors.push_back(x + direction.first);
            neighbors.push_back(y + direction.second);
            neighbors.push_back(path.size() + 1);

            paths.push_back(path);
            paths.at(paths.size() - 1).push_back(x + direction.first);
            paths.at(paths.size() - 1).push_back(y + direction.second);
            }

        }

    }


    return distance_map[end_pos_y][end_pos_x].second;

}


std::string Map::get_map() {
    std::string string;
    for (auto line : map) {
        if (! line.empty()) {
            string += line;
            string += '\n';
        }
    }

    return string;
}

void Map::set_map(int new_size, const std::string &map_string) {
    map_size = new_size;

    for (int i = 0; i < map_size; ++i) {
        for (int j = 0; j < map_size; ++j) {
            map[i][j] = ' ';
            map[i].clear();
        }
    }

    std::string line;
    int i = 0;
    for (const auto c : map_string) {
        if (c == '\n') {
            map[i] += line;
            line.clear();
            i++;

        } else {
            line += c;

        }
    }

}
