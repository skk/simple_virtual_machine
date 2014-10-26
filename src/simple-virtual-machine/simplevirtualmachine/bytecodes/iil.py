import simplevirtualmachine.bytecodes.instruction

class IIL(simplevirtualmachine.bytecodes.instruction.Instruction):
    """IIL instruction."""
    def __init__(self):
        super(IIL, self).__init__(4)


