import os
import time, SendMessage

def run(interval,random):
    while True:
        try:
            # sleep for the remaining seconds of interval
            # time_remaining = interval-time.time()%interval
            print SendMessage.randomly_inactive_node(random)
            time.sleep(interval)
        except Exception, e:
            print e


if __name__=="__main__":
    SendMessage.active_all_Nodes()
    random=60
    run(2,random)