import abc
from typing import List
import ability_module
from player import player
import skill_tree


BE_LUT = {"burn": 0, "bleed": 1, "frost": 2, "doom": 3, "poison": 4}
DE_LUT = {"burn": 0, "bleed": 1, "poison": 2}


class BufferEffect:
    def __init__(self, unit, duration: float = 5.0):
        self.duration = duration
        self.alive = True
        self.unit = unit

    def count_down(self, d_time: float = 0.5, print_be: bool = False):
        if print_be:
            print(f'Time remaining: {self.duration} | ', end='')
        self.apply_effect(print_be)
        self.duration -= d_time
        self.alive = self.duration > 0.0

    @abc.abstractmethod
    def apply_effect(self, print_be: bool = False):
        pass


class DamagingEffect(BufferEffect):
    def __init__(self, unit, damage: int = 5):
        BufferEffect.__init__(self, unit)
        self.damage = damage

    @abc.abstractmethod
    def apply_effect(self, print_be: bool = False):
        pass


class Burn(DamagingEffect):
    def __init__(self, unit):
        super().__init__(unit, 5)

    def apply_effect(self, print_be: bool = False):
        self.unit.take_damage(self.damage)
        if print_be:
            print(f'Burn dealt {self.damage} damage (pre-mitigation)')


class Bleed(DamagingEffect):
    def __init__(self, unit):
        super().__init__(unit, 5)

    def apply_effect(self, print_be: bool = False):
        self.unit.take_damage(self.damage)
        if print_be:
            print(f'Bleed dealt {self.damage} damage (pre-mitigation)')


class Poison(DamagingEffect):
    def __init__(self, unit):
        super().__init__(unit, 5)

    def apply_effect(self, print_be: bool = False):
        self.unit.take_damage(self.damage)
        if print_be:
            print(f'Poison dealt {self.damage} damage (pre-mitigation)')


DUMMY_DELTA = 0.5
EFFECT_LUT = {"burn": Burn, "bleed": Bleed, "poison": Poison}


# health will use float values rounded to ints
class Unit:
    def __init__(self, health: int = 1000, speed: float = 10):
        self.health = health
        self.speed = speed
        self.buffer_bleed: List[BufferEffect] = []
        self.buffer_doom: List[BufferEffect] = []
        self.buffer_poison: List[BufferEffect] = []
        self.buffer_frost: List[BufferEffect] = []
        self.buffer_burn: List[BufferEffect] = []
        self.buffers = {"bleed": self.buffer_bleed, "doom": self.buffer_doom, "poison": self.buffer_poison,
                        "frost": self.buffer_frost, "burn": self.buffer_frost}
        self.has_buffer_effects: bool = False
        self.buffer_damages = {"bleed": 0, "poison": 0, "burn": 0}

    def take_damage(self, damage: int):
        self.health -= damage

    # optional print_be argument to display BufferEffects
    def count_down_buffers(self, print_be: bool = False):
        self.has_buffer_effects = False
        for buffer in self.buffers.values():
            if len(buffer) > 0:
                self.has_buffer_effects = True
            for effect in buffer:
                effect.count_down(DUMMY_DELTA, print_be)
                if not effect.alive:
                    buffer.remove(effect)

    def apply_buffer_effect(self, effect_name: str = "burn"):
        effect_type = EFFECT_LUT[effect_name]
        self.buffers[effect_name].append(effect_type(self))

    def tick(self, print_be: bool = False):
        self.count_down_buffers(print_be)


# demo-ing units and effects
def test_buffer_effects():
    test_unit = Unit()
    test_unit.apply_buffer_effect("bleed")
    test_unit.tick(True)
    test_unit.tick(True)
    test_unit.apply_buffer_effect("burn")
    test_unit.tick(True)
    while test_unit.has_buffer_effects:
        test_unit.tick(True)


def test_upgrading():
    base_attributes = dict.copy(player.attributes)
    ability_module.propose_upgrades()

    chicken = Unit()
    ab_peck = ability_module.Ability(['damage', 'area', 'cast_rate'], "Peck")

    print(f'Base player attributes: {base_attributes}')
    print(f'New player attributes: {player.attributes}')


def test_skill_tree():
    skill_tree.learn_node(skill_tree.fighter_node_03)
    skill_tree.learn_node(skill_tree.fighter_node_02)
    skill_tree.learn_node(skill_tree.fighter_node_01)
    skill_tree.learn_node(skill_tree.fighter_node_03)
    st_upgrades = skill_tree.skill_tree_upgrades['fighter']
    print('------------Fighter Skill Tree Upgrades------------')
    for upgrade in st_upgrades:
        print(upgrade)
    skill_tree.apply_skill_tree('fighter')


test_skill_tree()
