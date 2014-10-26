import simplevirtualmachine.bytecodes.instruction

class STORE(simplevirtualmachine.bytecodes.instruction.Instruction):
    """STORE instruction."""
    def __init__(self):
        super(STORE, self).__init__(12, 1)


