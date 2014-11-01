'''
simple-virtual-machine: Main module
'''

import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,              
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',    
            'class':'logging.StreamHandler',
        },  
    },
    'loggers': {
        '': {                  
            'handlers': ['default'],        
            'level': 'DEBUG',  
            'propagate': True  
        },
    }
}

logging.config.dictConfig(LOGGING_CONFIG)




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
