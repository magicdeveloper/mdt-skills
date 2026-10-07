#!/usr/bin/env python3
"""Wait for subagent fact files to appear and stabilize.

Usage: wait_for_units.py <facts_dir> <expected> [--interval 30] [--cycle 300]
Exit 0: all expected unit files are present and their size is stable
        across two consecutive checks.
Exit 1: cycle timed out; prints done/missing lists.

A unit counts as complete only when its file size is unchanged between two
checks (a subagent may still be writing). Expected files: unit-NNNN.facts.txt
"""
import argparse
import glob
import json
import os
import sys
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('facts_dir')
    ap.add_argument('expected', type=int)
    ap.add_argument('--interval', type=int, default=30)
    ap.add_argument('--cycle', type=int, default=300)
    a = ap.parse_args()

    expected = {'unit-%04d.facts.txt' % i for i in range(1, a.expected + 1)}
    prev = {}
    done = set()
    deadline = time.time() + a.cycle
    while time.time() < deadline:
        cur = {os.path.basename(p): os.path.getsize(p)
               for p in glob.glob(os.path.join(a.facts_dir, 'unit-*.facts.txt'))
               if os.path.basename(p) in expected}
        done = {n for n in cur if n in prev and prev[n] == cur[n] and cur[n] > 0}
        missing = sorted(expected - done)
        print('check: %d/%d done, missing: %s'
              % (len(done), a.expected, ', '.join(missing) or 'none'))
        if len(done) == a.expected:
            print('ALL UNITS COMPLETE')
            sys.exit(0)
        prev = cur
        time.sleep(a.interval)
    print(json.dumps({'status': 'timeout', 'done': sorted(done),
                      'missing': sorted(expected - done)}))
    sys.exit(1)


if __name__ == '__main__':
    main()
