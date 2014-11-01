from simplevirtualmachine.bytecodes import INVALID, IADD, ISUB, IMUL, \
    IEQ, ILT, BR, BRT, BRF, ICONST, LOAD, GLOAD, STORE, GSTORE, \
    PUTS, POP, CALL, RET, HALT


def test_invalid():
    assert INVALID.opcode == 0 and INVALID.operand_count == 0


def test_iadd():
    assert IADD.opcode == 1 and IADD.operand_count == 0


def test_isub():
    assert ISUB.opcode == 2 and ISUB.operand_count == 0


def test_imul():
    assert IMUL.opcode == 3 and IMUL.operand_count == 0


def test_ilt():
    assert ILT.opcode == 4 and ILT.operand_count == 0


def test_ieq():
    assert IEQ.opcode == 5 and IEQ.operand_count == 0


def test_br():
    assert BR.opcode == 6 and BR.operand_count == 1


def test_brt():
    assert BRT.opcode == 7 and BRT.operand_count == 1
    

def test_brf():
    assert BRF.opcode == 8 and BRF.operand_count == 1
   

def test_iconst():
    assert ICONST.opcode == 9 and ICONST.operand_count == 1


def test_load():
    assert LOAD.opcode == 10 and LOAD.operand_count == 1


def test_gload():
    assert GLOAD.opcode == 11 and GLOAD.operand_count == 1


def test_store():
    assert STORE.opcode == 12 and STORE.operand_count == 1


def test_gstore():
    assert GSTORE.opcode == 13 and GSTORE.operand_count == 1


def test_puts():
    assert PUTS.opcode == 14 and PUTS.operand_count == 0


def test_pop():
    assert POP.opcode == 15 and POP.operand_count == 1


def test_call():
    assert CALL.opcode == 16 and CALL.operand_count == 2
 

def test_ret():
    assert RET.opcode == 17 and RET.operand_count == 0


def test_halt():
    assert HALT.opcode == 18 and HALT.operand_count == 0
    
    
