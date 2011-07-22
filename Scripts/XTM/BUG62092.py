#!/usr/bin/python

import os
import time

def main():
    print 'Start to wgcmd status'
    count = 0;
    file = open('/tmp/mem.log', "ab")
    
    for i in range(24 * 60): # loop in every minute for one day.
        count += 1
        print 'This is the ' + str(count) + ' time to run'
        for i in range(10):
            print 'Get cert list for ' + str(i) + 'time'
            os.system('wgcmd status /certificate/list > /dev/null 2>&1')
            time.sleep(5)
        meminfo = os.popen('cat /proc/meminfo | grep -i memfree').readlines()
        file.writelines(meminfo)
    
    file.close
    
    
if __name__ == '__main__':
    main()