# -*- coding: utf-8 -*-

import logging

from simplevirtualmachine.bytecodes.bytecodes import INVALID, IADD, ISUB, IMUL, \
    IEQ, ILT, ICONST, LOAD, GLOAD, STORE, GSTORE, \
    PUTS, POP, CALL, RET, HALT, BR, BRT, BRF
from simplevirtualmachine.bytecodes.instruction import InvalidInstructionError
from simplevirtualmachine.vm import VM

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
 

def test_halt():
    assert VM([HALT]).run() == HALT


def test_invalid():
    vm = VM([INVALID])
    rv = None
    try:
        rv = vm.run()
    except InvalidInstructionError as e:
        logger.debug(e)
        rv = e.bytecode
    else:
        assert rv == INVALID


def test_load_and_halt():
    vm = VM([ICONST, 100, HALT])
    rv = vm.run()

    # stack should load 100
    assert vm.stack[vm.sp] == 100

    # should halt
    assert rv == HALT


def test_load_two_constants():
    vm = VM([ICONST, 1, ICONST, 2, HALT])
    rv = vm.run()

    # stack should load 1 and 2
    assert vm.stack[vm.sp - 1] == 1
    assert vm.stack[vm.sp] == 2

    # should halt
    assert rv == HALT


def test_load_two_constants_add_and_halt():
    vm = VM([ICONST, 1, ICONST, 2, IADD, PUTS, HALT])
    rv = vm.run()

    # stack should have result of IADD
    assert vm.stack[vm.sp] == 1 + 2

    # should halt
    assert rv == HALT


def test_load_two_constants_mul_and_halt():
    vm = VM([ICONST, 2, ICONST, 8, IMUL, PUTS, HALT])
    rv = vm.run()

    # stack should have result of IMUL
    assert vm.stack[vm.sp] == 2 * 8

    # should halt
    assert rv == HALT


def test_load_two_constants_sub_and_halt_neg_result():
    vm = VM([ICONST, 14, ICONST, 20, ISUB, PUTS, HALT])
    rv = vm.run()

    # stack should have result of ISUB
    assert vm.stack[vm.sp] == 14 - 20

    # should halt
    assert rv == HALT


def test_load_two_constants_sub_and_halt_pos_result():
    vm = VM([ICONST, 51, ICONST, 23, ISUB, PUTS, HALT])
    rv = vm.run()

    # stack should have result of ISUB
    assert vm.stack[vm.sp] == 51 - 23

    # should halt
    assert rv == HALT
    
  
def _test_loop():
    instructions = [
        # .GLOBALS 2; N, I
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
    ]
    vm = VM(instructions)
    rv = vm.run()

    # should halt
    assert rv == HALT

