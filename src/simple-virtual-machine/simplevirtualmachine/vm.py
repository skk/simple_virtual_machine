# -*- coding: utf-8 -*-

import logging

import operator

from simplevirtualmachine.bytecodes import INVALID, IADD, ISUB, IMUL, \
    IEQ, ILT, BR, BRT, BRF, ICONST, LOAD, GLOAD, STORE, GSTORE, \
    PUTS, POP, CALL, RET, HALT, Bytecode, InvalidBytecodeError

TRUE = 1
FALSE = 0

class Stack(object):

    def __init__(self):
        self.items = []
        self.stack_pointer = 0
        self.logger = logging.getLogger(__name__)

    def push(self, item):
        self.items.append(item)
        self.stack_pointer += 1
        self.next_idx = 0

    def pop(self, popcount = 1):
        data = []
        #self.logger.debug("popcout {}".format(popcount))
        #self.logger.debug("self.items len {}".format(len(self.items)))
        #self.logger.debug("self.items {}".format(self.items))
        #self.logger.debug("self.stack_pointer {}".format(self.stack_pointer))
        for i in range(popcount):
            try:
                data.append(self.items.pop())
            except IndexError as e:
                pass
                #self.logger.debug("self.pop({}) error: {}".format(popcount, e))
            else:
                self.stack_pointer -= 1
                #self.logger.debug("self.stack_pointer {}".format(self.stack_pointer))
        

        if len(data) == 1:
            return data[0]
        else:
            return data

    def __setitem__(self, key, value):
        self.items[key] = value

    def __getitem__(self, key):
        return self.items[key]

    def __len__(self):
        return len(self.items)

    def isEmpty(self):
        return (self.items == [])

    def __iter__(self):
        return self

    def next(self):
        #self.logger.debug("stack.next next_idx {}".format(self.next_idx))
        #self.logger.debug("stack.next stack_pointer {}".format(self.stack_pointer))
        if self.next_idx < (self.stack_pointer):
            #self.logger.debug("stack.next next_idx {}".format(self.next_idx))
            v = self.items[self.next_idx]
            self.next_idx += 1         
            return v
        else:
            self.next_idx = 0        
            raise StopIteration

