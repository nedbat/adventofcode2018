# https://adventofcode.com/2018/day/19

from day16 import (
    addr, addi, mulr, muli, banr, bani, borr, bori,
    setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr,
    A, B, C,
    )

INPUT = """\
#ip 2
addi 2 16 2     # 0: rjump to 17
seti 1 1 5
seti 1 1 3
mulr 5 3 4
eqrr 4 1 4
addr 4 2 2
addi 2 1 2
addr 5 0 0
addi 3 1 3
gtrr 3 1 4
addr 2 4 2
seti 2 8 2      # jump to 3
addi 5 1 5
gtrr 5 1 4
addr 4 2 2
seti 1 5 2      # jump to 2
mulr 2 2 2
addi 1 2 1      # 17:
mulr 1 1 1
mulr 2 1 1
muli 1 11 1
addi 4 3 4
mulr 4 2 4
addi 4 7 4
addr 1 4 1
addr 2 0 2
seti 0 4 2      # jump to 1
setr 2 8 4
mulr 4 2 4
addr 2 4 4
mulr 2 4 4
muli 4 14 4
mulr 4 2 4
addr 1 4 1
seti 0 5 0
seti 0 8 2      # jump to 1
""".splitlines()

TEST_INPUT = """\
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""".splitlines()

class Device:
    def __init__(self):
        self.regs = [0] * 6
        self.ipreg = None
        self.prog = None

    def read_program(self, lines):
        assert lines[0].startswith("#ip ")
        self.ipreg = int(lines[0].split()[-1])
        self.prog = []
        for line in lines[1:]:
            parts = line.split()[:4]
            opfunc = globals()[parts[0]]
            inst = (opfunc,) + tuple(map(int, parts[1:]))
            self.prog.append(inst)

    @property
    def ip(self):
        return self.regs[self.ipreg]

    @ip.setter
    def ip(self, val):
        self.regs[self.ipreg] = val

    def run(self):
        self.ip = 0
        while True:
            inst = self.prog[self.ip]
            after = list(self.regs)
            inst[0](inst, self.regs, after)
            self.regs = after
            self.ip += 1
            if not (0 <= self.ip < len(self.prog)):
                break

    def disassemble(self):
        ipreg = self.ipreg
        for loc, inst in enumerate(self.prog):
            inst = list(inst)
            op = inst[0]
            opname = op.__name__
            operands = " ".join(map(str, inst[1:]))
            comment = ""
            if op in [addi, muli]:
                if op == addi:
                    operator = "+"
                elif op == muli:
                    operator = "*"
                if inst[A] == ipreg and inst[C] == ipreg:
                    assert op == addi
                    dest = loc + inst[B] + 1
                    comment = f"jump to {dest}"
                elif inst[A] == inst[C]:
                    comment = f"r{inst[C]} {operator}= {inst[B]}"
                else:
                    comment = f"r{inst[C]} = r{inst[A]} {operator} {inst[B]}"
            elif op in [addr, mulr]:
                if op == addr:
                    operator = "+"
                elif op == mulr:
                    operator = "*"
                if inst[B] == inst[C]:
                    inst[B], inst[A] = inst[A], inst[B]
                if inst[B] == ipreg:
                    operand = loc
                else:
                    operand = f"r{inst[B]}"
                if inst[A] == inst[C]:
                    comment = f"r{inst[C]} {operator}= {operand}"
                else:
                    comment = f"r{inst[C]} = r{inst[A]} {operator} {operand}"
            elif op == seti:
                if inst[C] == ipreg:
                    dest = inst[A] + 1
                    comment = f"jump to {dest}"
                else:
                    comment = f"r{inst[C]} = {inst[A]}"
            elif op == setr:
                if inst[A] == ipreg:
                    operand = loc
                else:
                    operand = f"r{inst[A]}"
                comment = f"r{inst[C]} = {operand}"
            comch = "#" if comment else ""
            print(f"{loc:2d}: {opname} {operands:20} {comch} {comment}".rstrip())

def test_device():
    device = Device()
    device.read_program(TEST_INPUT)
    device.run()
    assert device.regs[5] == 9
    assert device.ip == 7

def part1():
    device = Device()
    device.read_program(INPUT)
    device.run()
    print(f"Part 1: register 0 is {device.regs[0]}")

def naive_part2():
    device = Device()
    device.read_program(INPUT)
    device.regs[0] = 1
    device.run()
    print(f"Part 2: register 0 is {device.regs[0]}")

def disassemble():
    device = Device()
    device.read_program(INPUT)
    device.disassemble()

if __name__ == "__main__":
    disassemble()
