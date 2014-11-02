# -*- coding: utf-8 -*-

import logging

from simplevirtualmachine.bytecodes import INVALID, IADD, ISUB, IMUL, \
    IEQ, ILT, ICONST, LOAD, GLOAD, STORE, GSTORE, \
    PUTS, POP, CALL, RET, HALT, BR, BRT, BRF, InvalidBytecodeError
from simplevirtualmachine.vm import VM

logger = logging.getLogger(__name__)


def vm_test_helper(*vm_code, **vm_kwargs):

    if 'trace' in vm_kwargs:
        trace = vm_kwargs['trace']
        del vm_kwargs['trace']
    else:
        trace = False

    if 'capsys' in vm_kwargs:
        capsys = vm_kwargs['capsys']
        del vm_kwargs['capsys']
    else:
        capsys = None

    vm = VM(*vm_code, **vm_kwargs)
    rv = vm.run()

    (out, err) = (None, None)
    if capsys is not None:
        out, err = capsys.readouterr()
    if trace:
        logger.info("\nOUT:\n{}\nERR:\n{}".format(out, err))

    return (rv, out, err)


def test_halt():
    assert VM(HALT).run() == HALT


def test_invalid():
    try:
        (rv, out, err) = vm_test_helper(INVALID)
    except InvalidBytecodeError as e:
        logger.debug(e)
        rv = e.bytecode
    else:
        # vm should return INVALID bytecode
        assert rv == INVALID


def test_brt_and_ieq(capsys):
        # bytecodes            # address
    (rv, out, err) = vm_test_helper(
        ICONST,                 # 0
        20141118,               # 1
        PUTS,                   # 2
        HALT,                   # 3
        ICONST,                 # 4
        228,                    # 5
        ICONST,                 # 6
        228,                    # 7
        IEQ,                    # 8
        BRT,                    # 9
        0,                      # 10
        start_ip=4,
        capsys=capsys, trace=True)

    # vm should output 100
    assert out == "OUTPUT: {}\n".format(20141118)

    # should halt
    assert rv == HALT


def test_pop(capsys):
    (rv, out, err) = vm_test_helper(
        # store 111111 in global-data storage
        ICONST, 111111,
        GSTORE, 0,
        ICONST, 140,
        ICONST, 88,
        IADD,
        # load item 0 and push onto stack
        GLOAD, 0,
        # pop top of stack
        POP,
        PUTS, HALT,
        capsys=capsys)


    # vm should output 228
    assert out == "OUTPUT: {}\n".format(228)

    # should halt
    assert rv == HALT


def test_load_and_halt(capsys):
    (rv, out, err) = vm_test_helper(
        ICONST, 100, PUTS, HALT,
        capsys=capsys)

    # vm should output 100
    assert out == "OUTPUT: {}\n".format(100)

    # should halt
    assert rv == HALT


def test_load_two_constants_and_halt(capsys):
    (rv, out, err) = vm_test_helper(
        ICONST, 30, ICONST, 42, PUTS, PUTS, HALT,
        capsys=capsys)

    # vm should output 1 and 2
    assert out == "OUTPUT: {}\nOUTPUT: {}\n".format(42, 30)

    # should halt
    assert rv == HALT


def test_load_two_constants_add_and_halt(capsys):
    (rv, out, err) = vm_test_helper(ICONST, 30,
                                    ICONST, 12,
                                    IADD, PUTS, HALT,
                                    capsys=capsys)

    # vm should output 42
    assert out == "OUTPUT: {}\n".format(42)  # 42 = 30+12

    # should halt
    assert rv == HALT


def test_load_two_constants_mul_and_halt(capsys):
    (rv, out, err) = vm_test_helper(ICONST, 2,
                                    ICONST, 8,
                                    IMUL, PUTS, HALT,
                                    capsys=capsys)

    # vm should output 16
    assert out == "OUTPUT: {}\n".format(16)  # 16 = 2 * 8

    # should halt
    assert rv == HALT


def test_load_two_constants_sub_and_halt_neg_result(capsys):
    (rv, out, err) = vm_test_helper(ICONST, 14,
                                    ICONST, 20,
                                    ISUB, PUTS, HALT, capsys=capsys)

    # vm should output -6
    assert out == "OUTPUT: {}\n".format(-6)  # -6 = 14 - 20

    # and should halt
    assert rv == HALT


def test_load_two_constants_sub_and_halt_pos_result(capsys):
    (rv, out, err) = vm_test_helper(ICONST, 51,
                                    ICONST, 23,
                                    ISUB, PUTS, HALT, capsys=capsys)

    # vm should output 28
    assert out == "OUTPUT: {}\n".format(28)  # 28 = 51 - 23

    # and should halt
    assert rv == HALT


def test_gstore_and_gload(capsys):
    (rv, out, err) = vm_test_helper(ICONST, 99,
                                    GSTORE, 0,
                                    GLOAD, 0,
                                    PUTS, HALT, capsys=capsys)
    # vm should output 28
    assert out == "OUTPUT: 99\n"

    # and should halt
    assert rv == HALT


def test_store_and_load(capsys):
    (rv, out, err) = vm_test_helper(ICONST, 1980,
                                    STORE, 0,
                                    LOAD, 0,
                                    PUTS, HALT, capsys=capsys)
    # vm should output 1980
    assert out == "OUTPUT: 1980\n"

    # and should halt
    assert rv == HALT


def test_loop(capsys):
    (rv, out, err) = vm_test_helper(
        # .GLOBALS; N (CodeIndex: 0), I (CodeIndex: 1)
        # N = 13           ADDRESS
        ICONST, 13,            # 0
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
        GLOAD, 1,              # 24
        PUTS,
        HALT,                   # 27
        capsys=capsys
    )
    # vm should output 13
    assert out == "OUTPUT: 13\n"

    # should halt
    assert rv == HALT


def test_factorial_1(capsys):
    __test_factorial(capsys, 1)


def test_factorial_5(capsys):
    __test_factorial(capsys, 5)


def test_factorial_10(capsys):
    __test_factorial(capsys, 10)


def test_factorial_100(capsys):
    __test_factorial(capsys, 100)


def __test_factorial(capsys, n):
    import math
    result = math.factorial(n)

    (rv, out, err) = vm_test_helper(
        # def FACT: ARGS=1, LOCALS=0      # ADDRESS
        # IF N < 2 RETURN 1
        LOAD, -3,                               # 0
        ICONST, 2,                              # 2
        ILT,                                    # 4
        BRF, 10,                                # 5
        ICONST, 1,                              # 7
        RET,                                    # 9
        # CONT
        # RETURN N * FACT(N-1)
        LOAD, -3,                               # 10
        LOAD, -3,                               # 12
        ICONST, 1,                              # 14
        ISUB,                                   # 16
        CALL, 0, 1,                             # 17
        IMUL,                                   # 20
        RET,                                    # 21
        # def MAIN ARGS=0, LOCALS=0
        # print FACT( n )
        ICONST, n,                              # 22    # MAIN METHOD
        CALL, 0, 1,                             # 24
        PUTS,                                   # 27
        HALT,                                   # 28
        capsys=capsys,
        start_ip=22, stack_size=1000
    )
    assert out == "OUTPUT: {}\n".format(result)

    # should halt
    assert rv == HALT
