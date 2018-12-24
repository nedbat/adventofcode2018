# https://adventofcode.com/2018/day/24

import itertools
import pprint
import re

INPUT = """
Immune System:
3578 units each with 3874 hit points (immune to radiation) with an attack that does 10 bludgeoning damage at initiative 17
865 units each with 10940 hit points (weak to bludgeoning, cold) with an attack that does 94 cold damage at initiative 19
3088 units each with 14516 hit points (immune to cold) with an attack that does 32 bludgeoning damage at initiative 4
2119 units each with 6577 hit points (immune to slashing, fire; weak to cold) with an attack that does 22 bludgeoning damage at initiative 6
90 units each with 2089 hit points (immune to bludgeoning) with an attack that does 213 cold damage at initiative 14
1341 units each with 4768 hit points (immune to bludgeoning, radiation, cold) with an attack that does 34 bludgeoning damage at initiative 1
2846 units each with 5321 hit points (immune to cold) with an attack that does 17 cold damage at initiative 13
4727 units each with 7721 hit points (weak to radiation) with an attack that does 15 fire damage at initiative 10
1113 units each with 11891 hit points (immune to cold; weak to fire) with an attack that does 80 fire damage at initiative 18
887 units each with 5712 hit points (weak to bludgeoning) with an attack that does 55 slashing damage at initiative 15

Infection:
3689 units each with 32043 hit points (weak to cold, fire; immune to slashing) with an attack that does 16 cold damage at initiative 7
33 units each with 10879 hit points (weak to slashing) with an attack that does 588 slashing damage at initiative 12
2026 units each with 49122 hit points (weak to bludgeoning) with an attack that does 46 fire damage at initiative 16
7199 units each with 9010 hit points (immune to radiation, bludgeoning; weak to slashing) with an attack that does 2 slashing damage at initiative 8
2321 units each with 35348 hit points (weak to cold) with an attack that does 29 radiation damage at initiative 20
484 units each with 21952 hit points with an attack that does 84 radiation damage at initiative 9
2531 units each with 24340 hit points with an attack that does 18 fire damage at initiative 3
54 units each with 31919 hit points (immune to bludgeoning, cold) with an attack that does 1178 radiation damage at initiative 5
1137 units each with 8211 hit points (immune to slashing, radiation, bludgeoning; weak to cold) with an attack that does 14 bludgeoning damage at initiative 11
2804 units each with 17948 hit points with an attack that does 11 radiation damage at initiative 2
""".splitlines()

class Group:
    def __init__(self, units, hitpoints, damage, damage_kind, initiative, immune=(), weak=()):
        self.number = 0
        self.units = units
        self.hitpoints = hitpoints
        self.damage = damage
        self.damage_kind = damage_kind
        self.initiative = initiative
        self.immune = set(immune)
        self.weak = set(weak)
        self.army = None
        self.enemy = None

    def __repr__(self):
        return f"<Group {self.army.name} #{self.number} u={self.units} hp={self.hitpoints}, d={self.damage} {self.damage_kind}, ini={self.initiative}, imm={self.immune} weak={self.weak}>"

    @classmethod
    def from_line(cls, line):
        regex = (
            r"^(?P<units>\d+) units each with (?P<hitpoints>\d+) hit points "
            r"(?:\((?P<weakimmune>.*)\) )?"
            r"with an attack that does (?P<damage>\d+) (?P<damage_kind>\w+) damage "
            r"at initiative (?P<initiative>\d+)"
            )
        m = re.search(regex, line)
        if m:
            weak = set()
            immune = set()
            weakimmune = m.group('weakimmune')
            if weakimmune:
                parts = weakimmune.split(';')
                for part in parts:
                    atoms = part.split()
                    words = [a.strip(",") for a in atoms[2:]]
                    if atoms[0] == "weak":
                        weak.update(words)
                    else:
                        immune.update(words)
            return Group(
                units=int(m.group('units')),
                hitpoints = int(m.group('hitpoints')),
                damage = int(m.group('damage')),
                damage_kind = m.group('damage_kind'),
                initiative = int(m.group('initiative')),
                immune = immune,
                weak = weak,
                )

    def effective_power(self):
        return self.units * self.damage


def selection_key(group):
    """The sorting key for selecting a group to attack."""
    return (group.effective_power(), group.initiative)

def attack_damage(attacker, defender):
    if attacker.damage_kind in defender.immune:
        return 0
    elif attacker.damage_kind in defender.weak:
        return 2 * attacker.effective_power()
    else:
        return attacker.effective_power()


def attack(attacker, defender):
    damage = attack_damage(attacker, defender)
    dead_units = damage // defender.hitpoints
    dead_units = min(dead_units, defender.units)
    #print(f"{attacker} attacks {defender} killing {dead_units} units")
    defender.units -= dead_units
    if defender.units <= 0:
        defender.army.remove_group(defender)


class Army:
    def __init__(self, name):
        self.name = name
        self.groups = set()
        self.enemy = None

    def add_group(self, group):
        group.army = self
        group.enemy = self.enemy
        self.groups.add(group)
        group.number = len(self.groups)

    def remove_group(self, group):
        self.groups.remove(group)


TEST_INPUT = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""".splitlines()

def make_armies(lines):
    immune = Army("immune")
    infection = Army("infection")
    immune.enemy = infection
    infection.enemy = immune

    army = None
    for line in lines:
        if not line.strip():
            continue
        if line.startswith("Immune"):
            army = immune
        elif line.startswith("Infection"):
            army = infection
        else:
            group = Group.from_line(line)
            army.add_group(group)

    return immune, infection

def fighting_pairs(attacking, defending):
    defenders = set(defending.groups)
    for attacker in sorted(attacking.groups, key=selection_key, reverse=True):
        def attacking_key(defender):
            return (attack_damage(attacker, defender), defender.effective_power(), defender.initiative)
        if defenders:
            target = max(defenders, key=attacking_key)
            if attack_damage(attacker, target) > 0:
                yield (attacker, target)
                defenders.remove(target)

class Stalemate(Exception):
    pass

def fight(army1, army2):
    last = ""
    while army1.groups and army2.groups:
        #print("-"*80)
        # Target selection.
        pairs = (
            list(fighting_pairs(army1, army2)) +
            list(fighting_pairs(army2, army1))
            )
        this = repr(pairs)
        if this == last:
            # No progress
            raise Stalemate()
        last = this
        # Attack.
        pairs.sort(key=lambda pair: pair[0].initiative, reverse=True)
        for attacker, defender in pairs:
            attack(attacker, defender)

    return army1 if army1.groups else army2

def test_fight():
    winner = fight(*make_armies(TEST_INPUT))
    assert sum(g.units for g in winner.groups) == 5216

if __name__ == "__main__":
    winner = fight(*make_armies(INPUT))
    ans = sum(g.units for g in winner.groups)
    print(f"Part 1: army {winner.name} wins with {ans} units")


def run_boosted_fight(boost):
    immune, infection = make_armies(INPUT)
    for group in immune.groups:
        group.damage += boost
    winner = fight(immune, infection)
    return winner

def part2():
    for boost in itertools.count():
        try:
            winner = run_boosted_fight(boost)
        except Stalemate:
            print(f"Boost {boost}: stalemate")
        else:
            print(f"Boost {boost}: army {winner.name} wins")
            if winner.name == "immune":
                break
    remaining = sum(g.units for g in winner.groups)
    print(f"Boost {boost}: army {winner.name} wins with {remaining} units")

if __name__ == "__main__":
    part2()
