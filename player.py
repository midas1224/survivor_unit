class PlayerUnit:
    def __init__(self):
        self.cast_speed_bonus = 0
        self.damage_bonus = 0
        self.bases = {'speed': 1.0, 'area': 1.0, 'armor': 10, 'health': 100, 'cast_rate': 1.0, 'damage': 1.0,
                      'experience': 1.0, 'crit_damage': 2.0, 'crit_chance': 0.1}
        # used to change referenced variables
        self.attributes = {key: self.bases[key] for key in self.bases.keys()}
        # Integer Bonuses
        self.int_bonuses = {'armor': 0, 'health': 0}
        # Percentage Bonuses
        self.p_bonuses = {'speed': 1.0, 'area': 1.0, 'cast_rate': 1.0, 'damage': 1.0, 'experience': 1.0,
                          'crit_chance': 0.0, 'crit_damage': 0.0}
        # TODO: int_bonuses and p_bonuses could use some investigation/refactoring

    def apply_bonus(self, _type: str, _amount):
        test_percent = type(_amount) is float and _type in self.p_bonuses.keys()
        test_int = type(_amount) is int and _type in self.int_bonuses.keys()
        if test_percent is True:
            self.apply_percent_bonus(_type, _amount)
        elif test_int is True:
            self.apply_integer_bonus(_type, _amount)
        else:
            print(f'Attribute {_type} does not match type {type(_amount)}.')

    def apply_bonus_to_base(self, _type: str, _amount):
        test_percent = type(_amount) is float and _type in self.p_bonuses.keys()
        test_int = type(_amount) is int and _type in self.int_bonuses.keys()
        if test_percent or test_int:
            self.bases[_type] += _amount
        else:
            print(f'Attribute {_type} does not match type {type(_amount)}.')

    def apply_percent_bonus(self, _type: str, _amount: float):
        self.p_bonuses[_type] += _amount
        self.attributes[_type] = self.bases[_type] * self.p_bonuses[_type]

    def apply_integer_bonus(self, _type: str, _amount: int):
        self.int_bonuses[_type] += _amount
        self.attributes[_type] = self.bases[_type] + self.int_bonuses[_type]


player = PlayerUnit()
