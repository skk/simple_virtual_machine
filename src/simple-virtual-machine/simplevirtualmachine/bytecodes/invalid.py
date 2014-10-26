import simplevirtualmachine.bytecodes.instruction

class INVALID(simplevirtualmachine.bytecodes.instruction.Instruction):
    """INVLAID instruction."""
    def __init__(self):
        super(INVALID, self).__init__(0)


