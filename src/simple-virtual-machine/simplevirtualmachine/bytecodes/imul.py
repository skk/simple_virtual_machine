import simplevirtualmachine.bytecodes.instruction

class IMUL(simplevirtualmachine.bytecodes.instruction.Instruction):
    """IMUL instruction."""
    def __init__(self):
        super(IMUL, self).__init__(3)


