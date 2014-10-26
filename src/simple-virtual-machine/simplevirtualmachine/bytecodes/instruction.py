class Instruction(object):
    """ An instruction in our simplevirtualmachine."""
    
    def __init__(self, opcode, operand_count = 0):
        self.opcode = opcode
        self.operand_count = operand_count

    def __str__(self):
        return "opcode: {0}, operand_count: {1}".format(
            self.opcode, self.operand_count)

