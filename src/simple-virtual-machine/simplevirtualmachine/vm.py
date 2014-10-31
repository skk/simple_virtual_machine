# -*- coding: utf-8 -*-

import logging

from simplevirtualmachine.bytecodes import INVALID, IADD, ISUB, IMUL, \
    IEQ, ILT, BR, BRT, BRF, ICONST, LOAD, GLOAD, STORE, GSTORE, \
    PUTS, POP, CALL, RET, HALT, Bytecode, InvalidBytecodeError

TRUE = 1
FALSE = 0

class VM(object):
    """Implemenation of a (very) simple virtual machine."""

    def __init__(self, *code):
        VM.DEFAULT_STACK_SIZE = 1000
        self.ip = 0
        self.fp = -1
        self.sp = -1
        self.code = code
        self.stack = [None for i in range(VM.DEFAULT_STACK_SIZE)]
        self.data = [None for i in range(VM.DEFAULT_STACK_SIZE)]
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(message)s')
        handler = logging.StreamHandler()
        # handler = logging.FileHandler("./vm-output.log")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("-" * 80)

    @classmethod
    def format_instr_or_object(cls, obj):
        """Return string with obj formatted as an instruction."""
        if isinstance(obj, Bytecode):
            return Bytecode.to_instruction_from_opcode(obj.opcode)
        else:
            return str(obj)

    def __str__(self):
        '''Return the current state of the VM (e.g. FP, IP, STACK, etc).'''
        buf = ["FP: {fp} IP: {ip} SP: {sp}".format(fp=self.fp, ip=self.ip, sp=self.sp)]
        buf.append(self.dump_stack() + "\n")
        buf.append(self.dump_data_memory() + "\n")
        buf.append(self.dump_code_memory())

        return "\n".join(buf)
    
    def top_two_stack(self):
        b = self.stack[self.sp]
        self.sp -= 1
        a = self.stack[self.sp]
        self.sp -= 1
        return (b, a)

    def run(self):
        '''Simulate the fetch-decode execute cycle.'''
        # fetch opcode
        opcode = self.code[self.ip]
        rv = HALT

        while opcode != HALT and self.ip <= len(self.code):
            self.logger.debug(self.display_instruction())
            self.ip += 1

            # decode
            if opcode == IADD:
                (b, a) = self.top_two_stack()
                self.sp += 1
                self.stack[self.sp] = a + b
            elif opcode == ISUB:
                (b, a) = self.top_two_stack()
                self.sp += 1
                self.stack[self.sp] = a - b
            elif opcode == IMUL:
                (b, a) = self.top_two_stack()
                self.sp += 1
                self.stack[self.sp] = a * b
            elif opcode == ILT:
                (b, a) = self.top_two_stack()
                self.sp += 1
                self.stack[self.sp] = TRUE if a < b else FALSE
            elif opcode == IEQ:
                (b, a) = self.top_two_stack()
                self.sp += 1
                self.stack[self.sp] = TRUE if a == b else FALSE
            elif opcode == BR:
                self.ip = self.code[self.ip]
            elif opcode == BRT:
                addr = self.code[self.ip]
                self.ip += 1
                if self.stack[self.sp] == TRUE:
                    self.ip = addr
                self.sp -= 1
            elif opcode == BRF:
                addr = self.code[self.ip]
                self.ip += 1
                if self.stack[self.sp] == FALSE:
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
                self.logger.debug(msg)
            elif opcode == POP:
                self.sp -= 1
            elif opcode == CALL:
                pass
            elif opcode == RET:
                pass
            elif opcode == HALT:
                rv = HALT
            else:
                rv = INVALID
                raise InvalidBytecodeError("Invalid opcode {opcode} at ip = {ip}".format(
                    opcode=opcode, ip=self.ip - 1))
            
            self.print_stack()
            opcode = self.code[self.ip]

        self.logger.debug("{}".format(self))
        return rv

    def display_instruction(self):
        '''Dislay instruction'''
        opcode = self.code[self.ip]
        operands = []
        self.logger.debug("opcode {}".format(opcode))
            
        operands = ""
        if opcode.operand_count > 0:
            start_idx = self.ip + 1
            end_idx = self.ip + opcode.operand_count
            buf = []
            for idx in range(start_idx, end_idx + 1):
                buf.append("{}".format(self.code[idx]))

            operands = ", ".join(buf)

        return "IP: {:04d}: SP: {:04d} OPCODE: {} OPERANDS: [{}]".format(
            self.ip, self.sp, opcode, operands)

    def dump_stack(self):
        '''Return the dump of the stack.'''
        buf = []
        if self.sp < 0:
            return ""

        for idx in range(self.sp + 1):
            buf.append(str(self.stack[idx]))
            
        return "SP {}, stack=[{}]".format(self.sp, ", ".join(buf))
            
    def print_stack(self):
        self.logger.debug(self.dump_stack())

    def dump_data_memory(self):
        '''Return the dump of the data memory.'''
        addr = 0
        buf = ["Data memory:"]
        for d in self.data:
            if d is not None:
                buf.append("{0:>4d} {1}".format(addr, d))
            addr += 1
               
        return "\n".join(buf)

    def print_data_memory(self):
        self.logger.debug(self.dump_data_memory())
                    
    def dump_code_memory(self):
        '''Return the dump of the code memory.'''
        addr = 0
        buf = ["Code memory:"]
        for c in self.code:
            buf.append("{0:>04d} {1}".format(addr, c))
            addr += 1
                                
        return "\n".join(buf)
                            
    def print_code_memory(self):
        self.logger.debug(self.dump_code_memory())
                            
                            
                            
