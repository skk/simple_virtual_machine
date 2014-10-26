from simplevirtualmachine.bytecodes.bytecodes import *

def test_invalid():
    assert INVALID().opcode == 0
    assert INVALID().operand_count == 0

def test_iadd():
    assert IADD().opcode == 1
    assert IADD().operand_count == 0

def test_isub():
    assert ISUB().opcode == 2
    assert ISUB().operand_count == 0

def test_imul():
    assert IMUL().opcode == 3
    assert IMUL().operand_count == 0

def test_iil():
    assert IIL().opcode == 4
    assert IIL().operand_count == 0

def test_ieq():
    assert IEQ().opcode == 5
    assert IEQ().operand_count == 0

def test_br():
    assert BR().opcode == 6
    assert BR().operand_count == 1

def test_brt():
    assert BRT().opcode == 7
    assert BRT().operand_count == 1
    
def test_brf():
    assert BRF().opcode == 8
    assert BRF().operand_count == 1
   
def test_iconst():
    assert ICONST().opcode == 9
    assert ICONST().operand_count == 1

def test_load():
    assert LOAD().opcode == 10
    assert LOAD().operand_count == 1

def test_gload():
    assert GLOAD().opcode == 11
    assert GLOAD().operand_count == 1

def test_store():
    assert STORE().opcode == 12
    assert STORE().operand_count == 1

def test_gstore():
    assert GSTORE().opcode == 13
    assert GSTORE().operand_count == 1

def test_puts():
    assert PUTS().opcode == 14
    assert PUTS().operand_count == 0

def test_pop():
    assert POP().opcode == 15
    assert POP().operand_count == 1

def test_call():
    assert CALL().opcode == 16
    assert CALL().operand_count == 1
 
def test_ret():
    assert RET().opcode == 17
    assert RET().operand_count == 1

def test_halt():
    assert HALT().opcode == 18
    assert HALT().operand_count == 0

