import simplevirtualmachine.bytecodes.instruction

class RET(simplevirtualmachine.bytecodes.instruction.Instruction):
    """RET instruction."""
    def __init__(self):
        super(RET, self).__init__(17, 1)


