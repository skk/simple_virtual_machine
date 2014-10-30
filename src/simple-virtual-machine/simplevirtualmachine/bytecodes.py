class InvalidBytecodeError(Exception):
    def __init__(self, bytecode):
        self.bytecode = bytecode

    def __str__(self):
        return repr(self.bytecode)
        
        
class Bytecode(object):
    """ A bytecode in our simple virtual machine."""
    opcodes = {}
            
    def __init__(self, opcode, operand_count=0):
        self.opcode = opcode
        self.operand_count = operand_count
        Bytecode.opcodes[self] = self
                
    def __str__(self):
        return "opcode: {0}, operand_count: {1}".format(
            self.opcode, self.operand_count)
                
    @classmethod
    def to_instruction_from_opcode(cls, opcode):
        return cls.opcodes[opcode]


INVALID = Bytecode(0)
IADD = Bytecode(1)
ISUB = Bytecode(2)
IMUL = Bytecode(3)
IEQ = Bytecode(5)
ILT = Bytecode(4)
BR = Bytecode(6, 1)
BRT = Bytecode(7, 1)
BRF = Bytecode(8, 1)
ICONST = Bytecode(9, 1)
LOAD = Bytecode(10, 1)
GLOAD = Bytecode(11, 1)
STORE = Bytecode(12, 1)
GSTORE = Bytecode(13, 1)
PUTS = Bytecode(14)
POP = Bytecode(15, 1)
CALL = Bytecode(16, 1)
RET = Bytecode(17, 1)
HALT = Bytecode(18)
