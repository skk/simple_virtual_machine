import simplevirtualmachine.bytecodes.instruction

class GSTORE(simplevirtualmachine.bytecodes.instruction.Instruction):
    """GSTORE instruction."""
    def __init__(self):
        super(GSTORE, self).__init__(13, 1)


