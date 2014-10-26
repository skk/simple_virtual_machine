import simplevirtualmachine.bytecodes.instruction

class PUTS(simplevirtualmachine.bytecodes.instruction.Instruction):
    """PUTS instruction."""
    def __init__(self):
        super(PUTS, self).__init__(14)


