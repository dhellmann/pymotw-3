#!/usr/bin/env python3
"""More interaction between child processes.
"""
#end_pymotw_header

import subprocess

print('One line at a time:')
proc = subprocess.Popen(
    'python3 repeater.py',
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)
for i in range(5):
    line = ('%d\n' % i).encode('utf-8')
    proc.stdin.write(line)
    proc.stdin.flush()
    output = proc.stdout.readline().decode('utf-8')
    print(output.rstrip())
remainder = proc.communicate()[0].decode('utf-8')
print(remainder)

print()
print('All output at once:')
proc = subprocess.Popen(
    'python3 repeater.py',
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)
for i in range(5):
    line = ('%d\n' % i).encode('utf-8')
    proc.stdin.write(line)

output = proc.communicate()[0].decode('utf-8')
print(output)
