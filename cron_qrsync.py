#!/usr/bin/env python

import sys
import subprocess
import time

def do_qrsync(qrsync_exec_path,qrsync_conf,interval):
    try:
        while 1:
            try:
                rc = subprocess.call([qrsync_exec_path,qrsync_conf])
            except Exception:
                pass
        
            print 'qrsync done'
            time.sleep(interval)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    qrsync_exec_path,qrsync_conf = sys.argv[1:3]
    if len(sys.argv)>=4:
        interval = sys.argv[3]
    else:
        interval = 30
    do_qrsync(qrsync_exec_path,qrsync_conf,float(interval))


