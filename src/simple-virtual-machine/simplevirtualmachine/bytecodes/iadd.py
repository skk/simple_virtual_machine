import simplevirtualmachine.bytecodes.instruction

class IADD(simplevirtualmachine.bytecodes.instruction.Instruction):
    """IADD instruction."""
    def __init__(self):
        super(IADD, self).__init__(1)


