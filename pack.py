#!/usr/bin/env python

import sys
import paktools

'''Packs a directory into a .pak file'''

def main():
  if len(sys.argv) <= 1:
    print "Usage: %s <directory> [file]" % sys.argv[0]
    return
  
  directory = sys.argv[1]
  file      = sys.argv[2] if len(sys.argv) >= 3 else "%s.pak" % (directory)
  
  paktools.PackDirectoryIntoFile(directory, file)

if __name__ == '__main__':
  main()