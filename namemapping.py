from collections import defaultdict
file1 = open('names.txt', 'r')
Lines = file1.readlines()
map=defaultdict()
count = 0
# Strips the newline character
def utilmap(point):
    map[point] = Lines.pop()[:-2]