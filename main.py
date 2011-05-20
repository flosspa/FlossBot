#!/usr/bin/env python

import sys, socket, string, random, os, time
from Events import *
from Irc import *

irc = None
running = True

def restartIRCHook(event):
    global irc

    time.sleep(5)
    irc.connect()

def main(args):
    global irc
    
    if len(sys.argv) != 4:
        print 'Uso: main.py \'<servidor>\' <puerto> \'<canal>\''
        sys.exit(1)

    listener = Listener(IRC_RESTART, restartIRCHook)
    getEventManager().addListener(listener)

    host = args[1]
    port = int(args[2])
    channel = args[3]
    if channel[0] != '#':
        channel = '#' + channel

    getEventManager().start()

    irc = Irc(host, port, channel)

    while running:
        try:
            i = raw_input()
            if i == "quit" or i == "exit":
                irc.disconnect()
                getEventManager().stop()
                break
        except KeyboardInterrupt:
            irc.disconnect()
            getEventManager().stop()
            break

    time.sleep(1)
    sys.exit()

if __name__ == '__main__':
    main(sys.argv)

