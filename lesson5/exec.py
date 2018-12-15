#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import codecs
def myfun(input_file):
    p1 = re.compile(r'-\{.*?(zh-hans|zh-cn):([^;]*?)(;.*?)?\}-')
    p2 = re.compile(r'[（\(][，；。？！\s]*[）\)]')
    p3 = re.compile(r'[「『]')
    p4 = re.compile(r'[」』]')
    outfile = codecs.open('input_file' + '_std', 'w+', 'utf-8')
    with codecs.open(input_file, 'r', 'utf-8') as myfile:
        for line in myfile:
            line = p1.sub(r'\2', line)
            line = p2.sub(r'', line)
            line = p3.sub(r'“', line)
            line = p4.sub(r'”', line)
            outfile.write(line)
    outfile.close()
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py inputfile")
        sys.exit()
    input_file = sys.argv[1]
    myfun(input_file)