#pragma once
#include "PickupBase.h"

class SpeedPotion : public PickupBase {
public:
    SpeedPotion(Map &map);
    std::string description() const override;
    pickup_type get_type() const override;
};