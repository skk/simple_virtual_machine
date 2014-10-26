import simplevirtualmachine.bytecodes.instruction

class GLOAD(simplevirtualmachine.bytecodes.instruction.Instruction):
    """GLOAD instruction."""
    def __init__(self):
        super(GLOAD, self).__init__(11, 1)


