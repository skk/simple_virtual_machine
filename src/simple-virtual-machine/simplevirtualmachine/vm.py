# -*- coding: utf-8 -*-

from simplevirtualmachine.bytecodes.bytecodes import *
from simplevirtualmachine.bytecodes.instruction import Instruction

import logging

class VM:
    """Implemenation of a (very) simple virtual machine."""
    
    def __init__(self, code, ip = 0, datasize = 0):
        self.code = code
        self.ip = ip
        self.fp = 0
        self.sp = -1
        self.data = [None] * len(self.code)
        self.stack = [None] * len(self.code)
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug("\n" + "-" * 80)
        
    def format_instr_or_object(self, obj):
        """Return string with obj formatted as an instruction."""
        if isinstance(obj, Instruction):
            return Instruction.to_instruction_from_opcode(obj.opcode)
        else:
            return str(obj)
        
    def __str__(self):
        '''Return the current state of the VM (e.g. FP, IP, STACK, etc).'''
        buf = ["FP {fp}, IP {ip}, SP {sp},\nDATA {data},\nSTACK {stack},\n".format(fp = self.fp, ip = self.ip, data = self.data, stack = self.stack)]
        buf.append("CODE ['")
        bufcode = []
        for k, v in dic.iteritems():
            bufcode.append(self.format_instr_or_object(v))
            
            buf.append(",".join(bufcode))
            buf.append(']')
            
            return "".join(buf)
        
    def run(self):
        '''Exec the virual machine.'''
        # fetch opcode
        opcode = self.code[self.ip]
        rv = HALT

        self.logger.debug(self.dump_stack())

        while opcode != HALT and self.ip <= len(self.code):
            self.logger.debug(self.display_instruction())
            self.ip += 1
            
            # decode
            if opcode == IADD:
                b = self.stack[self.sp]; self.sp -= 1
                a = self.stack[self.sp]; self.sp -= 1
                self.stack[self.sp] = a + b
                self.sp += 1
            elif opcode == ISUB:
                b = self.stack[self.sp]; self.sp -= 1
                a = self.stack[self.sp]; self.sp -= 1
                self.stack[self.sp] = a - b
                self.sp += 1
            elif opcode == IMUL:
                b = self.stack[self.sp]; self.sp -= 1
                a = self.stack[self.sp]; self.sp -= 1
                self.stack[self.sp] = a * b
                self.sp += 1
            elif opcode == ILT:
                b = self.stack[self.sp]; self.sp -= 1
                a = self.stack[self.sp]; self.sp -= 1
                self.stack[self.sp] = (a < b)
                self.sp += 1
            elif opcode == IEQ:
                b = self.stack[self.sp]; self.sp -= 1
                a = self.stack[self.sp]; self.sp -= 1
                self.stack[self.sp] = (a == b)
                self.sp += 1
            elif opcode == BR:
                pass
            elif opcode == BRT:
                pass 
            elif opcode == BRF:
                pass
            elif opcode == ICONST:
                v = self.code[self.ip]
                self.ip += 1

                self.sp += 1
                self.stack[self.sp] = v
            elif opcode == LOAD:
                pass
            elif opcode == GLOAD:
                pass
            elif opcode == STORE:
                pass
            elif opcode == GSTORE:
                pass
            elif opcode == PUTS:
                v = self.stack[self.sp]
                self.sp -= 1
                print "OUTPUT: {}".format(v)
                self.logger.debug("OUTPUT: {}".format(v))
            elif opcode == POP:
                pass
            elif opcode == CALL:
                pass
            elif opcode == RET:
                pass
            elif opcode == HALT:
                rv = HALT
            else:
                rv = INVALID
                raise StandardError("Invalid opcode {opcode} at ip = {ip}".
                                    format(opcode = opcode, ip = self.ip  -1 ))
            
            self.logger.debug(self.dump_stack())
            self.logger.debug("\n")
            opcode = self.code[self.ip]
        
        
        self.logger.debug(self.display_instruction())
        self.logger.debug(self.dump_stack())
        self.logger.debug("\n")
        self.logger.debug(self.dump_data_memory())
        self.logger.debug(self.dump_code_memory())
        self.logger.debug("RV {rv}".format(rv=rv))
        return rv
    
    def display_instruction(self):
        '''Dislay instruction'''
        opcode = self.code[self.ip]
        
        if opcode.operand_count > 0:
            start_idx = self.ip + 1
            end_idx = self.ip + opcode.operand_count
            buf = []
            for i in range(start_idx, end_idx):
                buf.append(code[idx])
    
            operands = ", ".join(buf)
            return "IP: {:04d}: SP: {:04d} OPCODE: {:10s} OPERANDS: {:10s}".format(
                self.ip, self.sp, Instruction.to_instruction_from_opcode(opcode), operands)

        return ""
        
    def dump_stack(self):
        '''Return the dump of the stack.'''
        buf = []
        for s in self.stack:
            if s != None:
                buf.append(str(s))
        
        return "SP {}, stack=[{:10s}]".format(self.sp, ", ".join(buf))
            
    def dump_data_memory(self):
        '''Return the dump of the data memory.'''
        addr = -1
        buf = ["Data memory:"]
        for d in self.data:
            addr += 1
            if d != None:
                buf.append("{:4d} {}".format(addr, d))
        
        return "\n".join(buf)
            
    def dump_code_memory(self):
        '''Return the dump of the code memory.'''
        addr = -1
        buf = ["Code memory:"]
        for c in self.code:
            addr += 1
            if c != None:
                buf.append("{:4d} {}".format(addr, c))
                
        return "\n".join(buf)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
