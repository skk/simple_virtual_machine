import simplevirtualmachine.bytecodes.instruction

class LOAD(simplevirtualmachine.bytecodes.instruction.Instruction):
    """LOAD instruction."""
    def __init__(self):
        super(LOAD, self).__init__(10, 1)


