"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.reg[7] = 0xF4
        self.halted = False
        self.branchtable = {}       ## Lambda expression to add entries?
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[MUL] = self.alu
        self.branchtable[ADD] = self.alu
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret
        # self.sp = 0xF4
    
    def handle_ldi(self, instruction, op_a, op_b):
        self.reg[op_a] = op_b

    def handle_prn(self, instruction, op_a, op_b):
        print(self.reg[op_a])

    def handle_hlt(self, instruction, op_a, op_b):
        self.halted = True

    def pop(self, instruction, op_a, op_b):
        sp = self.reg[7]
        value = self.ram[sp]
        self.reg[op_a] = value
        self.reg[7] += 1
        
    def push(self, instruction, op_a, op_b):
        self.reg[7] -= 1
        value = self.reg[op_a]
        self.ram[self.reg[7]] = value

        # print(self.ram[0xf0:0xf4])
    def call(self, instruction, op_a, op_b):
        # self.push(instruction, op_b, op_a)
        # self.pc = self.reg[op_a]
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.pc + 2
        self.pc = self.reg[op_a]
        
    def ret(self, instruction, op_a, op_b):
        # self.pop(op_a, instruction, op_b)
        returnAddress = self.ram[self.reg[7]]
        self.ram[self.reg[7]] += 1
        self.pc = returnAddress

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
        

    def load(self, argv):
        """Load a program into memory."""

        address = 0

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

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]

        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception(f"Unsupported ALU operation: {op}")
            

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

            self.branchtable[instruction](instruction, operand_a, operand_b)
            
            if not(instruction == CALL or instruction == RET):
                self.pc += op_size

