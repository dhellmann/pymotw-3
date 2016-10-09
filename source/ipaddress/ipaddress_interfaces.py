#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2016 Doug Hellmann.  All rights reserved.
# Written for https://pymotw.com
#
"""
"""
#end_pymotw_header

import ipaddress


ADDRESSES = [
    '10.9.0.6/24',
    'fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa/64',
]


for ip in ADDRESSES:
    iface = ipaddress.ip_interface(ip)
    print('{!r}'.format(iface))
    print('    network:', iface.network)
    print('         ip:', iface.ip)
    print('  prefixlen:', iface.with_prefixlen)
    print('    netmask:', iface.with_netmask)
    print('   hostmask:', iface.with_hostmask)
    print()
