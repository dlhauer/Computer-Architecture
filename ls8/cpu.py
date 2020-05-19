
import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        address = 0
        program = []
        f = open(f'ls8/{sys.argv[1]}', 'r')
        program = f.read().split('\n')
        program = [int(line.split('#')[0], 2) for line in program if line != '' and line[0] != '#']

        for instruction in program:
            self.ram_write(instruction, address)
            address += 1

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

        print()

    def run(self):
        self.pc = 0
        halted = False

        while not halted:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            op_count = IR >> 6

            if IR == LDI:
                self.reg[operand_a] = operand_b
            elif IR == PRN:
                print(self.reg[operand_a])
            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)
            elif IR == HLT:
                halted = True
            
            self.pc += op_count+1
        
