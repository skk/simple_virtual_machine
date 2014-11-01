class InvalidBytecodeError(Exception):
    def __init__(self, bytecode):
        self.bytecode = bytecode

    def __str__(self):
        return repr(self.bytecode)
        
        
class Bytecode(object):
    """ A bytecode in our simple virtual machine."""
    opcodes = {}
            
    def __init__(self, name, opcode, operand_count=0):
        self.name = name
        self.opcode = opcode
        self.operand_count = operand_count
        Bytecode.opcodes[self.opcode] = self
                
    def __str__(self):
        return "Bytecode name: {}\topcode: {:02d}\toperand_count: {:02d}".format(self.name.ljust(10), self.opcode, self.operand_count)

    def dump_bytecode(self):
        return "{}".format(self.name.ljust(10))
                
    @classmethod
    def to_instruction_from_opcode(cls, opcode):
        return cls.opcodes[opcode]


INVALID = Bytecode("INVALID", 0)
IADD = Bytecode("IADD", 1)
ISUB = Bytecode("ISUB", 2)
IMUL = Bytecode("IMUL", 3)
IEQ = Bytecode("IEQ", 5)
ILT = Bytecode("IIT", 4)
BR = Bytecode("BR", 6, 1)
BRT = Bytecode("BRR", 7, 1)
BRF = Bytecode("BRF", 8, 1)
ICONST = Bytecode("ICONST", 9, 1)
LOAD = Bytecode("LOAD", 10, 1)
GLOAD = Bytecode("GLOAD", 11, 1)
STORE = Bytecode("STORE", 12, 1)
GSTORE = Bytecode("GSTORE", 13, 1)
PUTS = Bytecode("PUTS", 14)
POP = Bytecode("POP", 15, 1)
CALL = Bytecode("CALL", 16, 2)
RET = Bytecode("RET", 17, 1)
HALT = Bytecode("HALT", 18)
