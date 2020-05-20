
import sys

LDI  = 0b10000010
PRN  = 0b01000111
HLT  = 0b00000001
MUL  = 0b10100010
PUSH = 0b01000101
POP  = 0b01000110
SP   = 7

class CPU:

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[SP] = 0xF4 # Initialize stack pointer.
        # self.sp = self.reg[7]
        self.pc = 0
        self.branch_table = {
            LDI: self.handle_ldi,
            PRN: self.handle_prn,
            MUL: self.handle_mul,
            HLT: self.handle_hlt,
            PUSH: self.handle_push,
            POP: self.handle_pop
        }

    def load(self):
        address = 0
        program = []
        f = open(f'ls8/{sys.argv[1]}', 'r')
        program = f.read().split('\n')
        program = [int(line.split('#')[0], 2) for line in program if line != '' and line[0] != '#']

        for instruction in program:
            self.ram_write(instruction, address)
            address += 1

    def handle_ldi(self, reg, val):
        self.reg[reg] = val

    def handle_prn(self, reg, *args):
        print(self.reg[reg])

    def handle_mul(self, reg_a, reg_b):
        self.reg[reg_a] *= self.reg[reg_b]

    def handle_hlt(self, *args):
        exit()

    def handle_push(self, reg, *args):
        self.reg[SP] += 1
        self.ram_write(self.reg[reg], self.reg[SP])

    def handle_pop(self, reg, *args):
        if self.reg[SP] == 0xF4:
            return None
        val = self.ram_read(self.reg[SP])
        self.reg[SP] -= 1
        self.reg[reg] = val

    def ram_read(self, MAR):
        return self.ram[MAR]
        
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
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

    def run(self):
        self.pc = 0
        halted = False

        while not halted:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            op_count = IR >> 6

            self.branch_table[IR](operand_a, operand_b)
            
            self.pc += op_count+1
        
