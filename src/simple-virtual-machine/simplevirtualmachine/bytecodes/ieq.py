import simplevirtualmachine.bytecodes.instruction

class IEQ(simplevirtualmachine.bytecodes.instruction.Instruction):
    """IEQ instruction."""
    def __init__(self):
        super(IEQ, self).__init__(5)


