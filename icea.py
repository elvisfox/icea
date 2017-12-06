import sys

from config import *
from utils.csv_reader import csv_reader

# open input file
try:
	csvr = csv_reader(sys.argv[1])
except:
	print('Failed to open input file.\n')
	sys.exit(1)


l = csvr.readline()

print(csvr.col_list)
print(l)