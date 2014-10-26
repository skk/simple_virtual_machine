import simplevirtualmachine.bytecodes.instruction

class CALL(simplevirtualmachine.bytecodes.instruction.Instruction):
    """CALL instruction."""
    def __init__(self):
        super(CALL, self).__init__(16, 1)


