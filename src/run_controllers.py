#!/usr/bin/env python2

import sys
import signal
import logging
import argparse
import threading
from eventmanager import EventManager
from systemcontroller import SystemController

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--peers',
                        help='comma seperated list of peers to connect to. eg: \'localhost:8001,localhost:8002\'',
                        dest='peers')
    parser.add_argument('-l',
                        '--listen',
                        help='port to listen on',
                        type=int,
                        required=True,
                        dest='port')
    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        dest='verbose',
                        help='show debug logging')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    peer_list = []
    if args.peers:
        for peer in args.peers.split(','):
            peer_list.append(tuple(peer.split(':')))

    # Setup EventManager and Controllers
    event_manager = EventManager(peer_list, args.port)
    system_controller = SystemController(event_manager)

    # Start controllers
    controllers = (system_controller,)
    threads = []
    for controller in controllers:
        thread = threading.Thread(target=controller.run)
        thread.start()
        threads.append(thread)

    while len(threads) > 0:
        try:
            for thread in threads:
                if thread.isAlive():
                    thread.join(1)
                else:
                    threads.remove(thread)

        except KeyboardInterrupt, e:
            logging.info('Stopping all controllers...')
            for controller in controllers:
                controller.stop()

    logging.info('All controllers stopped')


