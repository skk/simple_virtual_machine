class InvalidInstructionError(Exception):
    def __init__(self, bytecode):
        self.bytecode = bytecode

    def __str__(self):
        return repr(self.bytecode)
        
        
class Instruction(object):
    """ An instruction in our simplevirtualmachine."""
    opcodes = {}
            
    def __init__(self, opcode, operand_count=0):
        self.opcode = opcode
        self.operand_count = operand_count
        Instruction.opcodes[self] = self
                
    def __str__(self):
        return "opcode: {0}, operand_count: {1}".format(
            self.opcode, self.operand_count)
                
    @classmethod
    def to_instruction_from_opcode(cls, opcode):
        return cls.opcodes[opcode]
