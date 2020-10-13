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
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[MUL] = self.handle_mul
    
    def handle_ldi(self, instruction, op_a, op_b):
        self.reg[op_a] = op_b
    def handle_prn(self, instruction, op_a, op_b):
        print(self.reg[op_a])
    def handle_hlt(self, instruction, op_a, op_b):
        self.halted = True
    def handle_mul(self, instruction, op_a, op_b):
        self.alu(instruction, op_a, op_b)

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
                        self.ram_write(x, address)
                        address += 1
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
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            op_size = (instruction >> 6) + 1

            # if instruction == HLT:
            #     self.halted = True
            # elif instruction == LDI:
            #     address = self.ram_read(self.pc + 1)
            #     value = self.ram_read(self.pc + 2)
            #     self.reg[address] = value
            # elif instruction == PRN:
            #     value = self.ram_read(self.pc + 1)
            #     print(self.reg[value])
            # elif ((instruction >> 5) & 0b1):
            #     val_1 = self.ram_read(self.pc + 1)
            #     val_2 = self.ram_read(self.pc + 2)
            #     self.alu(instruction, val_1, val_2)
            self.branchtable[instruction](instruction, operand_a, operand_b)
            
            self.pc += op_size

