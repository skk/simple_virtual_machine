'''
simple-virtual-machine: Main module
'''

import logging
import logging.config

logging.basicConfig(level=logging.INFO,
                    datefmt='%y-%m-%d %H:%M:%S',
                    format='%(asctime)s %(name)-12s %(funcName)s %(filename)s:%(lineno)d %(levelname)-8s %(message)s')
                    

def main():
    from docopt import docopt
    usage = """A Simple Virtual Machine

Usage:
  simple-vritual-machine (-h | --help)
  simple-vritual-machine --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
    arguments = docopt(usage, version='simple version machien 1.0')
    print arguments

if __name__ == '__main__':
    main()
