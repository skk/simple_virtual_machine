import simplevirtualmachine.bytecodes.instruction

class POP(simplevirtualmachine.bytecodes.instruction.Instruction):
    """POP instruction."""
    def __init__(self):
        super(POP, self).__init__(15, 1)