class VM(object):
    """Implemenation of a (very) simple virtual machine."""

    def __init__(self, *code):
        VM.DEFAULT_STACK_SIZE = 1000
        self.ip = 0
        self.fp = -1
        self.code = code
        self.stack = Stack()
        self.data = [None for i in range(VM.DEFAULT_STACK_SIZE)]
        self.logger = logging.getLogger(__name__)
        self.logger.debug("\n")

    @classmethod
    def format_instr_or_object(cls, obj):
        """Return string with obj formatted as an instruction."""
        if isinstance(obj, Bytecode):
            return Bytecode.to_instruction_from_opcode(obj.opcode)
        else:
            return str(obj)

    def __str__(self):
        '''Return the current state of the VM (e.g. FP, IP, STACK, etc).'''
        #buf = ["FP: {fp} IP: {ip}".format(fp=self.fp, ip=self.ip)]
        #buf.append(self.dump_stack())
        #buf.append(self.dump_data_memory())
        #buf.append(self.dump_code_memory())

        #return "\n".join(buf)
        return ""

    def binopt(self, operator):
        [b, a] = self.stack.pop(2)
        result = operator(a, b)
        result = 1 if result else 0 # use 1 or 0 rather than True or False for booleans
        self.stack.push(result)

    def run(self):
        '''Simulate the fetch-decode execute cycle.'''
        # fetch opcode
        opcode = self.code[self.ip]
        rv = HALT
        
        while opcode != HALT and self.ip <= len(self.code):
            trace = self.display_instruction()
            #self.logger.debug("{}".format(self.display_instruction()))
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
                self.binopt(operator.br)
            elif opcode == BR:
                self.ip = self.code[self.ip]
            elif opcode == BRT:
                addr = self.code[self.ip]
                self.ip += 1
                if self.stack.pop() == TRUE:
                    self.ip = addr
            elif opcode == BRF:
                addr = self.code[self.ip]
                self.ip += 1
                if self.stack.pop() == FALSE:
                    self.ip = addr
            elif opcode == ICONST:
                self.stack.push(self.code[self.ip])
                self.ip += 1
            elif opcode == LOAD:
                offset = self.code[self.ip]
                self.ip += 1
                self.stack.push(self.stack[self.fp+offset])
            elif opcode == GLOAD:
                addr = self.code[self.ip]
                self.ip += 1
                self.stack.push(self.data[addr])
            elif opcode == STORE:
                offset = self.code[self.ip]
                self.ip += 1
                self.stack[self.fp + offset] = self.stack.pop()
            elif opcode == GSTORE:
                addr = self.code[self.ip]
                self.ip += 1
                self.data[addr] = self.stack.pop()
            elif opcode == PUTS:
                msg = "OUTPUT: {}".format(self.stack.pop())
                print msg
                self.logger.debug(msg)
            elif opcode == POP:
                self.stack.pop()
            elif opcode == CALL:
                addr = self.code[self.ip]                       # target addr of function
                self.ip += 1
                number_args = self.code[self.ip]                # number of args
                self.ip += 1

                self.stack.push(number_args)                    # save number of args
                self.stack.push(self.fp)                        # save fp
                self.stack.push(self.ip)                        # save return addr
                
                #self.logger.debug("CALL self.stack.items {}".format(self.stack.items))

                self.fp = self.stack.stack_pointer              # fp points to return addr on stack
                self.ip = addr                                  # jump to function
            elif opcode == RET:
                rvalue = self.stack.pop()                       # pop return value
                self.stack.stack_pointer = self.fp              # jump over loads to fp

                #for n in range(self.fp):
                #    self.stack.pop()

                #self.logger.debug("RET self.stack.items {}".format(self.stack.items))

                #self.logger.debug("FP {}".format(self.fp))
                self.ip = self.stack.pop()                      # pop return address
                self.fp = self.stack.pop()                      # return fp
                number_args = self.stack.pop()                  # number of args

                #self.logger.debug("self.ip {}".format(self.ip))
                #self.logger.debug("self.fp {}".format(self.fp))
                #self.logger.debug("number_args {}".format(number_args))
                for n in range(number_args):                    # pop args
                    self.stack.pop()

                self.stack.push(rvalue)                         # leave result on stack
            elif opcode == HALT:
                rv = HALT
            else:
                rv = INVALID
                raise InvalidBytecodeError("Invalid opcode {opcode} at ip = {ip}".format(opcode=opcode, ip=self.ip - 1))
            trace += self.dump_stack()
            self.logger.debug("{}".format(trace))

            #trace += self.display_instruction()
            #trace += self.dump_stack()
            #self.logger.debug("{}".format(trace))
            opcode = self.code[self.ip]

        self.print_code_memory()
        self.print_data_memory()
        return rv

    def display_instruction(self):
        '''Dislay instruction'''
        opcode = self.code[self.ip]
        operands = []
        
        operands = ""
 
        if opcode.operand_count > 0:
            start_idx = self.ip + 1
            end_idx = self.ip + opcode.operand_count
            buf = []
            for idx in range(start_idx, end_idx):
                buf.append("{} ".format(self.code[idx]))

            operands = ", ".join(buf)

        return "IP {:04d}:\tBYTECODE {:10s}\tOPERAND COUNT {}\tOPERANDS {:10s}".format(
            self.ip, opcode.dump_bytecode(), opcode.operand_count, operands)

       
        #self.logger.debug("opcode {}".format(opcode))
        #if opcode.operand_count == 1:
            #operands = "{}".format(self.code[self.ip+1])
        #
        #if opcode.operand_count == 2:
            #operands = "{}, {}".format(self.code[self.ip+1], self.code[self.ip+2])
        
        #return "{:04d}: {:10s} {:10s}\t\t{:10s}".format(self.ip, opcode.dump_bytecode(), operands, self.dump_stack())
        #return "IP: {:04d}: OPCODE: {} OPERANDS: [{}]".format(self.ip, opcode, operands)
        #return "{:04d}: {:10s} {:10s}".format(self.ip, opcode.dump_bytecode(), operands)

    
    def dump_stack(self):
        '''Return the dump of the stack.'''
        buf = []

        for s in self.stack:
            buf.append(str(s))

        return "STACK [{}]".format(", ".join(buf))

    def print_stack(self):
        self.logger.debug(self.dump_stack())

    def dump_data_memory(self):
        '''Return the dump of the data memory.'''
        addr = 0
        buf = ["\nData memory:"]
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
        buf = ["\nCode memory:"]
        for c in self.code:
            buf.append("{0:>04d} {1}".format(addr, c))
            addr += 1

        return "\n".join(buf)

    def print_code_memory(self):
        self.logger.debug(self.dump_code_memory())
