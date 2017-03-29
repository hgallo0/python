#!/bin/python

import getopt
import sys

print 'ARGV      :', sys.argv[1:]

def usage():
  print "usage\n ./getopts.py -f -g -a -v"
  print "\n./getopts.py --file --group --all --version"

def usegetopts():
  try:
    options, remainder = getopt.getopt(sys.argv[1:], 'f:g:a:v:', ['file=',
                                                                  'group',
                                                                  'all',
                                                                  'version',
                                                                 ])
  except getopt.GetoptError as err:
    usage()
    sys.exit(2)

  print 'OPTIONS   :', options

  for opt, arg in options:
    if opt in ('-f', '--file'):
        output_filename = arg
    elif opt in ('-g', '--group'):
        output_filename = arg
    elif opt in ('-a', '--all'):
        output_filename = arg
    elif opt in ('-v', '--version'):
        output_filename = arg

usegetopts()
