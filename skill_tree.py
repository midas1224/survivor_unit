import ability_module as abm
from ability_module import Upgrade, AbilityUpgrade, TraitUpgrade
from typing_extensions import Self
from player import player

# DESCRIPTION:
# This is intended to be used in a node-based framework, allowing for unlock of skill upgrades on a branching path


skill_trees = {'fighter': []}
skill_tree_upgrades = {'fighter': []}


class SkillTreeNode:
    def __init__(self, tree_key: str, upgrade: Upgrade, is_unlocked: bool = False, prereqs: list[Self] = ()):
        self.pre_reqs = prereqs
        self.is_unlocked: bool = is_unlocked
        self.is_learned: bool = False
        self.upgrade = upgrade
        self.tree = skill_trees[tree_key]
        self.learned_upgrades: list[Upgrade] = skill_tree_upgrades[tree_key]
        self.tree_key = tree_key
        self.times_learned = 0
        self.max_times_learnable = 5

    def try_unlock(self):
        unfilled_reqs = []
        for req in self.pre_reqs:
            if not req.is_learned:
                unfilled_reqs.append(req)
        if len(unfilled_reqs) > 0:
            print(f'The following nodes need to be learned before {self}.')
            for req in unfilled_reqs:
                print(req)
        else:
            self.is_unlocked = True

    def learn_node(self):
        self.try_unlock()
        if self.is_unlocked:
            self.is_learned = True
            if self.times_learned < self.max_times_learnable:
                self.times_learned += 1
                upgrade_list: list[Upgrade] = skill_tree_upgrades[self.tree_key]
                upgrade_list.append(self.upgrade)
                if type(self.upgrade) is TraitUpgrade:
                    self.upgrade: TraitUpgrade
                    print(f'Learned: {self.upgrade}')
                    print(f'This node can be learned {self.max_times_learnable - self.times_learned} more times.')

    def __str__(self):
        return f'Node: {self.upgrade}'

# Work in progress feature to allow for a given upgrade node to be 'learned' multiple times
# class RepeatableSkillTreeNode(SkillTreeNode):


# applies all unlocked nodes in a given skill tree to the player character
# original intent is to do this one time before 'a game' has started
def apply_skill_tree(tree_key: str):
    for upgrade in skill_tree_upgrades[tree_key]:
        upgrade: TraitUpgrade
        upgrade.apply_to_base()


# wrapper for the SkillTreeNode class function: learn_node
def learn_node(node: SkillTreeNode):
    node.learn_node()


# examples of static upgrades (as opposed to ones generated in the proposition function)
# to be used in the skill tree
damage_upgrade = TraitUpgrade('damage', abm.UPGRADE_TABLE['damage'])
cast_rate_upgrade = TraitUpgrade('cast_rate', abm.UPGRADE_TABLE['cast_rate'])
area_upgrade = TraitUpgrade('area', abm.UPGRADE_TABLE['area'])


# basic skill tree construction
fighter_node_01 = SkillTreeNode('fighter', damage_upgrade, True)
# ^^^ This is the 'root' node, and as such, starts unlocked ^^^

fighter_node_02 = SkillTreeNode('fighter', cast_rate_upgrade, False, [fighter_node_01])
fighter_node_03 = SkillTreeNode('fighter', area_upgrade, False, [fighter_node_02])
