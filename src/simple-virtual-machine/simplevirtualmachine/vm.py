# -*- coding: utf-8 -*-

import logging
import operator

from simplevirtualmachine.bytecodes import INVALID, IADD, ISUB, IMUL, \
    IEQ, ILT, BR, BRT, BRF, ICONST, LOAD, GLOAD, STORE, GSTORE, \
    PUTS, POP, CALL, RET, HALT, Bytecode, InvalidBytecodeError

TRUE = 1
FALSE = 0


class VM(object):
    """Implemenation of a (very) simple virtual machine."""

    def __init__(self, *code, **kwargs):
        if 'stack_size' in kwargs:
            VM.DEFAULT_STACK_SIZE = kwargs['stack_size']
        else:
            VM.DEFAULT_STACK_SIZE = 10000

        if 'start_ip' in kwargs:
            self.ip = kwargs['start_ip']
        else:
            self.ip = 0

        self.fp = -1
        self.sp = -1
        self.code = code
        self.stack = [None for i in range(VM.DEFAULT_STACK_SIZE)]
        self.data = [None for i in range(VM.DEFAULT_STACK_SIZE)]
        self.logger = logging.getLogger(__name__)
        self.logger.info("\n")

    @classmethod
    def format_instr_or_object(cls, obj):
        """Return string with obj formatted as an instruction."""
        if isinstance(obj, Bytecode):
            return Bytecode.to_instruction_from_opcode(obj.opcode)
        else:
            return str(obj)

        return ""

    def binopt(self, opr):
        b = self.stack[self.sp]
        self.sp -= 1
        a = self.stack[self.sp]
        self.sp -= 1

        self.sp += 1
        result = opr(a, b)

        # use 1 or 0 rather than True or False for booleans
        if opr == operator.lt or opr == operator.eq:
            result = TRUE if result else FALSE

        self.logger.debug("binopt: a {} b {} result {} opr {}".format(a, b, result, opr))
        self.stack[self.sp] = result

    def run(self):
        '''Simulate the fetch-decode execute cycle.'''
        # fetch opcode
        opcode = self.code[self.ip]
        rv = HALT

        while opcode != HALT and self.ip <= len(self.code):
            trace = self.display_instruction()
            self.logger.debug("IP {} OPCODE {}".format(self.ip, opcode))
            self.ip += 1

            # decode
            if opcode == IADD:
                self.binopt(operator.add)
            elif opcode == ISUB:
                self.binopt(operator.sub)
            elif opcode == IMUL:
                self.binopt(operator.mul)
            elif opcode == ILT:
                self.binopt(operator.lt)
            elif opcode == IEQ:
                self.binopt(operator.eq)
            elif opcode == BR:
                self.ip = self.code[self.ip]
            elif opcode == BRT:
                addr = self.code[self.ip]
                self.ip += 1
                value = self.stack[self.sp]
                if value == TRUE:
                    self.ip = addr
                self.sp -= 1
            elif opcode == BRF:
                addr = self.code[self.ip]
                self.ip += 1
                value = self.stack[self.sp]
                if value == FALSE:
                    self.ip = addr
                self.sp -= 1
            elif opcode == ICONST:
                self.sp += 1
                self.stack[self.sp] = self.code[self.ip]
                self.ip += 1
            elif opcode == LOAD:
                offset = self.code[self.ip]
                self.ip += 1
                self.sp += 1
                self.stack[self.sp] = self.stack[self.fp + offset]
            elif opcode == GLOAD:
                addr = self.code[self.ip]
                self.ip += 1
                self.sp += 1
                self.stack[self.sp] = self.data[addr]
            elif opcode == STORE:
                offset = self.code[self.ip]
                self.ip += 1
                self.sp -= 1
                self.stack[self.fp + offset] = self.stack[self.sp]
            elif opcode == GSTORE:
                addr = self.code[self.ip]
                self.ip += 1
                self.data[addr] = self.stack[self.sp]
                self.sp -= 1
            elif opcode == PUTS:
                msg = "OUTPUT: {}".format(self.stack[self.sp])
                self.sp -= 1
                print msg
                self.logger.info(msg)
            elif opcode == POP:
                self.sp -= 1
            elif opcode == CALL:
                # target addr of function
                addr = self.code[self.ip]
                self.ip += 1

                # number of args
                number_args = self.code[self.ip]
                self.ip += 1

                # save number of args
                self.sp += 1
                self.stack[self.sp] = number_args

                # save fp
                self.sp += 1
                self.stack[self.sp] = self.fp

                # save return addr
                self.sp += 1
                self.stack[self.sp] = self.ip

                # fp points to return addr on stack
                self.fp = self.sp

                # jump to function
                self.ip = addr

                # self.stack = self.remove_none_from_array(self.stack)
            elif opcode == RET:
                self.logger.debug("RET sp {}".format(self.sp))

                # pop return value
                rvalue = self.stack[self.sp]
                self.sp -= 1

                # self.logger.debug("RET rvalue {}".format(rvalue))
                # self.logger.debug("RET STACK {}".format(self.dump_stack()))
                # self.logger.debug("RET fp {}".format(self.fp))

                # jump over locals to fp
                self.sp = self.fp

                # self.logger.debug("RET sp {}".format(self.sp))

                # restore ip
                self.ip = self.stack[self.sp]
                self.sp -= 1

                # self.logger.debug("RET sp {}".format(self.sp))

                # restore fp
                self.fp = self.stack[self.sp]
                self.sp -= 1

                # self.logger.debug("RET sp {}".format(self.sp))
                # self.logger.debug("RET STACK {}".format(self.dump_stack()))

                # get how many args to throw way
                number_args = self.stack[self.sp]
                self.sp -= 1

                # self.logger.debug("RET sp {}".format(self.sp))
                # self.logger.debug("RET number_args {}".format(number_args))
                # self.logger.debug("RET STACK {}".format(self.dump_stack()))

                # throw away args
                self.sp -= number_args

                self.sp += 1
                self.stack[self.sp] = rvalue

                # self.logger.debug("RET (end) sp {}".format(self.sp))
                # self.logger.debug("RET (end) STACK {}".format(self.dump_stack()))
            elif opcode == HALT:
                rv = HALT
            else:
                rv = INVALID
                raise InvalidBytecodeError("Invalid opcode {opcode} at ip = {ip}".
                                           format(opcode=opcode, ip=self.ip - 1))

            trace += self.dump_stack()
            self.logger.info("{}".format(trace))

            opcode = self.code[self.ip]

        self.print_code_memory()
        self.print_data_memory()
        return rv

    def display_instruction(self):
        '''Dislay instruction'''
        opcode = self.code[self.ip]
        self.logger.debug("opcode {}".format(opcode))
        if not isinstance(opcode, Bytecode):
            return ""

        operands = ""

        self.logger.debug("self.sp {}".format(self.sp))
        self.logger.debug("opcode.name {}".format(opcode.name))
        self.logger.debug("opcode.operand_count {}".format(opcode.operand_count))
        if opcode.operand_count > 0:
            start_idx = self.ip + 1
            end_idx = self.ip + opcode.operand_count
            buf = []
            self.logger.debug("start_idx {} end_idx {}".format(start_idx, end_idx))
            for idx in range(start_idx, end_idx + 1):
                self.logger.debug("INX {} OPERAND: {} ".format(idx, self.code[idx]))
                buf.append(str(self.code[idx]))

            operands = ", ".join(buf)

        self.logger.debug("IP {:04d}:\tBYTECODE {:10s}\tOPERAND COUNT {}\tOPERANDS {:10s}".format(
            self.ip, opcode.dump_bytecode(), opcode.operand_count, operands))

        return "{:04d}:\t{:10s}\t{:10s}".format(self.ip, opcode.dump_bytecode(), operands)

    def dump_stack(self):
        '''Return the dump of the stack.'''
        buf = []

        if self.sp < 0:
            return ""

        for idx in range(self.sp + 1):
            buf.append(str(self.stack[idx]))

        return "STACK [{}]".format(", ".join(buf))

    def print_stack(self):
        self.logger.info(self.dump_stack())

    def dump_data_memory(self):
        '''Return the dump of the data memory.'''
        addr = 0
        buf = ["Data memory:\n"]
        for d in self.data:
            if d is not None:
                buf.append("{0:>4d} {1}".format(addr, d))
            addr += 1

        return "\n".join(buf)

    def print_data_memory(self):
        self.logger.info(self.dump_data_memory())

    def dump_code_memory(self):
        '''Return the dump of the code memory.'''
        addr = 0
        buf = ["Code memory:\n"]
        for c in self.code:
            buf.append("{0:>04d} {1}".format(addr, c))
            addr += 1

        return "\n".join(buf)

    def print_code_memory(self):
        self.logger.info(self.dump_code_memory())
