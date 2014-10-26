import simplevirtualmachine.bytecodes.instruction

class ISUB(simplevirtualmachine.bytecodes.instruction.Instruction):
    """ISUB instruction."""
    def __init__(self):
        super(ISUB, self).__init__(2)


