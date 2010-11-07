#!/usr/bin/env python

import sys
import os
import os.path

RESULT_DATA_DIR = "percentages"

def Main():
  if os.path.isdir(RESULT_DATA_DIR) is not True:
    os.mkdir(RESULT_DATA_DIR)

  if len(sys.argv) == 1:
    sys.stderr.write("This program takes a bunch of files as arguments \
        converts them into no loss percentages, and writes them \
        in a percentages folder in the same directory.")

  for arg in sys.argv[1:]:
    ProcessFile(arg)

  return

def ProcessFile(f):

  output_filename = os.path.join(RESULT_DATA_DIR, os.path.basename(f))

  sys.stderr.write("Processing %s ++ %s\n"%(f, output_filename))

  fp = open(output_filename, "w")

  total_results = 0
  favourable_results = 0
  for line in open(f):
    result = int(line)
    if result != -1:
      favourable_results += 1
    total_results += 1
    percentage = float(favourable_results)/float(total_results) * 100

    fp.write("%.3f\n"%(percentage))

  fp.close()

if __name__ == '__main__':
  Main()
