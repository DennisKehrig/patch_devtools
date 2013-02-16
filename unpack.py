#!/usr/bin/env python

import sys
import re
import paktools

'''Unpacks a .pak file into a directory'''

def main():
  if len(sys.argv) <= 1:
    print "Usage: %s <file> [directory]" % sys.argv[0]
    return
  
  file      = sys.argv[1]
  directory = sys.argv[2] if len(sys.argv) >= 3 else re.sub("\.pak$", "", file)
  
  paktools.UnpackFileIntoDirectory(file, directory)

if __name__ == '__main__':
  main()