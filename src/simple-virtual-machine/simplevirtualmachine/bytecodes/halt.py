import simplevirtualmachine.bytecodes.instruction

class HALT(simplevirtualmachine.bytecodes.instruction.Instruction):
    """HALT instruction."""
    def __init__(self):
        super(HALT, self).__init__(18)


