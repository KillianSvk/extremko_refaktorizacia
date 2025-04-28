#include <iostream>
#include <vector>
#include <queue>
#include <tuple>
#include <functional>
#include <ctime>
#include <limits>
#include <algorithm>
#include <random>

enum special_characters {PICKUP = 15, EMPTY = 32, WALL = 35, PLAYER = 64, DOOR = 177 };

#pragma once

const int MAX_SIZE = 20;

class Map {
private:
    int map_size;
    std::string map[MAX_SIZE];
    std::pair<int, int> door_pos;

    void create_obstacle(int size);

public:
    explicit Map(bool have_obstacles = true);
    int get_size() const {return map_size;}

    std::string get_map();
    void set_map(int new_size, const std::string &map_string);
    void print() const;
    bool is_walkable (int x, int y) const ;
    bool is_empty (int x, int y) const ;
    bool place_door(int x, int y);
    std::pair<int, int> get_door_pos() const {return door_pos;}
    void set_door_pos(std::pair<int, int> new_door_pos) {door_pos = new_door_pos;}
    std::vector<int> find_path(int start_pos_x, int start_pos_y, int end_pos_x, int end_pos_y) const;
    bool set_pos(int x, int y, char image);
    bool set_pos(int x, int y, special_characters image);
};
