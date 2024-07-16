import abc
import random
from player import player
from frozendict import frozendict

# MOD_COLOR_LUT = {0: "white", 1: "green", 2: "blue", 3: "purple", 4: "gold"}  # Work in progress 'rarity' feature
ABILITY_BASE_VALUES = frozendict({'area': 1.0, 'cast_rate': 5.0, 'damage': 20})


# function to support pseudocode
def detect_hit(ability_name: str):
    print(f'detecting hit for {ability_name}')


class Ability:
    def __init__(self, upgradeable_modules: list[str], name: str = "default_name",
                 ability_value_reference: {} = ABILITY_BASE_VALUES):
        self.name = name
        self.upgradeable_modules = upgradeable_modules
        self.attributes = {k: ability_value_reference[k] for k in upgradeable_modules}
        # any modifiers will be applied immediately

    def apply_upgrade(self, attribute_name, value):
        self.attributes[attribute_name] += value

    def use_ability(self):
        detect_hit(self.name)


class DamagingAbility(Ability):
    def __init__(self, name: str = "default_damaging", damage: int = 100):
        super().__init__(['damage', 'area', 'cast_rate'], name)
        self.damage = damage


#  Base class for TraitUpgrade and AbilityUpgrade
class Upgrade:
    def __init__(self, _improvement):
        self.improvement = _improvement

    @abc.abstractmethod
    def apply_upgrade(self):
        pass


# TraitUpgrades modify attributes on the player character
class TraitUpgrade(Upgrade):
    def __init__(self, _type: str, _improvement):
        super().__init__(_improvement)
        self.type = _type

    def apply_upgrade(self):
        player.apply_bonus(self.type, self.improvement)
        print(f'Applied {self}.')

    def apply_to_base(self):
        player.apply_bonus_to_base(self.type, self.improvement)
        print(f'Applied {self} to base stats.')

    def __eq__(self, other):
        if type(other) is TraitUpgrade:
            return other.type == self.type and other.improvement == self.improvement
        return False

    def __str__(self):
        return (f'Trait Upgrade: Improve {ATTR_STR_TABLE[self.type]} by {formatted_factor(self.type)} '
                f'{UPG_TYPE[type(self.improvement)]}')


# AbilityUpgrades target specific abilities rather than attributes pertain directly to the player character
class AbilityUpgrade(Upgrade):
    def __init__(self, target_ability: Ability, target_attribute: str, base_improvement):
        super().__init__(base_improvement)
        self.ability = target_ability
        self.attribute = target_attribute

    def apply_upgrade(self):
        for ability in equipped_abilities:
            if ability.name == self.ability.name:
                self.ability.apply_upgrade(self.attribute, self.improvement)

    def __eq__(self, other):
        if type(other) is AbilityUpgrade:
            return other.ability == self.ability and other.attribute == self.attribute
        return False

    def __str__(self):
        return (f'{self.ability.name} Upgrade: Improve {ATTR_STR_TABLE[self.attribute]} '
                f'by {formatted_factor(self.attribute)} {UPG_TYPE[type(self.improvement)]}')


# These are the 'base upgrade values' i.e. the amount by which any given attribute is upgraded,
# stored in a dictionary to assist extensibility
UPGRADE_TABLE = {'speed': 0.10, 'armor': 6, 'experience': 0.10, 'health': 15, 'area': 0.10, 'cast_rate': 0.10,
                 'damage': 0.10, "crit_chance": 0.05, "crit_damage": 0.12}


def upgrade_key_to_str(key: str) -> str:
    key = key.replace('_', ' ')
    key = key.capitalize()
    return key


# creates a list from all key in the upgrade table
ATTR_STR_TABLE = {k: upgrade_key_to_str(k) for [k, v] in UPGRADE_TABLE.items()}
UPG_TYPE = {int: 'points', float: 'percent'}


def formatted_factor(_type: str) -> str:
    if type(UPGRADE_TABLE[_type]) is int:
        return UPGRADE_TABLE[_type]
    return UPGRADE_TABLE[_type] * 100


#  proposes 3 distinct upgrades for the player to choose from to upgrade their character
def propose_upgrades():
    print("Choose an upgrade: ")
    # 1. Create upgrade propositions, referencing equipped abilities and traits
    propositions = []
    selected_traits = []
    for i in range(3):
        # TODO: add a random power-degree multiplier to ability upgrades:
        #  the multiplier should be from 1 to 4
        #  for traits and 2 to 5 for abilities
        # Upgrade variant determines what type of upgrade will be added to the propositions
        variant = random.randrange(0, 2)
        # Variant 0: Trait Upgrade
        if variant == 0:
            traits = [k for k in player.attributes.keys()]
            generated_upgrade = None
            while generated_upgrade is None or generated_upgrade in propositions:
                index = random.randrange(0, len(traits))
                rand_trait = traits[index]
                generated_upgrade = TraitUpgrade(rand_trait, UPGRADE_TABLE[rand_trait])
            propositions.append(generated_upgrade)
        # Variant 1: Ability Upgrade
        elif variant == 1:
            generated_upgrade = None
            while generated_upgrade is None or generated_upgrade in propositions:
                # select random ability from currently equipped abilities
                index = random.randrange(0, len(equipped_abilities))
                selected = equipped_abilities[index]
                # select random mod type from ability modules
                index = random.randrange(0, len(selected.upgradeable_modules))
                mod_type = selected.upgradeable_modules[index]
                # create upgrade using selected ability and attributes
                generated_upgrade = AbilityUpgrade(selected, mod_type, UPGRADE_TABLE[mod_type] * 2)
            propositions.append(generated_upgrade)
    for i in range(3):
        upgrade = propositions[i]
        print(f'{i + 1}: {upgrade}.')
    user_in = input('Enter the number of the upgrade you would like to choose: ')
    propositions[int(user_in) - 1].apply_upgrade()


# da_ prefix indicates a DamagingAbility
da_punch = DamagingAbility("Punch")
da_kick = DamagingAbility("Kick")
da_grapple = DamagingAbility("Grapple")

equipped_abilities = [da_punch, da_kick, da_grapple]
