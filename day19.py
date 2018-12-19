# https://adventofcode.com/2018/day/19

from day16 import (
    addr, addi, mulr, muli, banr, bani, borr, bori,
    setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr,
    )

INPUT = """\
#ip 2
addi 2 16 2
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
seti 2 8 2
addi 5 1 5
gtrr 5 1 4
addr 4 2 2
seti 1 5 2
mulr 2 2 2
addi 1 2 1
mulr 1 1 1
mulr 2 1 1
muli 1 11 1
addi 4 3 4
mulr 4 2 4
addi 4 7 4
addr 1 4 1
addr 2 0 2
seti 0 4 2
setr 2 8 4
mulr 4 2 4
addr 2 4 4
mulr 2 4 4
muli 4 14 4
mulr 4 2 4
addr 1 4 1
seti 0 5 0
seti 0 8 2
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
            parts = line.split()
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

def test_device():
    device = Device()
    device.read_program(TEST_INPUT)
    device.run()
    assert device.regs[5] == 9
    assert device.ip == 7

if __name__ == "__main__":
    device = Device()
    device.read_program(INPUT)
    device.run()
    print(f"Part 1: register 0 is {device.regs[0]}")
