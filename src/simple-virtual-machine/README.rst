==================================================================
simple-virtual-machine: A simple virtual machine, written in Python
==================================================================

simple_virtual_machine
----------------------

After watching Terence Parr's great video on creating virtual machines (https://www.youtube.com/watch?v=OjaAToVkoTw).  I wanted to implement it myself and so this project was born.

Goals
-----

1. Implement a virtual machine in ruby with the same bytecodes as Terence's machine.
2. Expand the set of bytecodes to include floating support.
3. Include support for integer division.
4. Support running bytecodes from file stored on disk.
5. Learn about using Travis-CI.
6. Learn about using TDD.

Bytecodes
---------

* IADD
* ISUB
* IMUL
* IIL
* IEQ
* BR
* BRT
* BRF
* ICONST
* LOAD
* GLOAD
* STORE
* GSTORE
* PRINT
* POP
* CALL
* RET
* HALT

Contributing
------------

1. Fork it
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request

Copyright
---------

Copyright (c) 2014 Steven Knight. See LICENSE.txt for
further details.
