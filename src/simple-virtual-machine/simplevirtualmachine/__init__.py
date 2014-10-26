'''
simple-virtual-machine: Main module

Copyright 2014, Steven Knight
Licensed under MIT.
'''

from docopt import docopt

def main():
    
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
