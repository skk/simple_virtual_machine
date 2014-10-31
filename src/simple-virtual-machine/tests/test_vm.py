# -*- coding: utf-8 -*-

import logging

from simplevirtualmachine.bytecodes import INVALID, IADD, ISUB, IMUL, \
    IEQ, ILT, ICONST, LOAD, GLOAD, STORE, GSTORE, \
    PUTS, POP, CALL, RET, HALT, BR, BRT, BRF, InvalidBytecodeError
from simplevirtualmachine.vm import VM

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
 

def test_halt():
    assert VM(HALT).run() == HALT


def test_invalid():
    vm = VM(INVALID)
    rv = None
    try:
        rv = vm.run()
    except InvalidBytecodeError as e:
        logger.debug(e)
        rv = e.bytecode
    else:
        # vm should return INVALID bytecode
        assert rv == INVALID


def test_load_and_halt(capsys):
    vm = VM(ICONST, 100, PUTS, HALT)
    rv = vm.run()

    # vm should output be 100
    out, err = capsys.readouterr()
    assert out == "OUTPUT: {}\n".format(100)

    # should halt
    assert rv == HALT


def test_load_two_constants(capsys):
    vm = VM(ICONST, 1, ICONST, 2, PUTS, PUTS, HALT)
    rv = vm.run()

    # vm should output be 1 and 2
    out, err = capsys.readouterr()
    assert out == "OUTPUT: {}\nOUTPUT: {}\n".format(2, 1)

    # should halt
    assert rv == HALT


def test_load_two_constants_add_and_halt(capsys):
    vm = VM(ICONST, 1, ICONST, 2, IADD, PUTS, HALT)
    rv = vm.run()

    # vm should output be 3
    out, err = capsys.readouterr()
    assert out == "OUTPUT: {}\n".format(3)  # 1 + 2

    # should halt
    assert rv == HALT


def test_load_two_constants_mul_and_halt(capsys):
    vm = VM(ICONST, 2, ICONST, 8, IMUL, PUTS, HALT)
    rv = vm.run()

    # vm should output be -6
    out, err = capsys.readouterr()
    assert out == "OUTPUT: {}\n".format(16)  # 2 * 8

    # should halt
    assert rv == HALT


def test_load_two_constants_sub_and_halt_neg_result(capsys):
    vm = VM(ICONST, 14, ICONST, 20, ISUB, PUTS, HALT)
    rv = vm.run()

    # vm should output be -6
    out, err = capsys.readouterr()
    assert out == "OUTPUT: {}\n".format(-6)  # 14 - 20

    # and should halt
    assert rv == HALT


def test_load_two_constants_sub_and_halt_pos_result(capsys):
    vm = VM(ICONST, 51, ICONST, 23, ISUB, PUTS, HALT)
    rv = vm.run()

    # vm should output be 28
    out, err = capsys.readouterr()
    assert out == "OUTPUT: {}\n".format(28)  # 51 - 23

    # and should halt
    assert rv == HALT
    

def test_gstore_and_gload(capsys):
    vm = VM(ICONST, 99,
            GSTORE, 0,
            GLOAD, 0,
            PUTS, HALT)
    rv = vm.run()
    
    out, err = capsys.readouterr()
    # vm should output be 28
    assert out == "OUTPUT: 99\n"

    # and should halt
    assert rv == HALT
    
    
def test_loop():
    vm = VM(
        # .GLOBALS; N (CodeIndex: 0), I (CodeIndex: 1)
        # N = 10           ADDRESS
        ICONST, 10,            # 0
        GSTORE, 0,             # 2
        # I = 0
        ICONST, 0,             # 4
        GSTORE, 1,             # 6
        # WHILE I<N:
        # START (8):
        GLOAD, 1,              # 8
        GLOAD, 0,              # 10
        ILT,                   # 12
        BRF, 24,               # 13
        #     I = I + 1
        GLOAD, 1,              # 15
        ICONST, 1,             # 17
        IADD,                  # 19
        GSTORE, 1,             # 20
        BR, 8,                 # 22
        # DONE (24):
        # PRINT "LOOPED "+N+" TIMES."
        HALT                   # 24
    )
    rv = vm.run()

    # should halt
    assert rv == HALT

