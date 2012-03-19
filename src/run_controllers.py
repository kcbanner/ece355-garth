#!/usr/bin/env python2

import sys
import signal
import logging
import argparse
import threading
from eventmanager import EventManager
from sensorcontroller import SensorController
from systemcontroller import SystemController

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--peers',
                        help='comma seperated list of peers to connect to. ' +
                        'eg: \'localhost:8001,localhost:8002\'',
                        dest='peers')
    parser.add_argument('-l',
                        '--listen',
                        help='port to listen on',
                        type=int,
                        required=True,
                        dest='port')
    parser.add_argument('-r',
                        '--remote-url',
                        required=True,
                        type=str,
                        dest='remote_url',
                        help='URL of remote server')
    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        dest='verbose',
                        help='show debug logging')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Parse peer list
    peer_list = []
    if args.peers:
        for peer in args.peers.split(','):
            peer_list.append(tuple(peer.split(':')))

    # Setup EventManager and Controllers
    event_manager = EventManager(peer_list, args.port)
    sensor_controller = SensorController(event_manager)
    system_controller = SystemController(event_manager, args.remote_url)

    # Start controllers
    controllers = (system_controller, sensor_controller)

    threads = []
    for controller in controllers:
        thread = threading.Thread(target=controller.run)
        thread.start()
        threads.append(thread)

    logging.info('Controllers started')

    # Watch threads
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
