import simplevirtualmachine.bytecodes.instruction

class ICONST(simplevirtualmachine.bytecodes.instruction.Instruction):
    """ICONST instruction."""
    def __init__(self):
        super(ICONST, self).__init__(9, 1)


