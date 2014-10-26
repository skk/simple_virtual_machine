import simplevirtualmachine.bytecodes.instruction

class BR(simplevirtualmachine.bytecodes.instruction.Instruction):
    """BR instruction."""
    def __init__(self):
        super(BR, self).__init__(6, 1)


