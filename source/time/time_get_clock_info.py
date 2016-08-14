#!/usr/bin/env python3
# encoding: utf-8
#
"""The difference between clock and time.
"""
#end_pymotw_header

import textwrap
import time

available_clocks = [
    'clock',
    'monotonic',
    'perf_counter',
    'process_time',
    'time',
]

for clock_name in available_clocks:
    print(textwrap.dedent('''\
    {name}:
        adjustable    : {info.adjustable}
        implementation: {info.implementation}
        monotonic     : {info.monotonic}
        resolution    : {info.resolution}
    ''').format(
        name=clock_name,
        info=time.get_clock_info(clock_name))
    )
