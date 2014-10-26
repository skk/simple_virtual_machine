import simplevirtualmachine.bytecodes.instruction

class BRF(simplevirtualmachine.bytecodes.instruction.Instruction):
    """BRF instruction."""
    def __init__(self):
        super(BRF, self).__init__(8, 1)


