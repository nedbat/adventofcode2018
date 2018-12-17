# https://adventofcode.com/2018/day/16

import ast

# Opcodes

A, B, C = 1, 2, 3

def addr(inst, before, after):
    after[inst[C]] = before[inst[A]] + before[inst[B]]

def addi(inst, before, after):
    after[inst[C]] = before[inst[A]] + inst[B]

def mulr(inst, before, after):
    after[inst[C]] = before[inst[A]] * before[inst[B]]

def muli(inst, before, after):
    after[inst[C]] = before[inst[A]] * inst[B]

def banr(inst, before, after):
    after[inst[C]] = before[inst[A]] & before[inst[B]]

def bani(inst, before, after):
    after[inst[C]] = before[inst[A]] & inst[B]

def borr(inst, before, after):
    after[inst[C]] = before[inst[A]] | before[inst[B]]

def bori(inst, before, after):
    after[inst[C]] = before[inst[A]] | inst[B]

def setr(inst, before, after):
    after[inst[C]] = before[inst[A]]

def seti(inst, before, after):
    after[inst[C]] = inst[A]

def gtir(inst, before, after):
    after[inst[C]] = int(inst[A] > before[inst[B]])

def gtri(inst, before, after):
    after[inst[C]] = int(before[inst[A]] > inst[B])

def gtrr(inst, before, after):
    after[inst[C]] = int(before[inst[A]] > before[inst[B]])

def eqir(inst, before, after):
    after[inst[C]] = int(inst[A] == before[inst[B]])

def eqri(inst, before, after):
    after[inst[C]] = int(before[inst[A]] == inst[B])

def eqrr(inst, before, after):
    after[inst[C]] = int(before[inst[A]] == before[inst[B]])

ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

def read_input1():
    triples = []
    before = inst = after = None
    with open("day16_input1.txt") as f:
        for line in f:
            if line.startswith("Before:"):
                assert before is None
                before = ast.literal_eval(line.partition(":")[2].strip())
            elif line.startswith("After:"):
                assert after is None
                after = ast.literal_eval(line.partition(":")[2].strip())
                assert before is not None
                assert inst is not None
                triples.append((before, inst, after))
                before = inst = after = None
            elif line.strip():
                assert inst is None
                inst = list(map(int, line.split()))
    return triples

def run_opcode(op, inst, before):
    after = list(before)
    op(inst, before, after)
    return after

def possible_ops(before, inst, after):
    possible = set()
    for op in ops:
        actual_after = run_opcode(op, inst, before)
        same = (actual_after == after)
        #print(f"{op.__name__}: b{before} i{inst}: a{after} {'==' if same else '!='} aa{actual_after}")
        if same:
            possible.add(op)
    return possible

def test_possible_ops():
    possible = possible_ops([3,2,1,1], [9,2,1,2], [3,2,2,1])
    assert possible == {mulr, addi, seti}

def part1():
    triples = read_input1()
    three_or_more = 0
    for before, inst, after in triples:
        possible = possible_ops(before, inst, after)
        if len(possible) >= 3:
            three_or_more += 1
    print(f"Part 1: {three_or_more} samples behave like three or more opcodes")

if __name__ == "__main__":
    part1()
