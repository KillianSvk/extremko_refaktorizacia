#pragma once
#include "PickupBase.h"

class PowerPotion : public PickupBase {
public:
    PowerPotion(Map &map);
    std::string description() const override;
    pickup_type get_type() const override;
};