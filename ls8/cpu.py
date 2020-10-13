"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.reg[7] = 0xF4
        self.halted = False

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
        

    def load(self, argv):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print("Incorrect Command Line Args")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0]
                    try:
                        x = int(num, 2)
                        # print("{:08b}: {:d}".format(x,x))
                        self.ram[address] = x
                        address += 1
                        # print(x)
                    except:
                        continue
        except:
            print("File Not Found")
            sys.exit(1)
        


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        if op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # ir = []
        while not self.halted:
            instruction = self.ram_read(self.pc)

            if instruction == HLT:
                self.halted = True
                self.pc += 1
            elif instruction == LDI:
                address = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.reg[address] = value
                self.pc += 3
            elif instruction == PRN:
                value = self.ram_read(self.pc + 1)
                print(self.reg[value])
                self.pc += 2
            elif ((instruction >> 5) & 0b1):
                val_1 = self.ram_read(self.pc + 1)
                val_2 = self.ram_read(self.pc + 2)
                self.alu(instruction, val_1, val_2)
                self.pc += 3

