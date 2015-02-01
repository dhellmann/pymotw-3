#!/usr/bin/env python
# encoding: utf-8
#
# Copyright 2009 Doug Hellmann.
#
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software
# and its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Doug Hellmann not be used in advertising or publicity
# pertaining to distribution of the software without specific,
# written prior permission.
#
# DOUG HELLMANN DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS, IN NO EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY
# SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.
#
"""
"""
#end_pymotw_header

import grp

# Load all of the user data, sorted by username
all_groups = grp.getgrall()
interesting_groups = {
    g.gr_name: g
    for g in all_groups
    if not g.gr_name.startswith('_')
}
print(len(interesting_groups.keys()))

# Find the longest length for a few fields
name_length = max(len(k) for k in interesting_groups) + 1
gid_length = max(len(str(u.gr_gid))
                 for u in interesting_groups.values()) + 1

# Print report headers
fmt = '%-*s %*s %10s %s'
print(fmt % (name_length, 'Name',
             gid_length, 'GID',
             'Password',
             'Members'))
print('-' * name_length,
      '-' * gid_length,
      '-' * 10,
      '-' * 30)

# Print the data
for name, g in sorted(interesting_groups.items()):
    print(fmt % (name_length, g.gr_name,
                 gid_length, g.gr_gid,
                 g.gr_passwd,
                 ', '.join(g.gr_mem)))
