#include "Map.h"

Map::Map(bool have_obstacles) {
    srand(time(nullptr));
    int map_size_range = 7;
    int min_map_size = 10;
    map_size = rand() % map_size_range + min_map_size;

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
        int num_of_obstacles_range = 5;
        int min_num_of_obstacles = 2;
        int num_of_obstacles = rand() % num_of_obstacles_range + min_num_of_obstacles;
        int obstacle_size;

        int obstacle_size_range = 2;
        int min_obstacle_size = 1;
        for (int i = 0; i < num_of_obstacles; ++i) {
            obstacle_size = rand() % obstacle_size_range + min_obstacle_size;
            create_obstacle(obstacle_size);
        }
    }
}

bool Map::place_door(int x, int y) {
    std::vector<std::pair<int, int>> possible_door_pos;

    for (int i = 1; i < map_size - 1; ++i) {
        // Top Wall
        possible_door_pos.emplace_back(i, 0);

        // Bottom Wall
        possible_door_pos.emplace_back(i, map_size - 1);

        // Right Wall
        possible_door_pos.emplace_back(map_size - 1, i);

        // Left Wall
        possible_door_pos.emplace_back(0, i);
    }

    auto rng = std::default_random_engine {};
    std::shuffle(possible_door_pos.begin(), possible_door_pos.end(), rng);

    bool exist_path_to_door = true;
    std::pair<int, int> pos;
    int door_x, door_y;
    while (not possible_door_pos.empty() && exist_path_to_door) {
        pos = possible_door_pos.back();
        door_x = pos.first, door_y = pos.second;
        map[door_y][door_x] = DOOR;
        exist_path_to_door = find_path(x, y, door_x, door_y).empty();
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
    std::vector<int> distance_map[map_size][map_size];
    for (int i = 0; i < map_size; ++i) {
        for (int j = 0; j < map_size; ++j) {
            distance_map[i][j] = std::vector<int>(map_size * map_size, std::numeric_limits<int>::min());
        }
    }

    std::vector<int> no_path = distance_map[end_pos_y][end_pos_x];

    std::vector<int> neighbors;
    std::vector<std::vector<int>> paths;
    std::vector<int> path;
    neighbors.push_back(start_pos_x);
    neighbors.push_back(start_pos_y);
    paths.emplace_back();

    int x, y;
    while (!neighbors.empty()) {
        x = neighbors.at(0);
        y = neighbors.at(1);
        neighbors.erase(neighbors.begin(), neighbors.begin() + 2);

        path = paths.at(0);
        paths.erase(paths.begin());

        if (distance_map[y][x].size() <= path.size() || ! is_walkable(x, y)) {
            continue;
        }

        distance_map[y][x] = path;

        std::vector<std::pair<int, int>> directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (auto direction : directions) {
            if (is_walkable(x + direction.first, y + direction.second)) {
                neighbors.push_back(x + direction.first);
                neighbors.push_back(y + direction.second);

                paths.push_back(path);
                paths.at(paths.size() - 1).push_back(x + direction.first);
                paths.at(paths.size() - 1).push_back(y + direction.second);
            }

        }

    }
    if (no_path == distance_map[end_pos_y][end_pos_x]) {
        return {};
    }

    return distance_map[end_pos_y][end_pos_x];
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
