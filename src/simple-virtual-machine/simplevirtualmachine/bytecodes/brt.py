import simplevirtualmachine.bytecodes.instruction

class BRT(simplevirtualmachine.bytecodes.instruction.Instruction):
    """BRT instruction."""
    def __init__(self):
        super(BRT, self).__init__(7, 1)


