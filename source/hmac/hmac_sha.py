#!/usr/bin/env python
"""Generate an HMAC signature using SHA1.
"""
#end_pymotw_header

import hmac
import hashlib

digest_maker = hmac.new('secret-shared-key-goes-here',
                        '',
                        hashlib.sha1)

with open('hmac_sha.py', 'rb') as f:
    while True:
        block = f.read(1024)
        if not block:
            break
        digest_maker.update(block)

digest = digest_maker.hexdigest()
print digest
