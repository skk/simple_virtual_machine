# -*- coding: utf-8 -*-

from simplevirtualmachine.bytecodes.bytecodes import *
from simplevirtualmachine.vm import VM

def test_halt():
    assert VM([HALT]).run() == HALT
 
def test_load_and_halt():
    vm = VM([
        ICONST, 100, HALT 
    ])
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
    assert vm.stack[vm.sp] == 1+2
    
    # should halt
    assert rv == HALT

def test_load_two_constants_mul_and_halt():
    vm = VM([ICONST, 2, ICONST, 8, IMUL, PUTS, HALT])
    rv = vm.run()
       
    # stack should have result of IMUL
    assert vm.stack[vm.sp] == 2*8
       
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

