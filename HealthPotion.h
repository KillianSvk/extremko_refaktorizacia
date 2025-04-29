#pragma once
#include "PickupBase.h"

class HealthPotion : public PickupBase {
public:
    HealthPotion(Map &map);
    std::string description() const override;
    pickup_type get_type() const override;
};