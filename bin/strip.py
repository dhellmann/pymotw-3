#!/usr/bin/env python3

import fileinput
import re

straight_pat = re.compile(':(class|data|const|command):`(.*?)`')
func_pat = re.compile(':func:`(.*?)(\(\))?`')

for line in fileinput.input(inplace=True):
    line = line.rstrip('\n')
    line = straight_pat.sub(r'``\2``', line)
    line = func_pat.sub(r'``\1()``', line)
    print(line)
