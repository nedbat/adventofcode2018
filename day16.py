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

def decode_ops():
    # At first, any opcode could be any operation
    possibilities = [set(ops) for _ in range(16)]

    # Pass one: what opcodes can be what operations based on the input?
    for before, inst, after in read_input1():
        possible = possible_ops(before, inst, after)
        possibilities[inst[0]] &= possible

    # Pass two: reduce possibilities based on certainties.
    certains = [None] * 16
    while any(cert is None for cert in certains):
        for iop, (cert, possibles) in enumerate(zip(certains, possibilities)):
            if cert is not None:
                # We already know this one..
                continue
            if len(possibles) == 1:
                op = possibles.pop()
                certains[iop] = op
                for other_poss in possibilities:
                    if len(other_poss) > 1 and op in other_poss:
                        other_poss.remove(op)

    return certains

def read_input2():
    with open("day16_input2.txt") as f:
        return [list(map(int, line.split())) for line in f]

def run_program(opcodes, instructions):
    regs = [0, 0, 0, 0]
    for inst in instructions:
        regs = run_opcode(opcodes[inst[0]], inst, regs)
    return regs

def part2():
    instructions = read_input2()
    opcodes = decode_ops()
    regs = run_program(opcodes, instructions)
    print(f"Part 2: after running the program, register 0 is {regs[0]}")

if __name__ == "__main__":
    part2()
